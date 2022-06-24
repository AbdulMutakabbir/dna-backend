from http.client import HTTPResponse
from typing import Optional, Union
from app import app
from fastapi import Cookie, HTTPException, Request, Response
from utils.dnac import updated_config 
from app.models import UpdateIp, Auth


@app.get("/")
def root():
    return "Welcome to carleton its dnac!"

@app.get("/health")
def health():
    return "OK"

@app.post("/api/get_updated_config")
def get_updated_config(update_ip_data: UpdateIp, request: Request):

    encoded_auth = request.cookies.get("encoded_auth")

    config, mapping = updated_config(encoded_auth, update_ip_data.source_ip, update_ip_data.destination_ip)

    return {"mapping":mapping, "config":config}


@app.post("/api/auth")
def auth(auth: Auth, response: Response):
    response.set_cookie(key="encoded_auth", value=auth.encoded_auth, httponly=True, secure=True, samesite='none', max_age=3600)
    return {"response": "auth success"}
