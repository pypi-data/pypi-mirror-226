from pathlib import Path
from pprint import pprint

import pytest
from fastapi.testclient import TestClient

from main import app
from main import ModelName
from schemas import ItemSchema

# from main import Item
# from models import Item
# from models import User

client = TestClient(app)
ModelMsg = ['Deep Learning FTW!', 'Have some residuals', 'LeCNN all the images']


class TestPing:
    def test_ping(self):
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.json() == {'msg': 'pong'}


class TestItems:
    def test_read_item(self):
        response = client.get('/items/5')
        assert response.status_code == 200
        assert response.json() == {'item_id': 5}
        pass

    def test_read_item_optional(self):
        response = client.get('/items/5?q=foo')
        assert response.status_code == 200
        assert response.json() == {'item_id': 5, 'q': 'foo'}
        pass

    def test_read_item_req_param(self):
        response = client.get('/items/5?q=foo')
        assert response.status_code == 200
        assert response.json() == {'item_id': 5, 'q': 'foo'}
        pass

    def test_read_item_str(self):
        response = client.get('/items/foo')
        assert response.status_code == 422
        assert response.json() == {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': ['path', 'item_id'],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'foo',
                    'url': 'https://errors.pydantic.dev/2.2/v/int_parsing',
                }
            ]
        }
        pass

    def test_read_item_query_all(self):
        response = client.get('/items/?skip=0&limit=10')
        assert response.status_code == 200
        assert response.json() == [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]
        pass

    def test_read_item_query_none(self):
        response = client.get('/items/')
        assert response.status_code == 200
        assert response.json() == [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]
        pass

    def test_read_item_query_slice(self):
        response = client.get('/items/?skip=1&limit=10')
        assert response.status_code == 200
        assert response.json() == [{'item_name': 'Bar'}, {'item_name': 'Baz'}]
        pass

    def test_create_item_post(self):
        item = ItemSchema(name='Item name', price=2.0, tax=0.1)
        response = client.post('/items/', json=dict(item))
        assert response.status_code == 200
        assert response.json() == {
            'name': 'Item name',
            'description': None,
            'price': 2.0,
            'tax': 0.1,
            'price_with_tax': 2.1,
        }
        pass

    def test_create_item_put(self):
        item = ItemSchema(name='Item name', price=2.0, tax=0.1)
        response = client.put('/items/5?q=queue', json=dict(item))
        assert response.status_code == 200
        assert response.json() == {
            'item_id': 5,
            'name': 'Item name',
            'description': None,
            'price': 2.0,
            'tax': 0.1,
            'q': 'queue',
        }
        pass


class TestModels:
    @pytest.mark.parametrize('model,msg', list(zip(ModelName, ModelMsg)))
    def test_get_model(self, model, msg):
        response = client.get(f'/models/{model.name}')
        pprint(response.json())
        assert response.status_code == 200
        assert response.json() == {'model_name': model, 'message': msg}
        pass


class TestFiles:
    def test_get_file(self):
        file_path = Path('my', 'path', 'file.txt')
        response = client.get(f'/files/{str(file_path)}')
        assert response.status_code == 200
        assert response.json() == {'file_path': str(file_path)}
        pass


class TestMultipleAndQuery:
    def test_read_user_item(self):
        response = client.get('/users/2/items/5/')
        assert response.status_code == 200
        assert response.json() == {
            'item_id': '5',
            'owner_id': 2,
            'description': 'This is an amazing item that has a long description',
        }
        pass

    def test_read_user_query_1(self):
        response = client.get('/users/2/items/5/?q=bar')
        assert response.status_code == 200
        assert response.json() == {
            'item_id': '5',
            'owner_id': 2,
            'q': 'bar',
            'description': 'This is an amazing item that has a long description',
        }
        pass

    def test_read_user_query_2(self):
        response = client.get('/users/2/items/5/?q=bar&short=1')
        assert response.status_code == 200
        assert response.json() == {
            'item_id': '5',
            'owner_id': 2,
            'q': 'bar',
        }
        pass

    def test_read_user_req_query(self):
        response = client.get('/users/2?item_id=foo')
        assert response.status_code == 200
        assert response.json() == {
            'item_id': 'foo',
            'owner_id': 2,
            'description': 'This is an amazing item that has a long description',
        }
        pass

    def test_read_user_req_query_exc(self):
        response = client.get('/users/2')
        assert response.status_code == 422
        assert response.json() == {
            'detail': [
                {
                    'input': None,
                    'loc': ['query', 'item_id'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.2/v/missing',
                }
            ]
        }
        pass


class TestORM:
    def test_create_user_post(self):
        response = client.post('/users/', json={'email': 'foo@bar.com', 'password': 'mypassword', 'item': None})
        pprint(response.json())
        assert response.status_code == 200
        assert response.json() == {'email': 'foo@bar.com', 'id': 1, 'is_active': True, 'items': []}
        pass
        pass
