
from sentence_transformers import SentenceTransformer

embedding_model = None

def load_embedding_model(device="cpu"):
    global embedding_model
    if embedding_model is None:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
    return embedding_model