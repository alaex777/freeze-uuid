# freeze-uuid

## Python package for mocking uuid

### Usage Example

```python
from freeze_uuid import freeze_uuid


@freeze_uuid('12af6b44-8181-11ee-b890-628ab7cd4d99')
def test_uuid():
    assert str(uuid.uuid1()) == '12af6b44-8181-11ee-b890-628ab7cd4d99'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d99'

@freeze_uuid()
def test_uuid_default():
    assert str(uuid.uuid1()) == '00000000-0000-0000-0000-000000000000'
    assert str(uuid.uuid4()) == '00000000-0000-0000-0000-000000000000'

@pytest.mark.asyncio
@freeze_uuid('12af6b44-8181-11ee-b890-628ab7cd4d99')
async def test_uuid_async():
    assert str(uuid.uuid1()) == '12af6b44-8181-11ee-b890-628ab7cd4d99'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d99'
```

### Also you can use list of uuids for multiple usage

```python
@freeze_uuid(['12af6b44-8181-11ee-b890-628ab7cd4d99', '12af6b44-8181-11ee-b890-628ab7cd4d98'])
def test_uuid_list():
    assert str(uuid.uuid1()) == '12af6b44-8181-11ee-b890-628ab7cd4d99'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d98'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d98'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d98'

```

### Since library mocks uuid.UUID class, it can be used with all libraries, that support UUID class, i.e. uuid7

```python
from uuid_extensions import uuid7

@freeze_uuid(TEST_UUID)
def test_uuid_7():
    assert str(uuid7()) == TEST_UUID

```

### With freeze_uuid context manager you can create tests with pytest parametrize
```python
from freeze_uuid import freeze_uuid_manager

@pytest.mark.parametrize(
    ['expected_result', 'freeze_data'],
    [
        pytest.param(
            TEST_UUID_2,
            [TEST_UUID_2],
        ),
        pytest.param(
            TEST_UUID_3,
            [TEST_UUID_3],
        ),
        pytest.param(
            TEST_UUID_4,
            [TEST_UUID_4],
        ),
        pytest.param(
            TEST_UUID_5,
            [TEST_UUID_5],
        ),
    ]
)
def test_parametrize(expected_result, freeze_data):
    with freeze_uuid_manager(freeze_data):
        assert str(uuid.uuid4()) == expected_result
```
