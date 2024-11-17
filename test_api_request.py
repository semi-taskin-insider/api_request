'''

--Test Plan--
#1 - Create Item
    - create
    - get

#2 - Update Item
    - create
    - get
    - update

#3 - Lıst Item
    - create
    - list

#4 - Delete Item
    - create
    - get
    - delete

'''

import uuid
import requests

ENDPOINT = "https://todo.pixegami.io/"

def create_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }
def create_task(payload):
    return requests.put(ENDPOINT + "create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"get-task/{task_id}")

def list_tasks(user_id) :
    return requests.get (ENDPOINT + f"/list-tasks/{user_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"delete-task/{task_id}")

def test_call_response():
    response = requests.get(ENDPOINT)
    assert response.status_code in {200, 201}

def test_create_task():
    payload = create_payload()
    create_response = create_task(payload)
    assert create_response.status_code in {200, 201}

    create_data = create_response.json()
    task_id = create_data["task"]["task_id"]

    task_id_response = get_task(task_id)
    assert task_id_response.status_code in {200, 201}

    task_data = task_id_response.json()
    assert task_data["content"] == payload["content"]
    assert task_data["user_id"] == payload["user_id"]

def test_update_task():
    payload = create_payload()
    create_response = create_task(payload)
    assert create_response.status_code in {200, 201}

    create_data = create_response.json()
    task_id = create_data["task"]["task_id"]

    new_payload = {
        "content": "melitest",
        "is_done": True,
        "task_id": task_id,
        "user_id": payload["user_id"]
    }
    update_response = update_task(new_payload)
    assert update_response.status_code in {200, 201}

    task_response = get_task(task_id)
    assert task_response.status_code in {200, 201}

    task_data = task_response.json()
    assert task_data["content"] == new_payload["content"]
    assert task_data["is_done"] == new_payload["is_done"]

def test_list_tasks():
    n = 5
    payload = create_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code in {200, 201}

    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code in {200, 201}
    data = list_task_response.json()

    tasks = data["tasks"]
    assert len(tasks) == n

def test_delete_task():
    payload = create_payload()
    create_response = create_task(payload)
    assert create_response.status_code in {200, 201}

    create_data = create_response.json()
    task_id = create_data["task"]["task_id"]
    delete_response = delete_task(task_id)
    assert delete_response.status_code in {200, 201}

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
    pass