import json
from helpers import generate_users

# TODO: Post generated users to server


if __name__ == "__main__":
    rand_users = generate_users(20)
    # convert to json
    users_json = json.dumps(rand_users, indent=4)
    print(users_json)