import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

# OpenAI API Key
# client = OpenAI()
load_dotenv()
# Function to encode the image
def encode_image(image_path):
   return base64.b64encode(image_path.getvalue()).decode('utf-8') 
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')


def process_image_with_gpt4vision_streamlit(image_path):
  # Getting the base64 string
  base64_image = encode_image(image_path)
  api_key=os.environ["OPENAI_API_KEY"]
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
  

  template = """
      Objective: The objective is to classify the quality of the image in to High, medium and low. Please see below instructions on how to classify it and also output format:
      
      Instructions:
      
      
        1.Low:

            1.1 Look for images that have visible distortions, artifacts, or pixelation.
            1.2 Check for blurry or out-of-focus images.
            1.3 Identify images with poor lighting or exposure.
            1.4 Consider images with low resolution.

        2.Medium:

            2.1 Look for images that are reasonably clear and well-defined.
            2.2 Check for minor imperfections or noise that do not significantly impact the overall quality.
            2.3 Consider images with average lighting and exposure.
            2.4 Identify images with moderate resolution and file size.

        3.High:

            3.1 Look for images that are sharp, clear, and well-defined.
            3.2 Check for minimal or no imperfections, noise, or artifacts.
            3.3 Consider images with excellent lighting and exposure.
            3.4 Identify images with high resolution and large file size.
            
        4.Unknown:
            4.1 Dont make any assumptions. if you can't classify then categorize it as Unknown. 
      
      Output Format: 
        It should be JSON with no additional text as per below format.
      
              {"Low":<BooleanValue>,
              "Medium":<BooleanValue>,
              "High":<BooleanValue>,
              "Unknown":<BooleanValue>}
              
              In above JSON format replace the <BooleanValue> with True or False based on the instructions
            
  
      
      """

  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": template
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 4096
  }

  # response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  retry_attempts=3
  attempt = 0
  while attempt < retry_attempts:
      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
      
      if response.status_code == 200:
          response_json = response.json()
          content = response_json['choices'][0]['message']['content']
          
          # Check if the response content suggests it's not helpful
          unhelpful_phrases = ["I'm sorry, but I cannot assist",
                               "I cannot assist with that request.",
                               "I'm sorry, but I can't assist with that request.",
                               "I'm sorry, but I am unable to provide information extracted from documents or images that contain sensitive data",
                               "However, due to restrictions, I cannot process the content of documents",
                               "I'm sorry, but I can't assist with this request"]    # , "unable to process", "cannot be processed"]
          if any(phrase in content for phrase in unhelpful_phrases):
              print(f"Attempt {attempt + 1} failed with unhelpful response, retrying...")
              attempt += 1
              continue
          print(f"GPT4 Vision Response- {content}")
          return content
      else:
          print(f"Error: {response.status_code}")
          print(f"Response content: {response.content.decode()}")
          return {"Error": response.status_code, "Response content": response.content.decode()}
      
      attempt += 1  # Increment attempt counter if not successful

  return "Max retry attempts reached. The API could not process the request as expected."

# Path to your image

# response =process_image_with_gpt4vision("ScannedSampleDocs/page_2.png")
# print (response)