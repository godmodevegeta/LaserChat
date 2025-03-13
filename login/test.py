import json
import helper

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

users = helper.load_temp_db()
data = user
valid_user = helper.check_if_user_already_exists(users, data)
print(valid_user)
