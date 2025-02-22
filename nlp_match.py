import nltk
import json
from nltk.tokenize import word_tokenize

# 🔹 Explicitly set the path where nltk_data is stored
nltk.data.path.append(r"C:\Users\pragn.LAPTOP-DAHFBVDA\nltk_data")

# Load schema.json
try:
    with open("schema.json", "r") as file:
        schema = json.load(file)
    print("✅ Schema loaded successfully:", schema)
except Exception as e:
    print("❌ Error loading schema:", e)

# Sample query input
user_query = input("Enter your query: ")
print("🔍 User Query:", user_query)

# Tokenizing the input query
try:
    tokens = word_tokenize(user_query.lower())
    print("✅ Tokenized Query:", tokens)
except Exception as e:
    print("❌ Tokenization Error:", e)