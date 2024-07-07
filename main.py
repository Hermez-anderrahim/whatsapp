import base64
import json
import logging
from fastapi import FastAPI, HTTPException, Depends, Form , status , File, UploadFile
import aiohttp
import asyncio
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


class BuyTicketRequest(BaseModel):
    id: int


app = FastAPI()

# Load config from JSON file
with open('config.json') as f:
    config = json.load(f)

async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://graph.facebook.com/{config['VERSION']}/{config['PHONE_NUMBER_ID']}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                response_data = await response.json()  # Convert response to JSON if applicable

                if response.status == 200:
                    logging.info(f"Message sent successfully. Response: {response_data}")
                else:
                    logging.error(f"Failed to send message. Status: {response.status}. Response: {response_data}")
        except aiohttp.ClientConnectorError as e:
            logging.error(f'Connection Error: {str(e)}')
        # try:
        #     async with session.post(url, data=data, headers=headers) as response:
        #         if response.status == 200:
        #             print("Status hiiii:", response.status)
        #             print("Content-type:", response.headers['content-type'])

        #             html = await response.text()
        #             print("Body:", html)
        #         else:
        #             print(response.status)
        #             print(response)
        # except aiohttp.ClientConnectorError as e:
        #     print('Connection Error', str(e))

def get_text_message_input(recipient, text):
    return json.dumps({
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "body": text
        }
    })

@app.post("/welcome")
async def welcome(text : str ,recipient_waid: str = Form(...)):
    data = get_text_message_input(recipient_waid, text)
    await send_message(data)
    return {"message": "Message sent successfully"}






@app.post("/buy-ticket")
async def buy_ticket(text: str = Form(...)):
    # Specify the path to your file
    file_path = './serie1-THL.pdf'
    
    # Open the file in binary mode and read its content
    with open(file_path, 'rb') as file:
        attachment_bytes = file.read()

    
    # Encode the attachment content to base64
    base64_attachment = base64.b64encode(attachment_bytes).decode('utf-8')
    data = get_message_with_attachment(config['RECIPIENT_WAID'], base64_attachment ,file_path ,  text)
    await send_message(data)
    return {"message": "Message sent successfully"}


def get_message_with_attachment(recipient, attachment , file_path , text):
    # Construct message JSON with attachment and text
    
    
     
    message_data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "document",
        "document": {
            "link": "https://docs.google.com/viewerng/viewer?url=https://www.learningcontainer.com/download/sample-pdf-file-for-testing/?ind%3D0%26filename%3Dsample-pdf-file.pdf%26wpdmdl%3D1566%26refresh%3D6688f1e61be411720250854%26open%3D1",
            "filename": "randompdf.pdf",
            "caption": text
    }
    }
    
    
    return json.dumps(message_data)


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        logging.info(f"Received webhook data: {data}")

        # Process incoming message
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for message in messages:
                    # Handle the incoming message here
                    logging.info(f"Incoming message: {message}")
                    # You can add more logic to process the message and respond accordingly

        return {"status": "success"}
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=400, detail="Error processing webhook")

@app.get("/webhook")
async def verify_token(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == config["VERIFY_TOKEN"]:
        return int(challenge)
    else:
        raise HTTPException(status_code=403, detail="Invalid verification token")


# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
