import httpx


def base_url():
    return "http://127.0.0.1:8000"


def test_get_users():
    response = httpx.get(base_url() + "/api/v1/users/")
    assert response.status_code == 200
    users = response.json()["result"]
    assert type(users) is list


def test_create_user():
    user_data = {"nickname": "buyer123", "email": "abc123", "password": "hometownrevolution"}
    response = httpx.post(base_url() + "/api/v1/users/", json=user_data)
    json_response = response.json()
    if not json_response["success"]:
        print(json_response["error"])
    assert response.status_code == 200 and json_response["success"]


def test_create_duplicate_user():
    user_data = {"nickname": "buyer123", "email": "abc123", "password": "hometownrevolution"}

    error_text = "nickname={0} & email={1} -> Such user already exist".format(user_data["nickname"], user_data["email"])

    response = httpx.post(base_url() + "/api/v1/users/", json=user_data)
    json_response = response.json()
    assert (response.status_code == 200
            and not json_response["success"]
            and json_response["error"] == error_text)


def test_get_user():
    user_data = {"nickname": "test_user", "email": "test_email", "password": "test_password"}
    response = httpx.post(base_url() + "/api/v1/users/", json=user_data)
    json_response = response.json()
    if not json_response["success"]:
        print(json_response["error"])
    assert response.status_code == 200 and json_response["success"]

    new_user_id = json_response["result"]["id"]

    response = httpx.get(base_url() + f"/api/v1/users/{new_user_id}")
    json_response = response.json()

    assert response.status_code == 200 and json_response["success"] and json_response["result"]["nickname"] == user_data["nickname"]


def test_delete_user():
    response = httpx.get(base_url() + "/api/v1/users/")
    users = response.json()["result"]

    for user in users:
        if user["nickname"] == "test_user":
            response = httpx.delete(base_url() + f"/api/v1/users/{user["id"]}")
            json_response = response.json()
            if not json_response["success"]:
                print(json_response["error"])
            assert response.status_code == 200 and json_response["success"]

            response = httpx.get(base_url() + f"/api/v1/users/{user["id"]}")
            json_response = response.json()
            assert response.status_code == 200 and not json_response["success"]
            break


def test_update_user():
    response = httpx.get(base_url() + "/api/v1/users/")
    users = response.json()["result"]
    users_len = len(users)
    user_id = users[users_len - 1]["id"]

    user_data = {"nickname": "test_user", "email": "test_email", "password": "test_password"}

    response = httpx.put(base_url() + f"/api/v1/users/{user_id}", json=user_data)
    json_response = response.json()
    if not json_response["success"]:
        print(json_response["error"])

    assert response.status_code == 200 and json_response["success"] and json_response["result"]["nickname"] == user_data["nickname"]
