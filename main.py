import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv()

client = openai.OpenAI()

model = "gpt-4o"

engineering_assistant = client.beta.assistants.create(
  name="Engineering Assistant",
  instructions="You are a senior AI engineer, you are here to help a senior engineer develop AI features into web applications. Advise on the best practises and most up to date tools to use.",
  tools=[{"type": "code_interpreter"}],
  model=model
)

print(engineering_assistant.id)

thread = client.beta.threads.create(
  messages=[{
    "role": "user",
    "content": "How do I implement a personalised AI assistant on my website?"
  }]
)

print(thread.id)