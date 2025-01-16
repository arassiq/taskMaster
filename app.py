import os
from dotenv import load_dotenv
from openai import OpenAI
import re
from flask import Flask, render_template, request, jsonify

# Load environment variables
load_dotenv()

app = Flask(__name__)

class AIbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAIAPIKEY"),  # Set your OpenAI API key in .env
        )

    def gptCompletion(self, user_input):
        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": """You are a productivity-focused LLM. Your job is to help users organize, prioritize, and complete their tasks effectively. Break down tasks into clear and actionable steps and prioritize them based on urgency and importance. Ensure that the output is in a structured, subscriptable format so the user can easily separate the task list and the explanations. 

Output tasks in the following format:
1. [Main Task 1]
   a. [Subtask 1 for Main Task 1]
   b. [Subtask 2 for Main Task 1]
2. [Main Task 2]
   a. [Subtask 1 for Main Task 2]
   b. [Subtask 2 for Main Task 2]

Provide any additional information or guidance in a conversational style (not in a bulleted list) in a separate section labeled 'Notes' below the task list. This ensures the task list and guidance are easily distinguishable for further processing."""
                },
                { 
                    "role": "user", 
                    "content": user_input
                },
            ],
            model="gpt-4",
        )
        gpt_output = completion.choices[0].message.content

   # Attempt to split tasks and notes
        split_output = re.split(r"Notes:\s*", gpt_output, maxsplit=1)
        tasks = split_output[0].strip()  # Everything before "Notes:"
        notes = split_output[1].strip() if len(split_output) > 1 else "No additional notes provided."  # Handle missing Notes

        # Debugging
        print("Full GPT Output:", gpt_output)
        print("Tasks:", tasks)
        print("Notes:", notes)

        return {"tasks": tasks, "notes": notes}

# Initialize the AIbot instance
ai_bot = AIbot()

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML frontend file

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input', '')
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    # Get GPT completion results
    result = ai_bot.gptCompletion(user_input)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)