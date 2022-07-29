from pydantic import BaseModel, Field

class Ip(BaseModel):
    ip: str 

class UpdateIp(BaseModel):
    source_ip: str 
    destination_ip: str

class Auth(BaseModel):
    encoded_auth: str 

class SkipPortList(BaseModel):
    port_types: list

class SelectedPorts(BaseModel):
    source: list
    destination: list

class AdvanceFilter(BaseModel):
    source_onlyShutDown: bool
    source_trunkPort: bool
    destination_onlyShutDown: bool
    destination_trunkPort: bool