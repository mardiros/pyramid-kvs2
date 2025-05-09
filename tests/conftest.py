from typing import Any, Iterator, Mapping, Type

import pytest
from pyramid import testing
from pyramid.config import Configurator
from pyramid.interfaces import IRequestExtensions, ISessionFactory
from pyramid.request import apply_request_extensions


@pytest.fixture(scope="session")
def settings():
    return {
        "kvs.cache": {
            "kvs": "mock",
            "codec": "json",
            "key_prefix": "test::",
            "ttl": 20,
        },
        "kvs.session": {
            "kvs": "mock",
            "session_type": "header",
            "key_name": "X-Dummy-Header",
            "ttl": 600,
        },
        "kvs.ratelimit": {
            "window": 2,
            "limit": 10,
        },
    }


@pytest.fixture()
def config(settings: Mapping[str, Any]) -> Iterator[Configurator]:
    config = testing.setUp(settings=settings)
    config.include("pyramid_kvs.testing")
    yield config
    testing.tearDown()


@pytest.fixture()
def dummy_request_factory(config: Configurator) -> Type[testing.DummyRequest]:
    class DummyRequest(testing.DummyRequest):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            exts: IRequestExtensions = self.registry.queryUtility(IRequestExtensions)
            apply_request_extensions(self, exts)
            sess: ISessionFactory = config.registry.queryUtility(ISessionFactory)
            self.session = sess(self)

    return DummyRequest


@pytest.fixture()
def dummy_request(
    config: Configurator, dummy_request_factory: Type[testing.DummyRequest]
) -> testing.DummyRequest:
    return dummy_request_factory()
