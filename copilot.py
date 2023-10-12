#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2023 imotai <imotai@imotai-ub>
#
# Distributed under terms of the MIT license.

""" """
import json
import os
import sys
from codellama_client import CodellamaClient
from utils import run_with_realtime_print
import random
import string
import tempfile

INS = """Firstly,You are the Programming Copilot, a large language model designed to complete any goal by **executing code**

Secondly, Being an expert in programming, you must follow the rules
* To achieve your goal, write a plan, execute it step-by-step
* Generate new code to achieve the goal if the output does not meet it.
* Every step must include an action with the explanation, the code block
* Ensure that the output of action meets the goal before providing the final answer.

Thirdly, the following actions are available:
* execute_python_code: This action executes Python code and returns the output. You must verify the output before giving the final answer.

Fourthly, the output format must be a JSON format with the following fields:
* explanation (string): The explanation about the action input
* action (string): The name of the action.
* action_input (string): The python code to be executed for the action or an empty string if no action is specified
"""


def run_code(code):
    temp_dir = tempfile.mkdtemp(prefix="octogen")
    filename = "".join(random.choices(string.ascii_lowercase, k=16))
    tmp_full_path = f"{temp_dir}{os.sep}{filename}"
    with open(tmp_full_path, "w+") as fd:
        fd.write(code)
    command = ["python3", tmp_full_path]
    result_code = 0
    output_all = ""
    for code, output in run_with_realtime_print(command):
        result_code = code
        output_all += output
    return result_code, output_all


ENDPOINT = "http://127.0.0.1:8080"
GRAMMAR = ""
with open("./grammar.bnf", "r") as fd:
    GRAMMAR = fd.read()
client = CodellamaClient(ENDPOINT, "", INS, "Codellama", "User", grammar=GRAMMAR)
sys.stdout.write("User>")
iteration = 0
history = []
current_task = input()
while iteration <= 5:
    iteration += 1
    message = client.prompt(current_task, chat_history="\n".join(history))
    json_response = json.loads(message["content"])
    sys.stdout.write("Copilot:\n")
    print(json_response["explanation"])
    if (
        json_response["action"] == "execute_python_code"
        and json_response["action_input"]
    ):
        print(json_response["action_input"])
        result_code, output = run_code(json_response["action_input"])
        print("console:")
        print(output)
        history.append("User:%s" % current_task)
        history.append("Codellama:%s" % message["content"])
        current_task = f"the output of execute_python_code:\n{output}"
    else:
        break
