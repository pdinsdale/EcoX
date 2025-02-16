from flask import Blueprint
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import base64
import PIL.Image
import json

instructions = """
   Given an image, detect the object in the image. Then, give a breakdown of the environmental impact the item has in the process of manufacturing.
   Then, if the item has a current environmental impact, describe this as well. Keep descriptions informative but not too lengthy. 
   Then, provide alternatives users can use if they don't want to use the current item because of the impact it has on the environment. 
   Take into consideration the brands if detected, as brands can source materials and ingredients in ways that are negative to the environment. 
   For the alternatives, provide links to alternatives so user can click and learn more. The alternatives must be either an alternative product from a different company, or a way for the user to make themselves at home.
   Output info as a JSON, for any unknown information, put N/A:
   {
   "item": "string",
   "impact": [] (list of impacts as strings),
   "current_impact": [] (list of current impacts as strings, if applicable. Not everything may have a current impact),
   "alternatives": [] (list of alternatives split by name, company, logo of company (as PNG or JPEG ONLY), a brief description why it is a better alternative, and link to website)
   }
   """

load_dotenv()
gemini = os.getenv("GEMINI")
client = genai.Client(api_key=gemini)

def getImageData(image):
   openedImage = PIL.Image.open(image)
   
   response = client.models.generate_content(
      # model='gemini-2.0-pro-exp-02-05',
      model='gemini-2.0-flash-lite-preview-02-05',
      contents=[openedImage],
      config=types.GenerateContentConfig(
         system_instruction=instructions
      ),
   )

   try:   
      data = json.loads(response.text.strip("```json\n").strip("```"))
      return data
   except json.JSONDecodeError:
      print("Error: failed json")
      return None