from config.db import user_collection
from models.authModel import RegisterUser, LoginUser
from fastapi.exceptions import HTTPException
import bcrypt


async def registerService(data: RegisterUser):
    check_exist = await user_collection.find_one({"email": data.email.lower()})
    if check_exist:
        raise HTTPException(status_code=400, detail="Email already exists")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), salt)
    hash_string = hashed_password.decode("utf-8")
    user_data = data.dict()
    user_data["password"] = hash_string

    await user_collection.insert_one(user_data)
    return {"message": "User registered successfully", "toekn": ""}


async def loginService(data: LoginUser):
    # Check if user exist
    check_exist = await user_collection.find_one({"email": data.email.lower()})
    if not check_exist:
        raise HTTPException(status_code=400, detail="User Not Exist")

    # Verify password
    is_match = bcrypt.checkpw(
        data.password.encode("utf-8"), check_exist["password"].encode("utf-8")
    )
    if not is_match:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    token = ""
    return {"message": "Login Successfull", "token": token}
