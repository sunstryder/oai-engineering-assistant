import openai
from dotenv import load_dotenv, find_dotenv
import time
import logging
from datetime import datetime

load_dotenv()

client = openai.OpenAI()

model = "gpt-4o"

# # Create an assistant:
# engineering_assistant = client.beta.assistants.create(
#   name="Engineering Assistant",
#   instructions="You are a senior AI engineer, you are here to help a senior engineer develop AI features into web applications. Advise on the best practises and most up to date tools to use.",
#   tools=[{"type": "code_interpreter"}],
#   model=model
# )

# print(engineering_assistant.id)

# # Create a thread with the assistant:
# thread = client.beta.threads.create(
#   messages=[{
#     "role": "user",
#     "content": "How do I implement a personalised AI assistant on my website?"
#   }]
# )

# print(thread.id)

# Hardcode the Assistant and thread IDs as to not recreate them.
assistant_id="asst_xepODBpgvqxFiST0eg5ssRP0"
thread_id="thread_LD4hi7C4krYclctFCirtuxgP"

message= "Give me some example AI applications, using the Assistants API from OpenAI that I can use to build a personalised AI assistant on my website."

# Adds a message to the thread:
message = client.beta.threads.messages.create(
  thread_id=thread_id,
  role="user",
  content=message
)

# Run the thread:
run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id,
  instructions="Please address user as Mr Bond"
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
  
  while True:
    try:
      run =client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
      if run.completed_at:
        elapsed_time = run.completed_at - run.created_at
        formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(f"Run completed in {formatted_elapsed_time}")
        logging.info(f"Run completed in {formatted_elapsed_time}")
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        print(f"Assistant Response: {response}")
        break
    except Exception as e:
      logging.error(f"An error occurred while retrieving the run: {e}")
      break
    logging.info("Waiting for run to complete...")
    time.sleep(sleep_interval)
    
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread_id,
  run_id=run.id
)

print(run_steps.data[0])