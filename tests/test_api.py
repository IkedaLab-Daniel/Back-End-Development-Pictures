import json

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200


def test_count(client):
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json['length'] == 10


def test_data_contains_10_pictures(client):
    res = client.get("/picture")
    assert len(res.json) == 10


def test_get_picture(client):
    res = client.get("/picture")
    assert res.status_code == 200
    assert len(res.json) == 10


def test_get_pictures_check_content_type_equals_json(client):
    res = client.get("/picture")
    assert res.headers["Content-Type"] == "application/json"


def test_get_picture_by_id(client):
    id_delete = 2
    res = client.get(f'/picture/{id_delete}')
    assert res.status_code == 200
    assert res.json['id'] == id_delete

    res = client.get('/picture/404')
    assert res.status_code == 404


def test_pictures_json_is_not_empty(client):
    res = client.get("/picture")
    assert len(res.json) > 0


def test_post_picture(picture, client):
    # create a brand new picture to upload
    res = client.post("/picture", data=json.dumps(picture),
                      content_type="application/json")
    assert res.status_code == 201
    assert res.json['id'] == picture['id']
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json['length'] == 11

def test_post_picture_duplicate(picture, client):
    # create a brand new picture to upload
    res = client.post("/picture", data=json.dumps(picture),
                      content_type="application/json")
    assert res.status_code == 302
    assert res.json['Message'] == f"picture with id {picture['id']} already present"

def test_update_picture_by_id(client, picture):
    id = '2'
    res = client.get(f'/picture/{id}')
    res_picture = res.json
    assert res_picture['id'] == 2
    res_state = res_picture["event_state"]
    new_state = "*" + res_state
    res_picture["event_state"] = new_state
    res = client.put(f'/picture/{id}', data=json.dumps(res_picture),
                     content_type="application/json")
    res.status_code == 200
    res = client.get(f'/picture/{id}')
    assert res.json['event_state'] == new_state

def test_delete_picture_by_id(client):
    res = client.get("/count")
    assert res.json['length'] == 11
    res = client.delete("/picture/1")
    assert res.status_code == 204
    res = client.get("/count")
    assert res.json['length'] == 10
    res = client.delete("/picture/100")
    assert res.status_code == 404



