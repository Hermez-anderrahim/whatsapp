
import os
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
    "to": "213552471446",
    "type": "text",
    "text": {
        "body": "hiii pipit its working in my machine "
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
        print(data)
        if not data:
            raise HTTPException(status_code=400, detail="Empty request body")
        print("Received data:", data)
        # Process incoming message data here
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)