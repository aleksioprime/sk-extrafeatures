from app import app
from flask import session, send_file, jsonify, request
import requests


from .models import User
from .routes import login_required

SCHOOL = '1000013635121'
URL_DNEVNIK = 'https://api.dnevnik.ru/v2/'


@app.route('/users/me', methods=["GET"])
@login_required
def userme():
    user = User.query.filter_by(id=session["id"]).first()
    headers = {
        'Access-Token': f'{user.token_dnevnik}',
        'Content-Type': 'application/json'
        }
    url = f'{URL_DNEVNIK}/users/me'
    result = requests.get(url, headers=headers)
    print(result)
    return result.json()

# функция запроса данных о группах пользователя в Дневник.ру
def get_all_groups(token, person):
    headers = {
        'Access-Token': f'{token}',
        'Content-Type': 'application/json'
        }
    url = f'{URL_DNEVNIK}/persons/{person}/edu-groups/all'
    return requests.get(url, headers=headers)

# функция запроса информации о персоне в Дневник.ру
def get_person_info(token, person):
    headers = {
        'Access-Token': f'{token}',
        'Content-Type': 'application/json'
        }
    url = f'{URL_DNEVNIK}/persons/{person}'
    return requests.get(url, headers=headers)

# функция запроса данных об итоговых оценках пользователя в группе в Дневник.ру
def get_final_marks_and_subjects(token, person, group):
    headers = {
        'Access-Token': f'{token}',
        'Content-Type': 'application/json'
        }
    url = f'{URL_DNEVNIK}persons/{person}/edu-groups/{group}/allfinalmarks'
    return requests.get(url, headers=headers)

def get_report_finalmarks(token, person):
    response_groups = get_all_groups(token, person)
    if response_groups.status_code == 200:
        data_groups = response_groups.json()
        groups = []
        for group in data_groups:
            if group['type'] == 'Group':
                groups.append({'id': group['id_str'], 'name': group['name'], 'year': group['studyyear']})
        
        for group in groups:
            response_marks = get_final_marks_and_subjects(token, person, group['id'])
            if response_marks.status_code == 200:
                data_marks = response_marks.json()
                marks = {}
                for mark in data_marks['marks']:
                    marks[mark['work_str']] = mark['value']

                subjects = {}
                for subject in data_marks['subjects']:
                    subjects[subject['id']] = subject['name']

                # works = {}
                # for work in data_marks['works']:
                #     if work['subjectId'] in subjects and work['id_str'] in marks and work['periodType'] == 'Year':
                #         if subjects[work['subjectId']] in works:
                #             if works[subjects[work['subjectId']]]['type'] != 'PeriodFinalMark':
                #                 works[subjects[work['subjectId']]] = { 'mark': marks[work['id_str']], 'type': work['type'] }
                #         else:
                #             works[subjects[work['subjectId']]] = { 'mark': marks[work['id_str']], 'type': work['type'] }

                works = {}
                for work in data_marks['works']:
                    if work['subjectId'] in subjects and work['id_str'] in marks and work['periodType'] == 'Year':
                        if work['subjectId'] in works:
                            if works[work['subjectId']]['type'] != 'PeriodFinalMark':
                                works[work['subjectId']] = { 'mark': marks[work['id_str']], 'type': work['type'], 'subjectName': subjects[work['subjectId']] }
                        else:
                            works[work['subjectId']] = { 'mark': marks[work['id_str']], 'type': work['type'], 'subjectName': subjects[work['subjectId']] }
                
                group['marks'] = works

        response_person = get_person_info(token, person)
        if response_person.status_code == 200:
            data_person = response_person.json()

        return {
            'status': 'good',
            'student': data_person,
            'groups': groups
        }
    else:
        return {
            'status': 'bad',
        }

@app.route('/student/<int:student_id>/groups', methods=["GET"])
@login_required
def groups(student_id):
    user = User.query.filter_by(id=session["id"]).first()
    result = get_all_groups(user.token_dnevnik, student_id)
    if result.status_code == 200:
        data_groups = result.json()
        groups = []
        for group in data_groups:
            if group['type'] == 'Group':
                groups.append({'id': group['id_str'], 'name': group['name'], 'year': group['studyyear']})
        return jsonify(groups)
    else:
        return jsonify("Error")
    
@app.route('/student/<int:student_id>/allmarks', methods=["GET"])
@login_required
def marks(student_id):
    user = User.query.filter_by(id=session["id"]).first()
    result = get_report_finalmarks(user.token_dnevnik, student_id)
    return jsonify(result)

