import requests
import base64
import os
from langchain_ollama import ChatOllama
from pathlib import Path

from PIL import Image

def read_images(p):
    path_obj = Path(p)
    image_urls = []
    encoded_images = []
    no = 0
    for file_path in path_obj.iterdir():
        if file_path.is_file():
            no += 1
            file = f'image_{no}'
            image_urls.append(file)

            raw_bytes = file_path.read_bytes()
            b64_bytes = base64.b64encode(raw_bytes).decode('utf-8')
            encoded_images.append(b64_bytes)

    return image_urls, encoded_images

x = read_images('examples')

def llm_model(id, temp):
    model = ChatOllama(
        model = id,
        temperature = temp,
    )
    return model

llm = llm_model('qwen3-vl:30b', 0)

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

    # create the message object
    message = [
        {
            "role": "user",
            "content":[
                {
                "type":"text",
                "text": assistant_prompt + user_query,
                },
                {
            "type":"image_url",
            "image_url":{
                "url": "data:image/jpeg;base64,"+ encoded_image,
            }
        }
            ]
        },
        
    ]

    # send request to the model
    response = llm.invoke(message)

    return response.content


user_query = "Describe the photo"
encoded_images = x[1]

for i in range(len(encoded_images)):
    image = encoded_images[i]

    response = generate_model_response(image, user_query)

    print(f'Description for image {i + 1}: {response}')
