import json
from bs4 import BeautifulSoup
import re

def clean_html(raw_html):
    if raw_html is None:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def remove_newlines_and_links(text):
    if text is None:
        return ""
    text = text.replace('\n', ' ')
    text = re.sub(r'http\S+', '', text)
    return text

def format_docs_data(docs_list):
    formatted_docs = []
    for doc in docs_list:
        formatted_docs.append(f'***{doc["Name"]}***: {doc["Data"]}')
    return ' '.join(formatted_docs)

def get_first_doc(docs_list):
    for doc in docs_list:
        if doc.get('Data', '').strip():
            return doc.get('Data')
    return ''

def main():
    with open('data/organizations.json', 'r') as json_file:
        org_data = json.load(json_file)

    with open('data/documents.json', 'r') as json_file:
        doc_data = json.load(json_file)
    
    cleaned_data = [
        {
            'Name': item.get('Name'),
            'Description': remove_newlines_and_links(clean_html(item.get('Description', ''))),
            'Summary': remove_newlines_and_links(item.get('Summary')), # Should also remove all N/A and TBA in this field
            'CategoryNames': item.get('CategoryNames'),
            # 'Documents': remove_newlines_and_links(format_docs_data(doc.get('DocsList'))),
            'Documents': remove_newlines_and_links(get_first_doc(doc.get('DocsList')))
        }
        for item, doc in zip(org_data, doc_data)
    ]
    
    with open('data/clean.json', 'w') as json_file:
        json.dump(cleaned_data, json_file, indent=4)

    cleaned_dict = {}
    for item in cleaned_data:
        cleaned_dict[item['Name']] = item
    with open('data/clean_dict.json', 'w') as json_file:
        json.dump(cleaned_dict, json_file, indent=4)

if __name__ == "__main__":
    main()
    with open("data/clean.json", 'r') as json_file:
        data = json.load(json_file)
    print(len(data))