from app.services.embedding_service import generate_embedding

text = "Interested in food delivery and digital payments."

embedding = generate_embedding(text)

print("Embedding generated successfully!")
print("Vector dimensions:", len(embedding))
print("First five values:", embedding[:5])