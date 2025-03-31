from pinecone import Pinecone
import os
from dotenv import load_dotenv
import json

def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=api_key)
     
    with open('data/merged_data.json', 'r') as f:
        data = json.load(f)

    vectors = [
        {"id": str(i), "values": item["embedding"], "metadata": item["metadata"]}
        for i, item in enumerate(data)
    ]
    
    index = pc.Index("rso")
    chunk_size = 100 
    for chunk in chunk_data(vectors, chunk_size):
        index.upsert(   
            vectors=chunk,
            namespace="ns1"
        )
        print(f"Upserted {len(chunk)} items")

    # with open('data/embedded_contextual_data.json', 'r') as f:
    #     contextual_data = json.load(f)
    
    # nationality_index = pc.Index("rso-nationality")
    # mission_index = pc.Index("rso-mission")
    # activities_index = pc.Index("rso-activities")

    # nationality_vectors = []
    # mission_vectors = []
    # activities_vectors = []

    # for i, item in enumerate(contextual_data):
    #     nationality_vectors.append({
    #         "id": str(i),
    #         "values": item["Nationality"]
    #     })
    #     mission_vectors.append({
    #         "id": str(i),
    #         "values": item["Mission"]
    #     })
    #     activities_vectors.append({
    #         "id": str(i),
    #         "values": item["Activities"]
    #     })

    # print("Upserting nationality vectors")
    # for chunk in chunk_data(nationality_vectors, chunk_size):
    #     nationality_index.upsert(   
    #         vectors=chunk,
    #         namespace="ns1"
    #     )
    #     print(f"Upserted {len(chunk)} items")
    
    # print("Upserting mission vectors")
    # for chunk in chunk_data(mission_vectors, chunk_size):
    #     mission_index.upsert(   
    #         vectors=chunk,
    #         namespace="ns1"
    #     )
    #     print(f"Upserted {len(chunk)} items")
    
    # print("Upserting activities vectors")
    # for chunk in chunk_data(activities_vectors, chunk_size):
    #     activities_index.upsert(   
    #         vectors=chunk,
    #         namespace="ns1"
    #     )
    #     print(f"Upserted {len(chunk)} items")

        