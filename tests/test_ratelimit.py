from typing import Type

import pytest
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.testing import DummyRequest

from pyramid_kvs2.ratelimit import RateLimitError
from pyramid_kvs2.testing import MockCache


def test_ratelimit(config: Configurator, dummy_request_factory: Type[DummyRequest]):
    assert config.registry
    MockCache.cached_data = {
        b"session::x-dummy-header::dummy_key": '{"akey": "a val"}',
        b"session::x-dummy-header::dummy_key::ratelimit": "9",
    }
    req = dummy_request_factory(headers={"X-Dummy-Header": "dummy_key"})

    config.registry.notify(NewRequest(req))
    rte = MockCache.cached_data[b"session::x-dummy-header::dummy_key::ratelimit"]
    assert rte == "10"

    with pytest.raises(RateLimitError) as ctx:
        config.registry.notify(NewRequest(req))

    assert str(ctx.value) == ""
