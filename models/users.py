# from services.services import BaseMode
from pydantic import BaseModel, Field, constr


class UsersModel(BaseModel):
    document_type:  str
    document:  str
    name:  str
    full_last:  str
    hobbie:  str
