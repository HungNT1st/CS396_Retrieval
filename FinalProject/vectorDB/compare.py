import json
import numpy as np

def cosine_similarity(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def main():
  # Load embeddings
  with open('data/weighted_embedded_contextual_data.json', 'r') as f:
    embeddings = json.load(f)
  # Load RSO names
  with open('data/clean.json', 'r') as f:
    rso_data = json.load(f)
  # Map RSO names to embeddings
  rso_embeddings = {}
  for idx, rso in enumerate(rso_data):
    name = rso['Name']
    embedding = embeddings[idx]
    rso_embeddings[name] = embedding
  # Get the target RSO embedding
  target_name = 'Vietnamese Students Association'
  target_embedding = None
  for name, embedding in rso_embeddings.items():
    if name.lower() == target_name.lower():
      target_embedding = np.array(embedding)
      break
  if target_embedding is None:
    print(f"RSO '{target_name}' not found.")
    return
  # Compute similarities
  similarities = []
  for name, embedding in rso_embeddings.items():
    if name.lower() == target_name.lower():
      continue
    sim = cosine_similarity(target_embedding, np.array(embedding))
    similarities.append((name, sim))
  # Get top 10
  top_10 = sorted(similarities, key=lambda x: x[1], reverse=True)[:10]
  # Print results
  print(f"Top 10 similar RSOs to '{target_name}':")
  for name, sim in top_10:
    print(f"{name}: {sim}")

if __name__ == "__main__":
  main()