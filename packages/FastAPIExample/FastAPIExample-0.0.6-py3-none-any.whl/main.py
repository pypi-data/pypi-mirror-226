"""
MYSQL_DB_NAME=SQLAlchemyExample;MYSQL_HOST=localhost;MYSQL_ROOT_PWD=N0tS0S3curePassw0rd;MYSQL_TCP_PORT_EXAMPLES=50002;SQLALCHEMY_SILENCE_UBER_WARNING=1

"""
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from dbdef import engine
from dbdef import SessionLocal
from models import fake_items_db
from models import ModelName
from schemas import ItemSchema

# from models import Item

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/ping')
async def ping():
    return {'msg': 'pong'}


@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str | None = None):
    if q:
        return {'item_id': item_id, 'q': q}
    return {'item_id': item_id}


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.post('/items/')
async def create_item(item: ItemSchema):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def create_item(item_id: int, item: ItemSchema, q: str | None = None):
    result = {'item_id': item_id, **item.model_dump()}
    if q:
        result.update({'q': q})
    return result


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    # You can compare it with the enumeration member in your created enum ModelName
    if model_name is ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}
    # You can get the actual value (a str in this case) using model_name.value
    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'LeCNN all the images'}

    return {'model_name': model_name, 'message': 'Have some residuals'}


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}


@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, 'owner_id': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long description'})
    return item


@app.get('/users/{user_id}')
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, 'owner_id': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long description'})
    return item


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)
