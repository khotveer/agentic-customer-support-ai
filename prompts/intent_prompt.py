def get_intent_prmpt(customer_message):
  return f"""You are a STRICT intent classification system for customer support.

      TASK:
      Classify the customer message into EXACTLY ONE of the following labels:

      complaint
      request
      inquiry

      LABEL DEFINITIONS (STRICT):

      complaint:
      - The customer reports a problem, issue, error, dissatisfaction, delay, incorrect charge, fee, or something that went wrong.
      - This INCLUDES questions phrased as “why”, “how”, or “what” IF they refer to a problem that already happened.

      request:
      - The customer explicitly asks for an action to be performed.
      - Examples: asking to change, cancel, reset, enable, disable, or initiate something.

      inquiry:
      - The customer asks ONLY for general information or clarification.
      - No problem has occurred yet.
      - The question is hypothetical, policy-based, or future-oriented.

      CRITICAL RULES (MUST FOLLOW):

      1. If the message refers to something that ALREADY happened to the customer → complaint
      2. If the message mentions charges, fees, declines, failures, errors, delays, or penalties → complaint
      3. If a problem is described, EVEN AS A QUESTION → complaint
      4. If both a problem and a request are present → complaint
      5. Use inquiry ONLY when:
        - No issue has occurred
        - No account-specific event is mentioned
      6. Choose ONLY ONE label
      7. Output ONLY the label text
      8. Do NOT explain
      9. Do NOT add punctuation or extra words

      EXAMPLES (IMPORTANT — LEARN THE PATTERN):

      Message: "Why did I get late charges on my credit card?"
      Label: complaint

      Message: "My credit card payment was declined even though I had balance"
      Label: complaint

      Message: "I was charged twice for the same transaction"
      Label: complaint

      Message: "What happens if I miss the due date on my credit card payment?"
      Label: inquiry

      Message: "How are late payment charges calculated?"
      Label: inquiry

      Message: "Please reverse the late fee on my card"
      Label: request

      Message: "Can you block my credit card?"
      Label: request

      NOW CLASSIFY THE FOLLOWING MESSAGE.

      Customer message:
      {customer_message}

      Answer:"""