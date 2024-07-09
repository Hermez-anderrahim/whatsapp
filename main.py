# import json
# import logging
# import os
# from fastapi import FastAPI, HTTPException, Depends, Form, Request, requests , status , File, UploadFile , requests
# import aiohttp
# from fastapi.responses import RedirectResponse
# from pydantic import BaseModel
# import requests

# class BuyTicketRequest(BaseModel):
#     id: int


# app = FastAPI()

# # Load config from JSON file
# with open('config.json') as f:
#     config = json.load(f)

# # async def send_message(data):
# #     headers = {
# #         "Content-type": "application/json",
# #         "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
# #     }
# #     async with aiohttp.ClientSession() as session:
# #         url = f"https://graph.facebook.com/{config['VERSION']}/{config['PHONE_NUMBER_ID']}/messages"
# #         try:
# #             async with session.post(url, data=data, headers=headers) as response:
# #                 response_data = await response.json()  # Convert response to JSON if applicable

# #                 if response.status == 200:
# #                     logging.info(f"Message sent successfully. Response: {response_data}")
# #                 else:
# #                     logging.error(f"Failed to send message. Status: {response.status}. Response: {response_data}")
# #         except aiohttp.ClientConnectorError as e:
# #             logging.error(f'Connection Error: {str(e)}')
# #         # try:
# #         #     async with session.post(url, data=data, headers=headers) as response:
# #         #         if response.status == 200:
# #         #             print("Status hiiii:", response.status)
# #         #             print("Content-type:", response.headers['content-type'])

# #         #             html = await response.text()
# #         #             print("Body:", html)
# #         #         else:
# #         #             print(response.status)
# #         #             print(response)
# #         # except aiohttp.ClientConnectorError as e:
# #         #     print('Connection Error', str(e))

# # def get_text_message_input(recipient, text):
# #     return json.dumps({
# #         "messaging_product": "whatsapp",
# #         "preview_url": False,
# #         "recipient_type": "individual",
# #         "to": recipient,
# #         "type": "text",
# #         "text": {
# #             "body": text
# #         }
# #     })


# # def get_message_with_attachment(recipient , text):
# #     # Construct message JSON with attachment and text 
# #     message_data = {
# #         "messaging_product": "whatsapp",
# #         "to": recipient,
# #         "type": "document",
# #         "document": {
# #             "link": "https://docs.google.com/viewerng/viewer?url=https://www.learningcontainer.com/download/sample-pdf-file-for-testing/?ind%3D0%26filename%3Dsample-pdf-file.pdf%26wpdmdl%3D1566%26refresh%3D6688f1e61be411720250854%26open%3D1",
# #             "filename": "randompdf.pdf",
# #             "caption": text
# #     }
# #     }
# #     return json.dumps(message_data)

# # # Load config from JSON file
# # with open('config.json') as f:
# #     config = json.load(f)

# # async def send_request(url, method='POST', data=None):
# #     headers = {
# #         "Content-type": "application/json",
# #         "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
# #     }
# #     async with aiohttp.ClientSession() as session:
# #         try:
# #             async with session.request(method, url, json=data, headers=headers) as response:
# #                 return await response.json()
# #         except aiohttp.ClientConnectorError as e:
# #             logging.error(f'Connection Error: {str(e)}')
# #             return {"error": str(e)}
        



# # @app.post("/welcome")
# # async def welcome(text : str ,recipient_waid: str = Form(...)):
# #     data = get_text_message_input(recipient_waid, text)
# #     await send_message(data)
# #     return {"message": "Message sent successfully"}


# # @app.post("/sendAtachement")
# # async def buy_ticket(text: str = Form(...)):
# #     data = get_message_with_attachment(config['RECIPIENT_WAID'] ,  text)
# #     await send_message(data)
# #     return {"message": "Message sent successfully"}



# # @app.post("/webhook")
# # async def webhook(request: Request):
# #     try:
# #         data = request.json
# #         message = data.get('message', 'No message provided')
# #         logging.info(f'Received message: {message}')
# #         # Process incoming message
# #         for entry in data.get("entry", []):
# #             for change in entry.get("changes", []):
# #                 value = change.get("value", {})
# #                 messages = value.get("messages", [])
# #                 for message in messages:
# #                     # Handle the incoming message here
# #                     logging.info(f"Incoming message: {message}")
# #                     # You can add more logic to process the message and respond accordingly
# #         return {"status": "success"}
# #     except Exception as e:
# #         logging.error(f"Error processing webhook: {str(e)}")
# #         raise HTTPException(status_code=400, detail="Error processing webhook")
    
# # @app.get("/webhook")
# # async def verify_token(request: Request):
# #     token = request.query_params.get("hub.verify_token")
# #     challenge = request.query_params.get("hub.challenge")
# #     if token == config["VERIFY_TOKEN"]:
# #         return int(challenge)
# #     else:
# #         raise HTTPException(status_code=403, detail="Invalid verification token")

# API_KEY = "zXuPnT_sandbox"
# ADDRESS_URL = "https://waba-sandbox.360dialog.io"

# # Define the message data model
# class Message(BaseModel):
#     to: str
#     type: str
#     text: dict
#     channel_id: str

# @app.get("/channels")
# def get_channels():
#     headers = {
#         "D360-API-KEY": API_KEY,
#         "Content-Type": "application/json"
#     }
#     response = requests.get(f"{ADDRESS_URL}/v1/channels", headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HTTPException(status_code=response.status_code, detail=response.json())
    

# @app.post("/send_message")
# def send_message(msg: Message):
#     headers = {
#         "D360-API-KEY": API_KEY,
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "to": msg.to,
#         "type": msg.type,
#         "text": msg.text,
#         "channel_id": msg.channel_id
#     }

#     response = requests.post(ADDRESS_URL, json=payload, headers=headers)

#     if response.status_code == 200:
#         return {"status": "Message sent successfully", "response": response.json()}
#     else:
#         raise HTTPException(status_code=response.status_code, detail=response.json())

# @app.post("/webhook")
# async def webhook_handler(request: Request):
#     try:
#         data = await request.json()
#         print("Received data:", data)
#         # Process incoming message data here
#         return {"status": "success"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Run the application with uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests

class WebhookURL(BaseModel):
    url: str
app = FastAPI()

API_KEY = "jsSIcJ_sandbox"  # Replace with your actual Sandbox API key
BASE_URL = "https://waba-sandbox.360dialog.io"

@app.post("/send_message")
def send_message():
    headers = {
        "D360-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
     "messaging_product": "whatsapp",
     "recipient_type": "individual",
     "to": "+213 552 47 14 46 ",
     "type": "text",
     "text": {
        "body": "Hello, dear customer!"
    }
}
    response = requests.post(f"https://waba-sandbox.360dialog.io/v1/messages", json=payload, headers=headers)

    if response.status_code == 201:
        return {"status": "Message sent successfully", "response": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.post("/set_webhook")
def set_webhook(webhook: WebhookURL):
    headers = {
        "D360-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "url": webhook.url
    }

    response = requests.post(f"{BASE_URL}/v1/configs/webhook", json=payload, headers=headers)

    if response.status_code == 200:
        return {"status": "Webhook configured successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@app.post("/webhook")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        print("Received data:", data)
        # Process incoming message data here
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)