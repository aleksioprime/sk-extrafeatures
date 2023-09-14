import requests
from docxtpl import DocxTemplate

TOKEN = 'C7LZbuMjJTqhxdUuNx7YwP0rR7VmTA54'
SCHOOL = '1000013635121'
PERSON = '1000014806800'
# GROUP = '1844871832843220738'

def create_file(file_input, context, file_output):
    doc = DocxTemplate(file_input)
    doc.render(context)
    doc.save(file_output)

def get_final_marks_and_subjects(token, person, group):
    url_dnevnik_api = 'https://api.dnevnik.ru/v2/'
    headers = {
        'Access-Token': f'{token}',
        'Content-Type': 'application/json'
        }
    url = f'{url_dnevnik_api}persons/{person}/edu-groups/{group}/allfinalmarks'
    return requests.get(url, headers=headers)

def get_all_groups(token, person):
    url_dnevnik_api = 'https://api.dnevnik.ru/v2/'
    headers = {
        'Access-Token': f'{token}',
        'Content-Type': 'application/json'
        }
    url = f'{url_dnevnik_api}persons/{person}/edu-groups/all'
    return requests.get(url, headers=headers)


response_groups = get_all_groups(TOKEN, PERSON)
if response_groups.status_code == 200:
    data_groups = response_groups.json()
    groups = []
    for group in data_groups:
        if group['type'] == 'Group':
            groups.append({'id': group['id_str'], 'name': group['name'], 'year': group['studyyear']})


for group in groups:
    response_data = get_final_marks_and_subjects(TOKEN, PERSON, group['id'])
    if response_data.status_code == 200:
        data = response_data.json()
        marks = {}
        for mark in data['marks']:
            marks[mark['work_str']] = mark['value']

        subjects = {}
        for subject in data['subjects']:
            subjects[subject['id']] = subject['name']

        works = {}
        for work in data['works']:
            if work['subjectId'] in subjects and work['id_str'] in marks and work['periodType'] == 'Year':
                if subjects[work['subjectId']] in works:
                    if works[subjects[work['subjectId']]]['type'] != 'PeriodFinalMark':
                        works[subjects[work['subjectId']]] = { 'mark': marks[work['id_str']], 'type': work['type'] }
                else:
                    works[subjects[work['subjectId']]] = { 'mark': marks[work['id_str']], 'type': work['type'] }
        
        group['marks'] = works

print(groups)
        # create_file("subject_template.docx", { 'marks': group }, 'test.docx')
