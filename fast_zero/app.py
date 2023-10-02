from fastapi import FastAPI, HTTPException, status

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

DATABASE = []


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': DATABASE}


@app.post(
    '/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
async def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(DATABASE) + 1)
    DATABASE.append(user_with_id)
    print(DATABASE)
    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(DATABASE) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    DATABASE[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(DATABASE) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    del DATABASE[user_id - 1]

    return {'detail': 'User deleted'}
