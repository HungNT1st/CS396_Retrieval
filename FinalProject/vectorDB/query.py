from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
import json
from models.response_format import ContextualFormat

def generate_embeddings(client, text, model="text-embedding-3-large"):
    try:
        response = client.embeddings.create(model=model, input=[text])
        embedding = response.data[0].embedding
    except Exception as e:
        print(f"Error during embedding generation: {e}")
        embedding = None
    return embedding

def query(index, client, query, k = 2):
    embedding = generate_embeddings(client, query)
    
    res = index.query(
        namespace="ns1",
        vector=embedding,
        top_k=k,
        include_metadata=True,
    )
    return res

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_sim_explanation(client, query_text, target):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that explains similarities between student organizations."
            },
            {
                "role": "user",
                "content": f"""
                    Provide a concise yet detailed explanation of why the following student organization is similar to the organization in the given query text. Focus closely on the target students, its nationality and activities. Keep it up to 3 sentences. Do not use markdown format. Just pure text.

                    Query Text: {query_text}
                    Target Organization:
                    {json.dumps(target, indent=2)}
                    """
            }
        ]
    )
    explanation = response.choices[0].message.content.strip()
    return explanation


def context_query(indices, client, query_text, k = 2):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts relevant information from text."
            },
            {
                "role": "user",
                "content": f"""
                    Extract the following information from the text of a student organization below. Add as much detail as possible and include all relevant information. Include the name in nationality field. Activities should be long, explaining in great details what the organization does on a day-to-day basis. Do not include common information including board of officers and their duties, voting, protection from violations and discrimination. Do not make up or add information that does not exist in the text, even if it is from your own knowledge. Do not use new lines or non-UTF8 characters. Format to the given structure. Give a concise explanation on how it is similar to the reference:

                    Text: {query_text}
                    """
            }
        ],
        response_format=ContextualFormat
    )

    extracted = response.choices[0].message.parsed

    context_weights = [0.2, 0.5, 0.3]
    nationality_embeddings = generate_embeddings(client, extracted.nationality)
    mission_embeddings = generate_embeddings(client, extracted.mission)
    activities_embeddings = generate_embeddings(client, extracted.activities)
    overall_embeddings = np.average([nationality_embeddings, mission_embeddings, activities_embeddings], axis=0, weights=context_weights).tolist()

    res = indices[0].query(
        namespace="ns1",
        vector=overall_embeddings,
        top_k=k,
        include_metadata=True,
    )
    
    matches = []
    for rso in res['matches']:
        name = rso['metadata']['Name']
        score = rso['score']
        print(name, score)

        nationality_res = indices[1].query(namespace="ns1", id=rso['id'], top_k=1, include_values=True)['matches']
        mission_res = indices[2].query(namespace="ns1", id=rso['id'], top_k=1, include_values=True)['matches']
        activities_res = indices[3].query(namespace="ns1", id=rso['id'], top_k=1, include_values=True)['matches']
        
        nationality_sim = cosine_similarity(nationality_res[0]['values'], nationality_embeddings)
        mission_sim = cosine_similarity(mission_res[0]['values'], mission_embeddings)
        activities_sim = cosine_similarity(activities_res[0]['values'], activities_embeddings)

        # explanation = ""
        explanation = get_sim_explanation(client, query_text, rso['metadata'])
        matches.append({
            "name": name,
            "overall_score": score,
            "explanation": explanation,
            "contextual_score": {
                "nationality": nationality_sim,
                "mission": mission_sim,
                "activities": activities_sim
            }
        })

    return matches

def check(query_text, k = 2):
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=api_key)
    index = pc.Index("rso")
    nationality_index = pc.Index("rso-nationality")
    mission_index = pc.Index("rso-mission")
    activities_index = pc.Index("rso-activities")

    indices = [
        index,
        nationality_index,
        mission_index,
        activities_index
    ]
    
    client = OpenAI(
        api_key=os.getenv("OPEN_AI_API_KEY")
    )
    
    res = context_query(indices, client, query_text, k)
    return res