
import json
import spacy
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

# Load database schema from JSON file
def load_schema(schema_file):
    with open(schema_file, "r") as file:
        return json.load(file)

# Load dataset (actual data from tables)
def load_dataset(dataset_file):
    with open(dataset_file, "r") as file:
        return json.load(file)

# Tokenization function using spaCy
def spacy_tokenizer(text):
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

# Find relevant tables based on tokenized query
def find_relevant_tables(user_query, schema):
    tokens = spacy_tokenizer(user_query)
    print(f"🔹 Extracted Tokens: {tokens}")  # Debugging

    matching_tables = {}

    for table_name, table_info in schema["tables"].items():
        match_score = sum(1 for col in table_info["columns"] if col.lower() in tokens)
        if match_score > 0:
            matching_tables[table_name] = match_score

    return sorted(matching_tables.items(), key=lambda x: x[1], reverse=True)

# Retrieve and filter weather data dynamically
def retrieve_weather_data(dataset, tokens):
    best_match = None
    best_score = 0

    today = datetime.today().strftime('%Y-%m-%d')
    print(f"debug:check dataset for best mathc..")
    print(f"tokens:{tokens}") # Get today's date

    for record in dataset:
        match_score = 0
        print(f"\n checking record: {json.dumps(record,indent=2)}")

        for key, value in record.items():
            value_str = str(value).lower()
            if key.lower() in tokens or value_str in tokens:
                match_score += 1
                print(f"match found:{key}-> {value}")

        # Give extra priority to today's date if the user asks about "today"
        if "today" in tokens and "date" in record and record["date"] == today:
            match_score += 2
            print(f" extra score for todays date:{record['date']}")

        if match_score > best_score:
            best_match = record
            best_score = match_score
    print(f"\n best match selected:{json.dumps(best_match,indent=2)}")
    return best_match

# Main function
if __name__ == "__main__":
    schema = load_schema("schema.json")
    dataset = load_dataset("weather.json")  # Load weather data

    print(f"✅ Schema loaded successfully: {json.dumps(schema, indent=2)}")

    user_query = input("Enter your query: ")
    print(f"🔍 User Query: {user_query}")

    result = find_relevant_tables(user_query, schema)

    if result:
        print("✅ Relevant Tables Found:")
        for table, score in result:
            print(f"   - {table} (Match Score: {score})")

            # Retrieve and display the *best matching weather data*
            best_match = retrieve_weather_data(dataset, spacy_tokenizer(user_query))

            if best_match:
                print(f"📊 Most Relevant Weather Data:")
                print(json.dumps(best_match, indent=2))
            else:
                print(f"❌ No matching weather data found.")

    else:
        print("❌ No relevant tables found.")