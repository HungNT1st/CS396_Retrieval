import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from vectorDB.count_tokens import strip_to_tokens_limit
from models.response_format import ContextualFormat

load_dotenv()

def extract_contextual_data(client, data):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts relevant and contextual information from text. You are neutral and completely unbiased."
            },
            {
                "role": "user",
                "content": strip_to_tokens_limit(f"""
                    Extract the following information from the text of a student organization below. Add as much detail as possible for each of the fields in the structure and include all relevant information. Activities should be long, explaining in great details what the organization does on a day-to-day basis. Do not include common information including board of officers and their duties, voting, protection from violations and discrimination. Do not make up or add information that does not exist in the text, even if it is from your own knowledge. Do not use new lines or non-UTF8 characters. If information about a given field is not specified, you may assume based on the description and documents. Do not write N/A or 'unspecified'. For example, if nationality is not specified but it's African Student Association, you may assume that its nationality is African, African American, etc. If it's for a science club, you can say 'Open to all students who are interested in science'. The default nationality is 'Open to all students with an interested in ___', not 'American'. Format to the given structure:

                    NAME: {data.get('Name')}
                    DESCRIPTION: {data.get('Description')}
                    SUMMARY: {data.get('Summary')}
                    DOCUMENTS: {data.get('Documents')}
                    """ , 128000)
            }
        ],
        response_format=ContextualFormat
    )

    extracted = response.choices[0].message.parsed
    print(extracted)
    formatted = {
        'Name': data.get('Name'),
        'Description': data.get('Description'),
        'Summary': data.get('Summary'),
        'CategoryNames': data.get('CategoryNames'),
        'Nationality': extracted.nationality,
        'Mission': extracted.mission,
        'Activities': extracted.activities
    }

    current_section = None
    return formatted

def main():
    with open('data/clean.json', 'r') as json_file:
        cleaned_data = json.load(json_file)

    client = OpenAI(
        api_key=os.getenv("OPEN_AI_API_KEY")
    )
    contextual_data = []
    for item in cleaned_data:
        contextual_data.append(extract_contextual_data(client, item))
        with open('data/contextual_data.json', 'w') as json_file:
            json.dump(contextual_data, json_file, indent=4)
    
    contextual_dict = {}
    for item in contextual_data:
        contextual_dict[item['Name']] = item
    with open('data/contextual_dict.json', 'w') as json_file:
        json.dump(contextual_dict, json_file, indent=4)

if __name__ == "__main__":
    main()
