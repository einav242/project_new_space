from pydantic import BaseModel


class AuthDetails(BaseModel):
    ImagePath: str


