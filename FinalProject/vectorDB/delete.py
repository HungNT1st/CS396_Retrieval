from pinecone import Pinecone
import os
from dotenv import load_dotenv

def delete_all_vectors():
  load_dotenv()
  api_key = os.getenv("PINECONE_API_KEY")
  pc = Pinecone(api_key=api_key)
  
  index = pc.Index("rso")
  index.delete(delete_all=True, namespace="ns1")
  print("All vectors deleted from the Pinecone database.")

if __name__ == "__main__":
  delete_all_vectors()