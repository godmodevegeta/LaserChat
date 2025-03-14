import json
import helper
from functools import wraps
import datetime


# with open('users.json') as f:
#     users = json.load(f)

# print(users)

user = {
        "email": "cat@gmail.com",
        "username": "c1at_1234",
        "password": "Cat@1234"
    }

# users.append(user)

# with open('users.json', 'w') as f:
#     json.dump(users, f)

# print(users)

# users = helper.load_temp_db()
# data = user
# valid_user = helper.check_if_user_already_exists(users, data)
# print(valid_user)




# def logger(functionx):
#     wraps(functionx)
#     def inner(*args, **kwargs):
#         print("entering function", functionx.__name__)
#         result = functionx(*args, **kwargs)
#         print("exiting function", functionx.__name__)
#         return result
#     return inner

# @logger
# def summer(a: int, b: int, c: int) -> int:
#     return(a + b + c)

# summer(2,2,2)

print(datetime.datetime.now().isoformat)