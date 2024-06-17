import pathlib
import textwrap
# Used to securely store your API key
from google.colab import userdata

import google.generativeai as genai


from IPython.display import display
from IPython.display import Markdown

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY=userdata.get('AIzaSyC-N8pmMCpJ_pcjJ8UfaPj24rZjXBM6nk4')

genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
  
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)