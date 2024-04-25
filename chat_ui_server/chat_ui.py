import chainlit as cl
import requests
import time

base_url = "http://127.0.0.1:5000"

@cl.on_message
async def main(message: cl.Message):
    files = None
    
    while files is None:
        files = await cl.AskFileMessage(content="Please upload a text file containing links to call logs!", accept=["text/plain"], max_size_mb=20, timeout=180,).send()
    
    data = {'question': message.content, 'documents': open(files[0].path, "r", encoding="utf-8").read().splitlines()}
    
    response = requests.post(f"{base_url}/submit_question_and_documents", json=data)    
    if response.status_code == 200:
        get_response = requests.get(f"{base_url}/get_question_and_facts")
        
        if get_response.status_code == 200:
            get_data = get_response.json()
            tries = 0
            while True:
                await cl.Message(content="Your Request is being Processed, Give it a few seconds").send()
                tries += 1
                print('retrying')
                
                get_response = requests.get(f"{base_url}/get_question_and_facts")
                if get_response.status_code == 200:
                    get_data = get_response.json()
                    print(get_data)
                    if (get_data['status'] == 'done') or tries >= 3:
                        break
                else:
                    print(get_response)
                    break
                time.sleep(15)
        
            if get_data['status'] == 'processing':
                await cl.Message(content="Error: max tries reached, please try after some time").send()
            elif get_data['status'] == 'done':
                facts = "\n- ".join(get_data['facts'])
                await cl.Message(content=f"Here are the Facts:\n {facts}").send()
        else:
            print('failed')
            await cl.Message(content=f"Some error occured: \nPlease try again later").send()