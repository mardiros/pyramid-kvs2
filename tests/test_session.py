import json
from collections import deque
from typing import Type

from pyramid import testing

from pyramid_kvs2.testing import MockCache


def test_authtoken(dummy_request_factory: Type[testing.DummyRequest]):
    MockCache.cached_data = {b"session::x-dummy-header::dummy_key": '{"akey": "a val"}'}

    request = dummy_request_factory(headers={"X-Dummy-Header": "dummy_key"})

    client = request.session.client  # type: ignore
    client = request.session.client  # type: ignore
    assert isinstance(client, MockCache)
    assert client._serializer.dumps == json.dumps
    assert client.ttl == 600
    assert client.key_prefix == b"session::"
    assert request.session["akey"] == "a val"
    save_session = request.session.save_session  # type: ignore
    assert request.response_callbacks, deque([save_session])
