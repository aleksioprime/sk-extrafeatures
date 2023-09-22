import requests

TOKEN = 'Y1lt84AsVd8OHHti7ZfDbCIfDlu84Oa2'
SCHOOL = '1000013635121'

def get_groups_from_school(token, school):
    url_dnevnik_api = 'https://api.dnevnik.ru/v2/'
    headers = {
        'Access-Token': f'{token}',
        'Content-Type': 'application/json'
        }
    url = f'{url_dnevnik_api}/schools/{school}/edu-groups'
    return requests.get(url, headers=headers)

response_groups = get_groups_from_school(TOKEN, SCHOOL)
if response_groups.status_code == 200:
    for group in response_groups.json():
        print(group['fullName']), group['id_str']
    print(f"Количество групп: {len(response_groups.json())}")