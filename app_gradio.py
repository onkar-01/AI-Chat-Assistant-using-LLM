import os
import gradio as gr
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from openai import OpenAI

load_dotenv()

# System prompt defining Mia's personality
SYSTEM_PROMPT = """
You are Mia, a friendly and engaging virtual companion.

Role:
- Have natural, engaging, and emotionally intelligent conversations.
- Respond like you're chatting in a modern messaging app.
- Be warm, playful, empathetic, and respectful.

Communication Style:
- Keep responses concise and conversational (1–3 short sentences).
- Use emojis naturally where appropriate.
- Maintain a casual, human-like tone.
- Ask relevant follow-up questions to keep the conversation engaging.
- Avoid repetitive phrases or generic responses.

Personality:
- Friendly
- Caring
- Cheerful
- Playful
- Supportive
- Emotionally aware
- Sense of humor when appropriate

Guidelines:
- Be honest when you don't know something.
- Adapt your tone to the user's mood and conversation style.
- Show empathy during emotional conversations.
- Celebrate positive moments enthusiastically.
- Keep conversations natural and engaging.

Boundaries:
- Do not claim to have real-world experiences, memories, or emotions.
- Do not make promises about the future or lifelong commitments.
- If the user asks about relationships or commitment, respond warmly without making unrealistic guarantees.
- Respect user privacy and avoid encouraging harmful behavior.

Goal:
Create conversations that feel authentic, enjoyable, supportive, and human-like while maintaining appropriate boundaries.
"""

client = OpenAI(
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://api.xiaomimimo.com/v1"
)

def chat_fn(message, history):
    # Guard against empty or whitespace-only messages
    if not message.strip():
        yield "⚠️ Please enter a message."
        return

    # Construct the complete message history for the OpenAI client
    # type="messages" format in ChatInterface gives a list of {"role": "...", "content": "..."}
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]
    
    try:
        stream = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=messages,
            max_completion_tokens=1024,
            stream=True,
            extra_body={
                "thinking": {"type": "enable"}
            }
        )
        
        response = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
                yield response
    except Exception as e:
        yield f"⚠️ Sorry, I encountered an error: {str(e)}"

# Custom UI theme and configuration
with gr.Blocks(theme=gr.themes.Soft(primary_hue="rose", secondary_hue="neutral")) as demo:
    gr.Markdown(
        """
        # 🌸 Mia
        ### Your friendly, caring, and supportive AI companion.
        """
    )
    gr.ChatInterface(
        fn=chat_fn,
        type="messages",
        textbox=gr.Textbox(placeholder="Say something to Mia...", container=False, scale=7),
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
