
from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    return model


def generate_embedding(text: str):
    """
    Convert text into a numerical vector.
    """
    embedding = get_model().encode(text)

    return embedding.tolist()
