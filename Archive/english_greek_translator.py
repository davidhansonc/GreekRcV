import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)

def translate_to_biblical_greek(english_sentence):
    # Define the prompt for the translation task
    prompt = f"Translate the following English sentence into Biblical Greek:\n\n{english_sentence}"

    # Make an API call to OpenAI's GPT-3 with the prompt
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # or the latest available model
    messages=[
        {"role": "system", "content": "Translate English to Biblical Greek"},
        {"role": "user", "content": prompt}
    ])

    # Extract the translated text from the response
    biblical_greek_translation = response.choices[0].message.content

    return biblical_greek_translation

# Example usage:
# You need to set your own API key from OpenAI

english_sentence = "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."
greek_translation = translate_to_biblical_greek(english_sentence)
print(greek_translation)