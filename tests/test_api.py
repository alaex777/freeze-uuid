import uuid
from uuid_extensions import uuid7

import pytest

from freeze_uuid import freeze_uuid

from tests.testdata import (
    TEST_UUID, TEST_UUID_2, TEST_UUID_3, TEST_UUID_4,
    TEST_UUID_5, TEST_UUID_6, TEST_UUID_7, TEST_UUID_8
)


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


@freeze_uuid(TEST_UUID)
def get_uuid():
    return uuid.uuid1()


def test_uuid_from_func():
    assert get_uuid() == TEST_UUID


def test_uuid_from_func_2():
    assert uuid.uuid4() != TEST_UUID


@freeze_uuid([TEST_UUID_3, TEST_UUID_4])
def test_list_uuids_1():
    assert str(uuid.uuid1()) == TEST_UUID_3
    assert str(uuid.uuid4()) == TEST_UUID_4
    assert str(uuid.uuid1()) == TEST_UUID_4
    assert str(uuid.uuid4()) == TEST_UUID_4
    assert str(uuid.uuid1()) == TEST_UUID_4
    assert str(uuid.uuid4()) == TEST_UUID_4
    assert str(uuid.uuid1()) == TEST_UUID_4


@freeze_uuid()
def test_uuid_default_2():
    assert str(uuid.uuid1()) == '00000000-0000-0000-0000-000000000000'
    assert str(uuid.uuid4()) == '00000000-0000-0000-0000-000000000000'


@freeze_uuid([TEST_UUID_5, TEST_UUID_6, TEST_UUID_7, TEST_UUID_8])
def test_list_uuids_2():
    assert str(uuid.uuid1()) == TEST_UUID_5
    assert str(uuid.uuid4()) == TEST_UUID_6
    assert str(uuid.uuid1()) == TEST_UUID_7
    assert str(uuid.uuid1()) == TEST_UUID_8
    assert str(uuid.uuid1()) == TEST_UUID_8
    assert str(uuid.uuid1()) == TEST_UUID_8


def test_uuid_from_func_3():
    assert uuid.uuid4() != TEST_UUID_6


@freeze_uuid(TEST_UUID)
def test_uuid_2():
    assert str(uuid.uuid1()) == TEST_UUID
    assert str(uuid.uuid4()) == TEST_UUID


@freeze_uuid()
def test_uuid_default_3():
    assert str(uuid.uuid1()) == '00000000-0000-0000-0000-000000000000'
    assert str(uuid.uuid4()) == '00000000-0000-0000-0000-000000000000'


@freeze_uuid(TEST_UUID)
def test_uuid_3():
    assert str(uuid.uuid3(uuid.NAMESPACE_DNS, 'google.com')) == TEST_UUID
    assert str(uuid.uuid5(uuid.NAMESPACE_DNS, 'google.com')) == TEST_UUID


@freeze_uuid(TEST_UUID)
def test_uuid_7():
    assert str(uuid7()) == TEST_UUID


def test_uuid_7_not_equal():
    assert str(uuid7()) != TEST_UUID
