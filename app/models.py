from pydantic import BaseModel, Field

class UpdateIp(BaseModel):
    source_ip: str 
    destination_ip: str

class Auth(BaseModel):
    encoded_auth: str 