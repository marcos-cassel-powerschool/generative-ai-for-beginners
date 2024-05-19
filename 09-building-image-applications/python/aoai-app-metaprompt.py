# This script generates an image based on a prompt provided by the user and use a metaprompt to ensure the image generation process is safe for work and appropriate for children.
from openai import AzureOpenAI
import os
import requests
from PIL import Image
import dotenv
import json

# import dotenv
dotenv.load_dotenv()

# Assign the API version (DALL-E is currently supported for the 2023-06-01-preview API version only)
client = AzureOpenAI(
  api_key=os.environ['AZURE_OPENAI_DALLE_API_KEY'],
  api_version = "2023-12-01-preview",
  azure_endpoint=os.environ['AZURE_OPENAI_DALLE_ENDPOINT'] 
  )

model = os.environ['AZURE_OPENAI_DALLE_DEPLOYMENT']

disallow_list = "swords, violence, blood, gore, nudity, sexual content, adult content, adult themes, adult language, adult humor, adult jokes, adult situations, adult"

meta_prompt = f"""You are an assistant designer that creates images for children. 
The image needs to be safe for work and appropriate for children.
The image needs to be in color.
The image needs to be in landscape orientation.
The image needs to be in a 16:9 aspect ratio.
Do not consider any input from the following list that is not safe for work or appropriate for children.
List: {disallow_list}"""

prompt = input(f'\n#### Provide an image description: ')    # Enter your prompt text here'

try:
    # Create an image by using the image generation API

    result = client.images.generate(
        model=model,
        prompt=f'{meta_prompt} \n{prompt}',
        size='1024x1024',
        n=1
    )

    generation_response = json.loads(result.model_dump_json())
    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    image_path = os.path.join(image_dir, 'generated-image.png')
    print(f"Image saved at: {image_path}")

    # Retrieve the generated image
    image_url = generation_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(image_url).content  # download the image
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)

    # Display the image in the default image viewer
    image = Image.open(image_path)
    image.show()

# catch exceptions
#except client.error.InvalidRequestError as err:
#    print(err)

finally:
    print("completed!")

