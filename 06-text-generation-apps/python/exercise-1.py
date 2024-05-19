from openai import AzureOpenAI
import dotenv
import os

dotenv.load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv('AZURE_API_KEY'),
    api_version = "2023-05-15"
  )

deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')

system_prompt = "You are a Application security specialist. Your job is to suplement the user with Application Security information only, nothing else."

appsec_question = input(f'\nHey what do you need to know now? ')
user_prompt = f'Q: {appsec_question} \nA:'
messages = [
    {
        "role": "system",
        "content": f'{system_prompt}'
    },
    {
        "role": "user",
        "content": f'{user_prompt}'
    }
]

completion = client.chat.completions.create(model=deployment, messages=messages)
print(f'\n ######### \n {completion.choices[0].message.content} \n ######### \n')