import json
import requests
from randomuser import RandomUser

from ntc_regions import ntc_region_choices

NTC_REGIONS = len(ntc_region_choices)

RESULTS_SERVER_API_URL = "http://202.90.159.48/api"

def _get_user(data):
    ntc_region = data[0]
    user_obj: RandomUser = data[1]
    user = {'first_name': user_obj.get_first_name(), 'last_name': user_obj.get_last_name(),
            'email': f"{user_obj.get_full_name(False).replace(' ', '.')}@example.com",
            'password': "netmesh1234",
            'ntc_region': ntc_region[0]}
    return user


def generate_users(n):
    regions = []
    if 0 < n <= NTC_REGIONS:
        regions.extend(ntc_region_choices[:n])
    elif not n % NTC_REGIONS:
        regions.extend(ntc_region_choices * n)
    else:
        not_multiple = n % NTC_REGIONS
        regions.extend(ntc_region_choices * n)
        regions.extend(ntc_region_choices[:not_multiple])

    users = RandomUser.generate_users(n, {'nat': 'us'})
    users = map(_get_user, zip(regions, users))

    return list(users)

def register_users(users):
    token = get_admin_token()

    if not token:
        print("no token")
        return

    try:
        for user in users:
            r = requests.post(
                url=f'{RESULTS_SERVER_API_URL}/user/create/',
                json=user,
                headers={"Authorization": f"Token {token}"}
            )
            r.raise_for_status()
            
            print("added to the rs: ", user)
    except requests.exceptions.RequestException as rx:
        print(r.content)

def get_admin_token():
    token = None
    try:
        r = requests.post(
            url=f'{RESULTS_SERVER_API_URL}/user/token/',
            json={
                "email": "super@example.com",
                "password": "netmesh!@#",
                "client": "admin"
            }
        )
        r.raise_for_status()
        token = r.json()["token"]
    except requests.exceptions.RequestException as rx:
        print("error", rx)

    return token

if __name__ == "__main__":
    rand_users = generate_users(95)
    for i in rand_users:
        print(i)
