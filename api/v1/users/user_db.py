from sqlalchemy import or_
from sqlalchemy.orm import Session

from api.v1.database.tables import TableUsers


class User:
    @classmethod
    def FindUser(cls, session: Session, nickname, email):
        return session.query(TableUsers).filter(or_(TableUsers.nickname == nickname, TableUsers.email == email)).first()

    @classmethod
    def GetUser(cls, session: Session, id: int):
        return session.query(TableUsers).filter(TableUsers.id == id).first()

    @classmethod
    def Create(cls, session: Session, nickname, email, password):
        user = cls.FindUser(session, nickname, email)

        if user is None:
            user = TableUsers(id=None, nickname=nickname, email=email, password=password)

            session.add(user)
            session.commit()
            session.refresh(user)

            result = cls.Serialize(user)
        else:
            result = None

        return result

    @classmethod
    def Read(cls, session: Session, id: int):
        user = cls.GetUser(session, id)
        if user is None:
            return None

        return cls.Serialize(user)

    @classmethod
    def Update(cls, session: Session, id, nickname, email, password):
        user = cls.GetUser(session, id)

        if user is None:
            result = None
        else:
            user.nickname = nickname
            user.email = email
            user.password = password

            session.commit()

            session.refresh(user)

            result = cls.Serialize(user)

        return result

    @classmethod
    def Delete(cls, session: Session, id):
        user = cls.GetUser(session, id)

        result = False
        if user is not None:
            session.delete(user)
            session.commit()
            result = True

        return result

    @classmethod
    def List(cls, session: Session):
        return [cls.Serialize(user) for user in session.query(TableUsers).all()]

    @classmethod
    def Serialize(cls, instance):
        return {"id": instance.id, "nickname": instance.nickname, "email": instance.email}
