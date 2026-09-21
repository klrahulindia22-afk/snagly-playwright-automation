def assert_envelope(response, expected_status: int = 200) -> dict:
    assert response.status == expected_status, response.text()
    body = response.json()
    assert isinstance(body, dict)
    assert "data" in body
    return body["data"]


def assert_collection(response) -> list:
    data = assert_envelope(response)
    assert isinstance(data, list)
    return data
