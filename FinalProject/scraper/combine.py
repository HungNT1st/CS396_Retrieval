import json

def clean_non_utf8(text):
    return text.encode('utf-8', 'ignore').decode('utf-8')

def combine_fields(item):
    parts = []
    for key, value in item.items():
        clean_value = clean_non_utf8(', '.join(value) if isinstance(value, list) else str(value))
        if clean_value:
            parts.append(f"{key.upper()}: {clean_value}")
    combined_text = ".".join(parts)
    return combined_text

def main():
    with open('data/clean.json', 'r') as json_file:
        data = json.load(json_file)
    
    combined_data = [combine_fields(item) for item in data]
    
    with open('data/combined.json', 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)

if __name__ == "__main__":
    main()
