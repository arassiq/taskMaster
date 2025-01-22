import os
from dotenv import load_dotenv
from openai import OpenAI
import re
from flask import Flask, render_template, request, jsonify, Response

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

                        Provide the output with a strict separation between 'Tasks:' and 'Notes:'. Ensure all Output tasks in a structured format, like a JSON object., and any unrelated text is only added to the 'Notes:' section prefixed by 'Notes:'.

                        Output tasks in the following format:
                        1. [Main Task 1]
                        a. [Subtask 1 for Main Task 1]
                        b. [Subtask 2 for Main Task 1]
                        2. [Main Task 2]
                        a. [Subtask 1 for Main Task 2]
                        b. [Subtask 2 for Main Task 2]

                        Provide any additional information or guidance in a conversational style (not in a bulleted list) in a separate section labeled 'Notes' below the task list. This ensures the task list and guidance are easily distinguishable for further processing.
                        
                        Anything that is not apart of the task list, add in the notes section, such as greetings, plaintext. If it is not in task format, do not add it to tasks.

                        Make sure that you keep it concise in the notes section, and ask a good amount of questions
                        """
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
        tasks_raw = split_output[0].strip()  # Everything before "Notes:"
        notes = split_output[1].strip() if len(split_output) > 1 else "No additional notes provided."

        # Parse tasks into structured format (mock example for explanation)
        tasks = []
        for line in tasks_raw.split('\n'):
            if line.strip().startswith("1.") or line.strip().startswith("2."):
                tasks.append({"main_task": line.strip(), "subtasks": []})
            elif line.strip().startswith("a.") or line.strip().startswith("b."):
                if tasks:
                    tasks[-1]["subtasks"].append(line.strip())

        print(f"notes: {notes}")
        print(f"tasks: {tasks}")

        return {"tasks": tasks, "notes": notes}

# Initialize the AIbot instance
ai_bot = AIbot()

jsonFormat= {
        username: userName,

        







    }

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML frontend file

user_input_list = []

@app.route('/send_name', methods=['POST'])
def retrieveUserChats():
    userName = get_name()
    print(userName)

def get_name():
    request.json.get('name')
    return Response(status=204)


@app.route('/get_response', methods=['POST'])
def get_response():
    global user_input_list  # Use the global variable to persist memory

    # Get user input from the request
    user_input = request.json.get('user_input', '').strip()
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    # Append the new input to the user input list
    user_input_list.append(user_input)

    # Combine all inputs into a conversation string
    conversation = "\n".join(user_input_list)

    # Pass the conversation to the AI bot
    result = ai_bot.gptCompletion(conversation)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)