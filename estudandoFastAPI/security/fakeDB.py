from securityModels import UserInDB


fake_users_db = {
    "eu": {
        "username": "eu",
        "full_name": "John Doe",
        "email": "eu@example.com",
        "hashed_password": "$2b$12$sTTx1EZZW6KV3d3wNKZCQOGbSbDqCL2RNePHGjlkqlWmiZ1nCf/8K",
        "disabled": False,
    },
    "eu2": {
        "username": "eu2",
        "full_name": "eu2 Chains",
        "email": "eu2@example.com",
        "hashed_password": "$2b$12$sTTx1EZZW6KV3d3wNKZCQOGbSbDqCL2RNePHGjlkqlWmiZ1nCf/8K",
        "disabled": True,
    },
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
