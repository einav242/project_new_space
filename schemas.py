from pydantic import BaseModel


class AuthDetails(BaseModel):
    ImagePath: str


class Access(BaseModel):
    starsList: str
