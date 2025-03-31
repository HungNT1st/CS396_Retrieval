import json

def load_data(data_path, embedded_path):
    with open(data_path, 'r') as f:
        data_data = json.load(f)
    
    with open(embedded_path, 'r') as f:
        embedded_data = json.load(f)
    
    return data_data, embedded_data

def merge_data(data_data, embedded_data):
    merged_data = []
    for data_item, embedded_item in zip(data_data, embedded_data):
        merged_data.append({
            "metadata": data_item,
            "embedding": embedded_item
        })
    return merged_data

if __name__ == "__main__":
    data_data, embedded_data = load_data('data/contextual_data.json', 'data/weighted_embedded_contextual_data.json')
    merged_data = merge_data(data_data, embedded_data)
    with open('data/merged_data.json', 'w') as f:
        json.dump(merged_data, f, indent=4)
