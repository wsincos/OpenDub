import uuid

import pytest

from opendub.domain.ids import new_id, validate_uuid7


def test_new_id_returns_uuidv7() -> None:
    identifier = new_id()

    assert uuid.UUID(identifier).version == 7
    assert validate_uuid7(identifier) == identifier


def test_validate_uuid7_rejects_other_uuid_versions() -> None:
    with pytest.raises(ValueError, match="UUIDv7"):
        validate_uuid7(str(uuid.uuid4()))
