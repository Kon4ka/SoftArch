import requests


def test_find_by_name(name: str, surname: str):
    url = f"http://localhost:5005/api/users/find_by_name?" \
        f"name={name}&" \
        f"surname={surname}"
    request = requests.get(url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_find_by_login(login: str):
    url = f"http://localhost:5005/api/users/find_by_login?login={login}"
    request = requests.get(url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_new_user(user_login: str, user_name: str, user_surname: str, user_password: str):
    data = {
        "user_login": user_login,
        "user_name": user_name,
        "user_surname": user_surname,
        "user_password": user_password
    }
    url = f"http://localhost:5005/api/users/new_user"
    request = requests.post(url=url, json=data)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_user_info(id: int):
    url = f"http://localhost:5005/api/users/info?id={id}"
    request = requests.get(url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_delete_user(id: int):
    url = f"http://localhost:5005/api/users/delete?id={id}"
    request = requests.delete(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_update_user(user_id: int, user_login: str = None, user_name: str = None, user_surname: str = None, user_password: str = None):
    data = {
        "user_id": user_id,
        "user_login": user_login,
        "user_name": user_name,
        "user_surname": user_surname,
        "user_password": user_password
    }
    url = f"http://localhost:5005/api/users/update"
    request = requests.put(url=url, json=data)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_new_report(report_title: str, mongodb_id: str):
    data = {
        "report_title": report_title,
        "mongodb_id": mongodb_id,
    }
    url = f"http://localhost:5005/api/reports/new_report"
    request = requests.post(url=url, json=data)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_get_all_reports():
    url = f"http://localhost:5005/api/reports/"
    request = requests.get(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_add_report_to_conference(conference_id: int, report_id: int):
    url = f"http://localhost:5005/api/reports/add_report_to_conference?"\
        f"conference_id={conference_id}&"\
        f"report_id={report_id}"
    request = requests.get(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_get_reports_by_conference(conference_id: int):
    url = f"http://localhost:5005/api/reports/get_reports_by_conference?"\
        f"conference_id={conference_id}"
    request = requests.get(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


test_user_info(id=1)
test_new_user(user_login="kon4ka", user_name="Rina",
              user_surname="Lisakovskaya", user_password="1234")
test_find_by_login(login="kon")
test_find_by_name(name="Ri", surname="Lisa")
test_delete_user(id=1)
test_update_user(user_id=11, user_login="kon8ka")
test_new_report(report_title="Hello, world!", mongodb_id="123asdsdaf31")
test_get_all_reports()
test_add_report_to_conference(conference_id=1, report_id=1)
test_add_report_to_conference(conference_id=1, report_id=2)
test_add_report_to_conference(conference_id=1, report_id=3)
test_add_report_to_conference(conference_id=2, report_id=4)
test_add_report_to_conference(conference_id=2, report_id=5)
test_add_report_to_conference(conference_id=2, report_id=6)
test_add_report_to_conference(conference_id=3, report_id=7)
test_add_report_to_conference(conference_id=3, report_id=8)
test_add_report_to_conference(conference_id=3, report_id=9)
test_get_reports_by_conference(conference_id=2)
