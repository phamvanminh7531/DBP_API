import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)

import json
import urllib.request
import urllib.parse
import requests
from workflow.workflow_path import WORKFLOW_DIR
import random
from io import BytesIO
import io
from PIL import Image
import base64

LOAD_BALANCER = {
    "Server_1" : {
        "host_name": "192.168.1.49:8188",
        "count": 0
    },
    "Server_2" : {
        "host_name": "192.168.1.50:8188",
        "count": 0
    }
}

# server_address = "192.168.1.49:8188"



with open(WORKFLOW_DIR, "r", encoding="utf-8") as f:
    workflow_data = f.read()

workflow = json.loads(workflow_data)

def queue_prompt(prompt, client_id, server_address):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type, server_address):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id, server_address):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

# def get_images(ws, prompt, client_id, server_address):
#     prompt_id = queue_prompt(prompt, client_id, server_address)['prompt_id']
#     output_images = {}
#     while True:
#         out = ws.recv()
#         if isinstance(out, str):
#             message = json.loads(out)
#             if message['type'] == 'executing':
#                 data = message['data']
#                 if data['node'] is None and data['prompt_id'] == prompt_id:
#                     break #Execution is done
#         else:
#             continue #previews are binary data

#     history = get_history(prompt_id, server_address)[prompt_id]
#     for o in history['outputs']:
#         for node_id in history['outputs']:
#             node_output = history['outputs'][node_id]
#             if 'images' in node_output:
#                 images_output = []
#                 for image in node_output['images']:
#                     image_data = get_image(image['filename'], image['subfolder'], image['type'], server_address)
#                     images_output.append(image_data)
#             output_images[node_id] = images_output
#     return output_images

def get_images(ws, prompt, client_id, server_address):
    prompt_id = queue_prompt(prompt, client_id, server_address)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break  # Execution is done
        else:
            continue  # Previews are binary data

    history = get_history(prompt_id, server_address)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
            images_output = []
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'], server_address)
                images_output.append(image_data)
            output_images[node_id] = images_output  # Assign to `output_images`
        else:
            # Initialize `output_images[node_id]` to an empty list if no images are found
            output_images[node_id] = []
    return output_images

def upload_file(file, subfolder="", overwrite=False):
    try:
        # Wrap file in formdata so it includes filename
        body = {"image": file}
        data = {}
        
        if overwrite:
            data["overwrite"] = "true"
  
        if subfolder:
            data["subfolder"] = subfolder

        resp = requests.post(f"http://{server_address}/upload/image", files=body,data=data)
        
        if resp.status_code == 200:
            data = resp.json()
            # Add the file to the dropdown list and update the widget value
            path = data["name"]
            if "subfolder" in data:
                if data["subfolder"] != "":
                    path = data["subfolder"] + "/" + path
            

        else:
            print(f"{resp.status_code} - {resp.reason}")
    except Exception as error:
        print(error)
    return path

def get_IMG2IMG_result(img_3d_input_path, img_style_input_path, client_id, server_address, promt_text=None):
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))


    workflow["173"]["inputs"]["noise_seed"] = random.randint(1,9999999999999999)

    # set the image name for our LoadImage node
    workflow["659"]["inputs"]["image"] = img_3d_input_path

    # set the image name for our LoadImage node
    workflow["660"]["inputs"]["image"] = img_style_input_path

    workflow["203"]["inputs"]["text"] = ''
    if promt_text:
        workflow["203"]["inputs"]["text"] = promt_text
    
    print(workflow["203"]["inputs"]["text"])

    images = get_images(ws, workflow, client_id, server_address)
    # print(type(images))
    # print(images["181"])
    # for key, value in images["181"].iteritems():
    #     print(key)
    #     print('-'*8)
    ws.close()
    return images["181"][-1]

    for node_id in images:
        print(node_id)
        # for image_data in images[node_id]:
        #     from PIL import Image
        #     import io
        #     image = Image.open(io.BytesIO(image_data))
        #     # return image_data
        #     # image.show()
        #     # print(image)
        #     # save image
        #     image.save(f"{node_id}-.png")

def test_IMG2IMG(img_3d_input_url, img_style_input_url, client_id, server_address, promt_text=None):
    print(LOAD_BALANCER)
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    


    workflow["173"]["inputs"]["noise_seed"] = random.randint(1,9999999999999999)

    # set the image name for our LoadImage node
    workflow["659"]["inputs"]["image"] = img_3d_input_url

    # set the image name for our LoadImage node
    workflow["660"]["inputs"]["image"] = img_style_input_url

    workflow["203"]["inputs"]["text"] = ''
    if promt_text:
        workflow["203"]["inputs"]["text"] = promt_text
    
    images = get_images(ws, workflow, client_id, server_address)
    # print(type(images))
    # print(images["181"])
    # for key, value in images["181"].iteritems():
    #     print(key)
    #     print('-'*8)
    ws.close()
    return images["181"][-1]


def image_base64_encode(image_data):
    """
    This function return base64 image data from image data of response from AI Gen Module    
    """
    image = Image.open(io.BytesIO(image_data))
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    return base64.b64encode(img_io.read()).decode('utf-8')