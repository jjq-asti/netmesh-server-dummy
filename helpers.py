from randomuser import RandomUser

from ntc_regions import ntc_region_choices

NTC_REGIONS = len(ntc_region_choices)


def _get_user(data):
    ntc_region = data[0]
    user_obj: RandomUser = data[1]
    user = {'firstname': user_obj.get_first_name(), 'lastname': user_obj.get_last_name(),
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

    users = RandomUser.generate_users(n, {'nat': 'ch'})
    users = map(_get_user, zip(regions, users))

    return list(users)


def register_user(user):
    # TODO: submit generated random users to results server

    pass


if __name__ == "__main__":
    rand_users = generate_users(20)
    for i in rand_users:
        print(i)
