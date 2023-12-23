from .bot_config import CLIENT

def findUser(user_id):
    # return user on success and None on failure
    return CLIENT.get_user(user_id)