# There are a few things we need to do go really understand the logic of the system.
# The human specifies what their learning goal is and how long they have to achieve it.
# The system then uses the goal to determine a schedule of subject for the human to learn in order to achive that goal.

# Lets start with the human specifying their learning goal.
# The human specifies their learning goal by answering the following questions:
# 1. What is your learning goal?
# 2. How long do you have to achieve your learning goal?
# 3. What is your current level of knowledge of the subject?

#  an input statmemt that asks the user to specify their learning goal

goal = input("What is your learning goal?")
time = input("How long do you have to achieve your learning goal?")

# Now er append the goal and time to the augmented query.

human_statement = f"""My learning goal is{goal}and I have{time}to achieve it."""
print(human_statement)

# Now we have to pass the human input into the model to the system.

# we need to import the openai library and the os library

import openai
import os

# initialize the openai

# Set the OpenAI API key
openai.api_key = os.environ["OPENAI"]

# system message to prime the model
primer = f"""You are Q&A bot. A highly intelligent system that answers human questions based on the information provded by the user above each question.
If the information can not be found in the information provided by the user, come up with a plausible answer.
"""

res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k-0613",
    messages=[
        {"role": "system", "content": primer},
        {"role": "user", "content": human_statement},
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)
