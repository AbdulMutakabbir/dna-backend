from http.client import HTTPResponse
from typing import Optional, Union
from app import app
from fastapi import Cookie, HTTPException, Request, Response
from utils.dnac import get_config, updated_config, run_cmd_show_interface_status, get_filtered_device_list
from app.models import Ip, UpdateIp, Auth, SkipPortList, SelectedPorts, AdvanceFilter


@app.get("/")
def root():
    return "Welcome to carleton its dnac!"

@app.get("/health")
def health():
    return "OK"

@app.post("/api/config")
def get_updated_config(ip_data: Ip, skip_port_list: SkipPortList, request: Request):

    encoded_auth = request.cookies.get("encoded_auth")

    config = get_config(encoded_auth, skip_port_list.port_types, ip_data.ip)

    return config

@app.post("/api/get_updated_config")
def get_updated_config(
    update_ip_data: UpdateIp, 
    selected_ports: SelectedPorts,
    advance_filter: AdvanceFilter,
    request: Request):

    encoded_auth = request.cookies.get("encoded_auth")

    config, mapping = updated_config(
        encoded_auth, 
        update_ip_data.source_ip, 
        update_ip_data.destination_ip, 
        selected_ports.source, 
        selected_ports.destination)

    return {"mapping":mapping, "config":config}


@app.post("/api/auth")
def auth(auth: Auth, response: Response):
    response.set_cookie(key="encoded_auth", value=auth.encoded_auth, httponly=True, secure=True, samesite='none', max_age=3600)
    return {"response": "auth success"}


@app.post("/api/get_port_list")
def get_port_list(ip_data: Ip, request: Request):
    encoded_auth = request.cookies.get("encoded_auth")

    ports = run_cmd_show_interface_status(encoded_auth, ip_data.ip)

    return ports

@app.get("/api/get_filtered_switches")
def get_filtered_switches(request: Request):
    encoded_auth = request.cookies.get("encoded_auth")

    ports = get_filtered_device_list(encoded_auth)

    return ports