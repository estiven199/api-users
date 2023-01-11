from pydantic import BaseModel

class keys(BaseModel):
    x_token: str
    x_api_key: str
    x_secret_id: str
