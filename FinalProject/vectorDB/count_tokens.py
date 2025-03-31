import json
import tiktoken

def count_tokens(text, model='text-embedding-3-large'):
    tokenizer = tiktoken.encoding_for_model(model)
    tokens = tokenizer.encode(text)
    return len(tokens)

def find_largest_token_item(data):
    max_tokens = 0
    max_item = None
    for item in data:
        item_tokens = count_tokens(item)
        if item_tokens > max_tokens:
            max_tokens = item_tokens
            max_item = item
    return max_item, max_tokens

def count_items_by_token_thresholds(data, thresholds):
    counts = {threshold: 0 for threshold in thresholds}
    for item in data:
        item_tokens = count_tokens(item)
        for threshold in thresholds:
            if item_tokens > threshold:
                counts[threshold] += 1
    return counts

def strip_to_tokens_limit(text, limit, model='text-embedding-3-large'):
    tokenizer = tiktoken.encoding_for_model(model)
    tokens = tokenizer.encode(text)
    return tokenizer.decode(tokens[:limit])

if __name__ == "__main__":
    with open('data/combined.json', 'r') as file:
        data = json.load(file)
    
    largest_item, largest_tokens = find_largest_token_item(data)
    # print(f"Largest item: {largest_item}")
    print(f"Number of tokens in the largest item: {largest_tokens}")
    
    thresholds = [800, 1200, 1500, 2000]
    counts = count_items_by_token_thresholds(data, thresholds)
    for threshold, count in counts.items():
        print(f"Number of items with more than {threshold} tokens: {count}")