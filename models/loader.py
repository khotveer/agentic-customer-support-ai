
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# required global variables
tokenizer = None
model = None


# helper function to load the mistralai model
def load_mistralai(use_fast=False , torch_dtype = torch.float16, device_map="auto"):

    global tokenizer, model

    if tokenizer is None or model is None:
      model_id = "mistralai/Mistral-7B-Instruct-v0.2"

      tokenizer = AutoTokenizer.from_pretrained(
          model_id,
          use_fast=use_fast  
      )

      tokenizer.pad_token = tokenizer.eos_token

      model = AutoModelForCausalLM.from_pretrained(
          model_id,
          torch_dtype=torch_dtype,
          device_map=device_map
      )

      print("Mistral 7B loaded successfully (slow tokenizer).")
      return tokenizer, model

# helper function to generate response from given prompt
def generate_text(
    prompt: str,
    max_new_tokens: int = 256,
    temperature: float = 0.2,
    top_p: float = 0.9,
    do_sample: bool = True,
):
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# helper function to get the response from model
def generate_text_mist(
    prompt: str,
    tokenizer,
    model,
    max_new_tokens: int = 256,
    temperature: float = 0.0,
    top_p: float = 0.9,
    do_sample: bool = False,
):
    """
    Generic text generation helper for Mistral.
    Safe for classification, API responses, and RAG answers.
    """

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    # ensure inputs are on same device as model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            use_cache=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode only the generated part
    generated_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return generated_text