import requests
import base64
import os
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model, ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames

from PIL import Image

credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                   # api_key = "<YOUR_API_KEY>" # Normally you'd put an API key here, but we've got you covered here
                  )
client = APIClient(credentials)

url_image_1 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/5uo16pKhdB1f2Vz7H8Utkg/image-1.png'
url_image_2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/fsuegY1q_OxKIxNhf6zeYg/image-2.png'
url_image_3 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/KCh_pM9BVWq_ZdzIBIA9Fw/image-3.png'
url_image_4 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/VaaYLw52RaykwrE3jpFv7g/image-4.png'

"""
or Images from Dir
url_image_1= 'DwnImg/image-1.png'
url_image_2= 'DwnImg/image-2.png'
url_image_3= 'DwnImg/image-3.png'
url_image_4= 'DwnImg/image-4.png'
"""

image_urls = [url_image_1, url_image_2, url_image_3, url_image_4] 

encoded_images = []

for url in image_urls: 
    encoded_images.append(base64.b64encode(requests.get(url).content).decode("utf-8"))

model_id = "meta-llama/llama-3-2-90b-vision-instruct"
project_id = "skills-network"
params = TextChatParameters()

model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id,
    params=params
)

def generate_model_response(encoded_image, user_query, assistant_prompt="You are a helpful assistant. Answer the following user query in 1 or 2 sentences: "):
    """
    Sends an image and a query to the model and retrieves the description or answer.

    Parameters:
    - encoded_image (str): Base64-encoded image string.
    - user_query (str): The user's question about the image.
    - assistant_prompt (str): Optional prompt to guide the model's response.

    Returns:
    - str: The model's response for the given image and query.
    """
    
    # Create the messages object
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": assistant_prompt + user_query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64," + encoded_image,
                    }
                }
            ]
        }
    ]
    
    # Send the request to the model
    response = model.chat(messages=messages)
    
    # Return the model's response
    return response['choices'][0]['message']['content']

user_query = "Describe the photo"

for i in range(len(encoded_images)):
    image = encoded_images[i]

    response = generate_model_response(image, user_query)

    # Print the response with a formatted description
    print(f"Description for image {i + 1}: {response}")

"""
user_query = "Describe the photo"

for i in range(len(encoded_images)):
    image = encoded_images[i]

    response = generate_model_response(image, user_query)

    # Print the response with a formatted description
    print(f"Description for image {i + 1}: {response}")

# ---------------------------------------------------------------- #

Answer::

Description for image 1: The photo depicts a bustling city street, with towering buildings and a busy road filled with cars, taxis, and pedestrians. The scene is set against a backdrop of a cloudy sky, adding to the urban atmosphere.
Description for image 2: The image depicts a woman jogging on a road, wearing a yellow hoodie and black leggings. The background features a large white building with a parking lot and a black car.
Description for image 3: The image shows a flooded farm with several buildings and structures surrounded by water. The floodwaters have risen to the level of the buildings, with some partially submerged.
Description for image 4: The image depicts a close-up of a nutrition label, with a finger pointing to the "Total Carbohydrate" section. The label is white with black text and features a purple border, set against a dark gray background.

"""