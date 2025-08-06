from pyramid_kvs2 import serializer
from pyramid_kvs2.cache import ApplicationCache
from pyramid_kvs2.testing import MockCache


def test_cache(dummy_request):
    assert isinstance(dummy_request.cache, ApplicationCache)
    client = dummy_request.cache.client
    assert isinstance(client, MockCache)
    assert client._serializer.dumps == serializer.json.dumps
    assert client.ttl == 20
    assert client.key_prefix == b"test::"


def test_cache_set(dummy_request):
    dummy_request.cache["dummy"] = "value"
    assert MockCache.cached_data[b"test::dummy"] == '"value"'
    assert MockCache.last_ttl == 20


def test_cache_set_ttl(dummy_request):
    dummy_request.cache.set("dummy", "value", 200)
    assert MockCache.cached_data[b"test::dummy"] == '"value"'
    assert MockCache.last_ttl == 200


def test_pop_val(dummy_request):
    MockCache.cached_data[b"test::popme"] = '"value"'
    val = dummy_request.cache.pop("popme")
    assert val == "value"
    assert "popme" not in MockCache.cached_data


def test_get_keys(dummy_request):
    MockCache.cached_data[b"test::key1"] = '"value1"'
    MockCache.cached_data[b"test::key2"] = '"value2"'
    val = dummy_request.cache.list_keys()
    assert val == ["key1", "key2"]


def test_get_keys_wildcard(dummy_request):
    MockCache.cached_data[b"test::key1"] = '"value1"'
    MockCache.cached_data[b"test::clef2"] = '"valeur2"'
    MockCache.cached_data[b"test::kagi3"] = '"varyu3"'
    val = dummy_request.cache.list_keys("key*")
    assert val == ["key1"]

    val = dummy_request.cache.list_keys("k*")
    assert val == ["key1", "kagi3"]

    val = dummy_request.cache.list_keys(r"[a-z]+\d")
    assert val == []
