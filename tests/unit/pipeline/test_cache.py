from opendub.pipeline.cache import stage_cache_key


def test_stage_cache_key_changes_when_seed_or_weights_change() -> None:
    base = {"asset_sha256": "a", "segment_revision": 1, "weight_sha256": "b", "seed": 7}

    assert stage_cache_key(base) != stage_cache_key({**base, "seed": 8})
    assert stage_cache_key(base) != stage_cache_key({**base, "weight_sha256": "c"})
