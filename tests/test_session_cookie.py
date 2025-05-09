import json
from collections import deque
from typing import Type

import pytest
from pyramid import testing

from pyramid_kvs.testing import MockCache


@pytest.fixture()
def settings():
    return {
        "pyramid.includes": ["pyramid_kvs.testing"],
        "kvs.session": {
            "kvs": "mock",
            "key_name": "SessionId",
            "session_type": "cookie",
            "codec": "json",
            "key_prefix": "cookie::",
            "ttl": 20,
        },
    }


def test_cookie(dummy_request_factory: Type[testing.DummyRequest]):
    MockCache.cached_data = {b"cookie::chocolate": '{"anotherkey": "another val"}'}
    request = dummy_request_factory(cookies={"SessionId": "chocolate"})
    client = request.session.client  # type: ignore
    assert isinstance(client, MockCache)
    assert client._serializer.dumps == json.dumps
    assert client.ttl == 20
    assert client.key_prefix == b"cookie::"
    assert request.session["anotherkey"] == "another val"
    save_session = request.session.save_session  # type: ignore
    assert request.response_callbacks, deque([save_session])


def test_should_renew_session_on_invalidate(
    dummy_request_factory: Type[testing.DummyRequest],
):
    MockCache.cached_data = {b"cookie::chocolate": '{"stuffing": "chocolate"}'}
    request = dummy_request_factory(cookies={"SessionId": "chocolate"})
    session = request.session

    # Ensure session is initialized
    assert session["stuffing"] == "chocolate"
    # Invalidate session
    session.invalidate()

    # session is invalidated
    assert "stuffing" not in session
    # ensure it can be reused immediately
    session["stuffing"] = "macadamia"

    assert session["stuffing"] == "macadamia"
