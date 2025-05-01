from bson import ObjectId
from pydantic import BaseModel, Field
from mongodb import user_collection
from auth import hash_password

# To support ObjectId in Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserBase(BaseModel):
    email: str

class UserAuth(UserBase):
    password: str

class UserCreate(UserAuth):
    name: str
    role: str = "user"

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class UserPublic(UserBase):
    id: str
    name: str
    role: str = "user"

def create_user(user: UserCreate) -> UserPublic:
    if user_collection.find_one({"email": user.email}):
        raise ValueError("Email already registered")

    user_dict = {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "hashed_password": hash_password(user.password)
    }

    result = user_collection.insert_one(user_dict)

    return UserPublic(
        id=str(result.inserted_id),
        name=user.name,
        email=user.email,
    )

def get_user_by_email(email: str) -> UserInDB | None:
    result = user_collection.find_one({"email": email})
    if not result:
        return None

    return UserInDB(
        email=result["email"],
        hashed_password=result["hashed_password"]
    )