import openai
import pinecone
import os

# Set the OpenAI API key
openai.api_key = os.environ["OPENAI"]
# set up pinecone
pinecone.init(api_key=os.environ["PINECONE"], environment="us-west4-gcp-free")

query = "Hello"

# Generate text embeddings using OpenAI

res = openai.Embedding.create(input=[query], engine="text-embedding-ada-002")


# retrieve from pinecone
index = pinecone.Index("mojave")

xq = res["data"][0]["embedding"]

# get relevant context
res = index.query(xq, top_k=5, include_metadata=True)

# contexts

contexts = [item["metadata"]["text"] for item in res["matches"]]

augmented_query = "\n\n---\n\n".join(contexts) + "\n\n---\n\n" + query

print(augmented_query)
