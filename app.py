import os

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from openai import OpenAI

load_dotenv()


class Aichatapp:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("MIMO_API_KEY"),
            base_url="https://api.xiaomimimo.com/v1"
        )
    
    def ask_ai(self,question):
        completion = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_completion_tokens=1024,
            stream=False,
            extra_body={
                "thinking": {"type": "enable"}
            }
        )
        return completion.choices[0].message.content
    
    def chat(self):
        while True:
            question= input("Ask me anything: ")
            if question == "exit":
                break
            else:
                ans= self.ask_ai(question)
                print(ans)

chat = Aichatapp()
chat.chat()