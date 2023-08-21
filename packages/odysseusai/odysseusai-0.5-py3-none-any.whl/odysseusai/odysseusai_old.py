def say_hello():
    print("Hello, World!")

import os
import json
from datetime import datetime
import uuid
import openai

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=2000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

def evaluate_chatbot_response(messages, response, open_ai_key):
    openai.api_key = open_ai_key
    system_message_content = messages[0]['content']
    conversation = messages[1:-1]
    last_prompt = messages[-1]['content']

    system_message = f""" 
        You are an expert in evaluating whether a chatbot has responded to a user's prompt as expected.
        You will receive a system message that defines the chatbot's behavior, 
        any previous conversations between the chatbot and users (if available), 
        and the user's prompt along with the chatbot's response that you need to evaluate.
        Your objective is to assign a probability to the correctness of the chatbot's response and to provide a concise justification. 
        Please return a JSON object in the following format:
        "probability": probability, "justification": justification.
    """

    user_message = f"""
        Let's think step by step.
        1. You receive the following 
        system message: {system_message_content}.
        previous conversation: {conversation}
        user's prompt: {last_prompt}
        chatbot's response: {response}
        2. You assign a probability score 'probability' to the correctness of chatbot's response to user's prompt based on previous conversation and system message. 
        3. You craft a concise justification 'justification' for the assignemnet 
        4. Return a JSON object in the following format "probability": 'probability', "justification": 'justification'.
    """
    message = [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': user_message}]

    openai_response = get_completion_from_messages(message)
    return(openai_response)

def create_env(project_dir, prompt, model):
    os.makedirs(project_dir)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    env_info_dir = f'{project_dir}/env_info.json'
    with open(env_info_dir, 'w') as f:
        json.dump({
            'prompt': prompt,
            'model': model,
            'timestamp': str(current_time)
        }, f, indent=4)
    


def init(project_name, prompt, model, tracking_dir = ''):
    tracking_dest = f'{tracking_dir}data_tracking'
    if not os.path.exists(tracking_dest):
        os.makedirs(tracking_dest)
    project_dir = f'{tracking_dir}data_tracking/{project_name}'
    if not os.path.exists(project_dir):
        create_env(project_dir, prompt, model)
    

def log(project_name, input_llm, output_llm, tracking_dir = '', user_id='', session_id='', auto_failure = False,  manual_labeling ='', open_ai_key =''):
    unique_str = str(uuid.uuid4())
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    if(auto_failure):
        failure_response = json.loads(evaluate_chatbot_response(input_llm, output_llm, open_ai_key))

        print(failure_response)
        prob_failure = failure_response['probability']
        justification = failure_response['justification']
    else:
        prob_failure = ''
        justification = ''
    project_dir = f'{tracking_dir}data_tracking/{project_name}/{unique_str}.json'
    with open(project_dir, 'w') as f:
        json.dump({
            'user_id': user_id,
            'session_id': session_id,
            'timestamp': str(current_time),
            'input_llm': input_llm,
            'output_llm': output_llm,
            'prob_failure': prob_failure,
            'justification': justification,
            'manual_labeling': manual_labeling
        }, f, indent=4)

   
    

