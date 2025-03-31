import json
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
import numpy as np

def generate_embeddings(client, text, model="text-embedding-3-large"):
    try:
        response = client.embeddings.create(model=model, input=[text])
        embedding = response.data[0].embedding
    except Exception as e:
        print(f"Error during embedding generation: {e}")
        embedding = None
    return embedding

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("OPEN_AI_API_KEY")
    )
    # with open('data/combined.json', 'r') as file:
    #     data = json.load(file)
        
    # output = []
    # for idx, item in enumerate(data):
    #     embedding = generate_embeddings(client, item)
    #     output.append(embedding)
    #     if (idx + 1) % 25 == 0:
    #         print(f"Processed {idx + 1} items")
    
    # with open('data/embedded_data.json', 'w') as outfile:
    #     json.dump(output, outfile)
        
    # print("Data embedded successfully!")
    # print(len(output), len(output[0]) if output else 0)

    with open('data/contextual_data.json', 'r') as file:
        contextual_data = json.load(file)
    
    # print(f"Loaded {len(contextual_data)} items for contextual embeddings")
    # embedded_contextual_data = []


    # for idx, item in enumerate(contextual_data):
    #     print(f"Processing item {idx + 1}")
    #     nationality = item.get("Nationality", "Open to all nationalities.")
    #     mission = item.get("Description", "") + item.get("Mission", "Unspecified.")
    #     activities = item.get("Activities", "Unspecified.")

    #     nationality_embedding = generate_embeddings(client, nationality if nationality else "Open to all nationalities.")
    #     mission_embedding = generate_embeddings(client, mission if mission else "Unspecified.")
    #     activities_embedding = generate_embeddings(client, activities if activities else "Unspecified.")

    #     embedded_contextual_data.append({
    #         "Name": item.get("Name"),
    #         "Nationality": nationality_embedding,
    #         "Mission": mission_embedding,
    #         "Activities": activities_embedding
    #     })
        
    #     with open('data/embedded_contextual_data.json', 'w') as outfile:
    #         json.dump(embedded_contextual_data, outfile)
    
    with open('data/embedded_contextual_data.json', 'r') as file:
        embedded_contextual_data = json.load(file)
    
    embedded_contextual_data_dict = {}
    for item in embedded_contextual_data:
        embedded_contextual_data_dict[item["Name"]] = item
    with open('data/embedded_contextual_data_dict.json', 'w') as file:
        json.dump(embedded_contextual_data_dict, file, indent=4)
    
    # context_weights = [0.2, 0.5, 0.3]
    # weighted_contextual_data = []
    # for idx, item in enumerate(embedded_contextual_data):
    #     nationality_embedding = np.array(item["Nationality"])
    #     mission_embedding = np.array(item["Mission"])
    #     activities_embedding = np.array(item["Activities"])
        
    #     combined_embedding = np.average([nationality_embedding, mission_embedding, activities_embedding], axis=0, weights=context_weights)
    #     weighted_contextual_data.append(combined_embedding.tolist())

    # with open('data/weighted_embedded_contextual_data.json', 'w') as outfile:
    #     json.dump(weighted_contextual_data, outfile, indent=4)

    print("Contextual data embedded successfully!")