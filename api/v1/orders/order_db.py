from sqlalchemy.orm import Session

from api.v1.database.tables import TableOrders
from api.v1.users.user_db import User
from api.v1.models import FunctionResult


class Order:
    @classmethod
    def GetOrder(cls, session: Session, id: int) -> FunctionResult:
        order = session.query(TableOrders).filter(TableOrders.id == id).first()

        if order is None:
            result = FunctionResult(error="Order with id={0} does not exist".format(id))
        else:
            result = FunctionResult(success=True, result=order)

        return result

    @classmethod
    def Create(cls, session: Session, buyer_id: int, seller_id: int, amount: int) -> FunctionResult:
        buyer = User.GetUser(session, buyer_id)
        if buyer is None:
            return FunctionResult(error="Buyer with id={0} is not exist".format(buyer_id))

        seller = User.GetUser(session, seller_id)
        if seller is None:
            return FunctionResult(error="Seller with id={0} is not exist".format(seller_id))

        order = TableOrders(id=None, buyer_id=buyer_id, seller_id=seller_id, amount=amount, active=True)

        session.add(order)
        session.commit()
        session.refresh(order)

        result = FunctionResult(success=True, result=cls.Serialize(session, order))

        return result

    @classmethod
    def Read(cls, session: Session, id: int) -> FunctionResult:
        OrderSearchResult = cls.GetOrder(session, id)
        if not OrderSearchResult.success:
            result = OrderSearchResult
        else:
            result = FunctionResult(success=True, result=cls.Serialize(session, OrderSearchResult.result))

        return result

    @classmethod
    def Update(cls, session: Session, id, buyer_id: int, seller_id: int, amount: int, active: bool) -> FunctionResult:
        buyer = User.GetUser(session, buyer_id)
        if buyer is None:
            return FunctionResult(error="Buyer with id={0} is not exist".format(buyer_id))

        seller = User.GetUser(session, seller_id)
        if seller is None:
            return FunctionResult(error="Seller with id={0} is not exist".format(seller_id))

        OrderSearchResult = cls.GetOrder(session, id)

        result = OrderSearchResult

        if OrderSearchResult.success:
            order = OrderSearchResult.result

            order.buyer_id = buyer_id
            order.seller_id = seller_id
            order.amount = amount
            order.active = active

            session.commit()

            session.refresh(order)

            OrderSearchResult.result = cls.Serialize(session, order)

        return result

    @classmethod
    def Delete(cls, session: Session, id) -> FunctionResult:
        OrderSearchResult = cls.GetOrder(session, id)

        result = OrderSearchResult
        if OrderSearchResult.success:
            order = OrderSearchResult.result

            session.delete(order)
            session.commit()

            OrderSearchResult.result = None

        return result

    @classmethod
    def List(cls, session: Session) -> FunctionResult:
        return FunctionResult(success=True, result=[cls.Serialize(session, order) for order in session.query(TableOrders).all()])

    @classmethod
    def Serialize(cls, session: Session, instance):
        buyer = User.GetUser(session, instance.buyer_id)
        seller = User.GetUser(session, instance.seller_id)
        return {"id": instance.id, "buyer": buyer.nickname, "seller": seller.nickname, "amount": instance.amount, "active": instance.active}
