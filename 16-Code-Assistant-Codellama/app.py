import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

history=[]

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)
    data = {
        "model": "codeguru",
        "prompt": final_prompt,
        "stream": False,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.text
        data = json.loads(response_json)
        actual_response = data['response']
        return actual_response
    else:
        print("Error:", response.status_code, response.text)


interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, label="Enter your prompt"),
    outputs="text"
)

interface.launch();