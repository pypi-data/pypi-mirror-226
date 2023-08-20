import openai
import os
from IPython.display import markdown


# Set the OpenAI API key
openai.api_key = os.environ["OPENAI"]

# system message to prime the model
primer = f"""You are Q&A bot. A highly intelligent system that answers human questions based on the information provded by the human above each question.
If the information can not be found in the information provided by the user, you truthfully say "I dont know". 
"""

res = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": primer},
        {"role": "user", "content": "augmented_query"},
    ],
)

display(markdown(res["choices"][0]["messages"]["content"]))
