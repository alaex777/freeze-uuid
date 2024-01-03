# freeze-uuid

## Python package for mocking uuid
## For now only uuid1 and uuid4 have mocks
## Also you can use list of uuids for multiple usage

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

@freeze_uuid(['12af6b44-8181-11ee-b890-628ab7cd4d99', '12af6b44-8181-11ee-b890-628ab7cd4d98'])
def test_uuid_list():
    assert str(uuid.uuid1()) == '12af6b44-8181-11ee-b890-628ab7cd4d99'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d98'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d98'
    assert str(uuid.uuid4()) == '12af6b44-8181-11ee-b890-628ab7cd4d98'

```