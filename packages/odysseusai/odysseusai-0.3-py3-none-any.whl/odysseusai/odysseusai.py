def say_hello():
    print("Hello, World!")

import os
import json
from datetime import datetime
import uuid



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
    

def log(project_name, input_llm, output_llm, tracking_dir = '', user_id='', session_id='', auto_failure = False,  manual_labeling =''):
    unique_str = str(uuid.uuid4())
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    if(auto_failure):
        prob_failure = 'High'
    else:
        prob_failure = ''
    project_dir = f'{tracking_dir}data_tracking/{project_name}/{unique_str}.json'
    with open(project_dir, 'w') as f:
        json.dump({
            'user_id': user_id,
            'session_id': session_id,
            'timestamp': str(current_time),
            'input_llm': input_llm,
            'output_llm': output_llm,
            'prob_failure': prob_failure,
            'manual_labeling': manual_labeling
        }, f, indent=4)

   
    

#def log(user_message, output, user_id):

