import uuid

import pytest

from freeze_uuid import freeze_uuid

from tests.testdata import TEST_UUID, TEST_UUID_2


@freeze_uuid(TEST_UUID)
def test_uuid():
    assert str(uuid.uuid1()) == TEST_UUID
    assert str(uuid.uuid4()) == TEST_UUID


@freeze_uuid(TEST_UUID_2)
def test_uuid_default():
    assert str(uuid.uuid1()) == TEST_UUID_2
    assert str(uuid.uuid4()) == TEST_UUID_2


@freeze_uuid()
def test_uuid_default():
    assert str(uuid.uuid1()) == '00000000-0000-0000-0000-000000000000'
    assert str(uuid.uuid4()) == '00000000-0000-0000-0000-000000000000'


@pytest.mark.asyncio
@freeze_uuid(TEST_UUID)
async def test_uuid_async():
    assert str(uuid.uuid1()) == TEST_UUID
    assert str(uuid.uuid4()) == TEST_UUID
