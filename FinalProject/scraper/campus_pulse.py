import requests
import json
from io import BytesIO
from pdfminer.high_level import extract_text
import docx

API_URL = "https://umassamherst.campuslabs.com/engage/api/discovery/"
SEARCH_URL = API_URL + "search/organizations?orderBy%5B0%5D=UpperName%20asc&top=&filter=&query=&skip="
DOC_SUFFIX = "/document?isFolder=false&orderByField=id&orderByDirection=descending"
WEBSITE_URL = "https://umassamherst.campuslabs.com/engage/organization/"
FILE_SUFFIX = "/documents/view/"

def fetch_organizations(url):
	org_list = []
	fetched_list = []
	i = 0
	while not org_list or fetched_list:
		print("Fetch with skip =", i)
		org_list.extend(fetched_list)
		response = requests.get(url + str(i))
		response.raise_for_status()  # Raise an error for bad status codes
		data = response.json()
		fetched_list = data['value']
		i += len(fetched_list)
	return org_list

def fetch_docs_list(org_id):
	url = API_URL + "organization/" + org_id + DOC_SUFFIX
	response = requests.get(url)
	response.raise_for_status()  # Raise an error for bad status codes
	try:
		data = response.json()
		return data["items"]
	except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
		# print(f"Error fetching documents list: {e}")
		return []

def fetch_docs_data(org_key, docs_list):
	fetched_list = []
	for doc in docs_list:
		url = WEBSITE_URL + org_key + FILE_SUFFIX + str(doc["id"])
		print("Fetching file from URL: ", url)
		response = requests.get(url)
		response.raise_for_status()
		file_data = response.content
		file_name = doc["documentName"]
		try:
			if file_data[:4] == b'%PDF':
				text = extract_text(BytesIO(file_data))
				# print(text)
			else:
				document = docx.Document(BytesIO(file_data))
				# print(document)
				text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
			fetched_list.append({'Name': file_name, 'Data': text})
		except Exception as e:
			print(f"Error processing document {file_name}: {e}")
			continue
	return fetched_list

def main():
	org_list = fetch_organizations(SEARCH_URL)
	print("RSO Count: ", len(org_list))
	with open('data/organizations.json', 'w') as json_file:
		json.dump(org_list, json_file, indent=4)

	# Fetch documents
	org_docs_list = []
	with open('data/documents.json', 'r') as json_file:
		org_docs_list = json.load(json_file)
	for org in org_list:
		docs_list = fetch_docs_list(org["Id"])
		print(f"Fetching documents for {org['Name']} (ID: {org['Id']})")
		if not docs_list:
			print(f"No documents found for {org['Name']}")
		docs_data = fetch_docs_data(org["WebsiteKey"], docs_list)
		org_docs_list.append({'Name': org["Name"], 'DocsList': docs_data})
		with open('data/documents.json', 'w') as json_file:
			json.dump(org_docs_list, json_file, indent=4)

if __name__ == "__main__":
	main()