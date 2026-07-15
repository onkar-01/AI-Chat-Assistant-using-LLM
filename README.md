# AI-Chat-Assistant

A terminal-based AI chat assistant built in Python. This application allows you to have a continuous interactive conversation with an AI model directly from your command line. 

Currently, it uses the **Xiaomi MiMo API** (`mimo-v2.5-pro` model) via the official OpenAI Python SDK, leveraging its OpenAI-compatible endpoint.

## Features
- **Interactive Continuous Chat:** Keep chatting with the AI in an endless loop until you decide to leave.
- **Object-Oriented Design:** Clean, modular, and maintainable `Aichatapp` class structure.
- **"Thinking" Enabled:** Uses advanced model settings (`"thinking": {"type": "enable"}`) to allow the AI to reason deeply before responding.
- **Secure Key Management:** Uses `python-dotenv` to securely load API keys from a `.env` file instead of hardcoding them.

## Prerequisites
- Python 3.8+
- `pip` (Python package manager)

## Setup Instructions

1. **Open the project folder:**
   ```bash
   cd "AI-Chat-Assistant-using-LLM"
   ```

2. **Create a Virtual Environment (Recommended):**
   This keeps your project's dependencies isolated from your main system.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Copy the example `.env` file to create your own active `.env` file:
     ```bash
     cp .env.example .env
     ```
   - Open the newly created `.env` file in your text editor and replace `your mimo api key` with your actual Xiaomi MiMo API key:
     ```env
     MIMO_API_KEY=sk-your-actual-api-key-here
     ```

## Usage

1. **Run the application:**
   Make sure your virtual environment is active, then execute:
   ```bash
   python app.py
   ```

2. **Chat with the AI:**
   - Type your questions at the `Ask me anything: ` prompt and hit **Enter**.
   - The AI will process your request and respond directly in the terminal.

3. **Exit the Application:**
   - Type `exit` and hit **Enter** to break the chat loop and close the app.

## Project Structure
- `app.py`: The main application code containing the `Aichatapp` class and chat loop.
- `requirements.txt`: The list of Python dependencies required (like `openai` and `python-dotenv`).
- `.env.example`: The template for setting up environment variables.
- `basic.py`: Contains basic Python syntax examples (classes, functions, defaults) for reference.