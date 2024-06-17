"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import google.generativeai as genai

# Set the API key (replace with your actual API key)
os.environ['GOOGLE_API_KEY'] = "AIzaSyC-N8pmMCpJ_pcjJ8UfaPj24rZjXBM6nk4"

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1.9,
  "top_p": 0.95,
  "top_k": 50,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def generate_prompt(user_input):
  # Implement logic to generate prompt based on user_input
  # This example uses a simple template approach, replace with your logic
  keywords = user_input.split()

  if keywords[0] == "summarize":
    prompt = f"Summarize the following article in 3 sentences: "
  elif keywords[0] == "translate":
    prompt = f"Translate the following sentence to French: "
  else:
    prompt = "create a prompt for me so that i can feed it into any text based or image based llm to generate a high quality and efficient output."  # Default prompt

  prompt += " ".join(keywords[1:])
  return prompt

# User Input
user_input = input("Enter your prompt or subject: ")

prompt = generate_prompt(user_input)

chat_session = model.start_chat(
  history=[
  ]
)

# Send the generated prompt as the message
response = chat_session.send_message(prompt)

print(response.text)

