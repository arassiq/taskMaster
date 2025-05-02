import os
from dotenv import load_dotenv
from openai import OpenAI
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class AIbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAIAPIKEY"),  # This is the default and can be omitted
        )

    def gptCompletion(self):
        self.completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system", "content": """You are a productivity-focused LLM. Your job is to help users organize, prioritize, and complete their tasks effectively. Break down tasks into clear and actionable steps and prioritize them based on urgency and importance. Ensure that the output is in a structured, subscriptable format so the user can easily separate the task list and the explanations. 

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
                    "role": "user", "content": " I have a paper due in 2 weeks pertaining to the ceasefire in gaza, as well as a CS project due in 3 weeks where i have to create my own file system. "
                },
            ],
            model="gpt-4o",
        )
        self.gptOutput = self.completion.choices[0].message.content

        return self.gptOutput


    def main(self):
        split_output = re.split(r"Notes:\s*", self.gptCompletion(), maxsplit=1)

        # Store tasks and notes separately
        tasks = split_output[0].strip()  # Everything before "Notes:"
        notes = split_output[1].strip() if len(split_output) > 1 else ""  # Everything after "Notes:"

        # Print the results
        print("Tasks:")
        print(tasks)
        print("\nNotes:")
        print(notes)
    
if __name__ == "__main__":
    AIbot = AIbot()
    AIbot.main()