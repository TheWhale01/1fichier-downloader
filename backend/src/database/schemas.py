from pydantic import BaseModel

class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str

class User(UserCreate):
	id: int

	class Config:
		from_attributes = True

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	username: str | None = None

class DownloadBase(BaseModel):
	link: str

class DownloadCreate(DownloadBase):
	pass

class Download(DownloadCreate):
	id: int
	filename: str
	state: int

	class Config:
		from_attributes = True