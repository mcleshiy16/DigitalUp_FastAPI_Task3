from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1.users.user_db import User
from api.v1.models import ResponsePattern, UserRequestBody, Tags

from api.v1.database.manager import DBManager

users_v1_api = APIRouter(prefix="/api/v1/users", tags=[Tags.users])


@users_v1_api.get("/", response_class=JSONResponse, tags=[Tags.users])
def API_users_list(session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    return ResponsePattern(success=True, result=User.List(session))


@users_v1_api.get("/{id}", response_class=JSONResponse, tags=[Tags.users])
async def API_user_get(id: int = Path(title="user id", description="Идентификатор пользователя"), session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    UserObject = User.Read(session, id)

    if UserObject is None:
        result = ResponsePattern(error="User with id={0} does not exist".format(id))
    else:
        result = ResponsePattern(success=True, result=UserObject)

    return result


@users_v1_api.post("/", response_class=JSONResponse, tags=[Tags.users])
def API_user_add(UsersInfo: UserRequestBody | list[UserRequestBody], session: Session = Depends(DBManager.GetSession)) -> ResponsePattern | list[ResponsePattern]:
    if type(UsersInfo) is not list:
        UsersInfoList = [UsersInfo]
    else:
        UsersInfoList = UsersInfo

    result = list()
    for NewUserInfo in UsersInfoList:
        NewUserObject = User.Create(session, NewUserInfo.nickname, NewUserInfo.email, NewUserInfo.password)

        if NewUserObject is None:
            UserCreationResult = ResponsePattern(error="nickname={0} & email={1} -> Such user already exist".format(NewUserInfo.nickname, NewUserInfo.email))
        else:
            UserCreationResult = ResponsePattern(result=NewUserObject, success=True)

        result.append(UserCreationResult)

    if len(result) == 1:
        result = result[0]

    return result


@users_v1_api.put("/{id}", response_class=JSONResponse, tags=[Tags.users])
async def API_user_update(UserInfo: UserRequestBody, id: int = Path(title="user id", description="Идентификатор пользователя"), session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    UserObject = User.Update(session, id, UserInfo.nickname, UserInfo.email, UserInfo.password)

    if UserObject is None:
        result = ResponsePattern(error="User with id={0} does not exist".format(id))
    else:
        result = ResponsePattern(result=UserObject, success=True)

    return result


@users_v1_api.delete("/{id}", response_class=JSONResponse, tags=[Tags.users])
async def API_user_delete(id: int, session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    if User.Delete(session, id):
        result = ResponsePattern(success=True)
    else:
        result = ResponsePattern(error="User with id={0} does not exist".format(id))

    return result
