from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1.orders.order_db import Order
from api.v1.models import ResponsePattern, OrderRequestBody, OrderInfoBody, Tags

from api.v1.database.manager import DBManager

orders_v1_api = APIRouter(prefix="/api/v1/orders", tags=[Tags.orders])


@orders_v1_api.get("/", response_class=JSONResponse, tags=[Tags.orders])
async def API_orders_list(session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    return Order.List(session).AsResponsePattern()


@orders_v1_api.get("/{id}", response_class=JSONResponse, tags=[Tags.orders])
async def API_orders_get(id: int = Path(title="order id", description="Идентификатор заказа"),
                         session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    return Order.Read(session, id).AsResponsePattern()


@orders_v1_api.post("/", response_class=JSONResponse, tags=[Tags.orders])
async def API_orders_add(OrderInfo: OrderRequestBody | list[OrderRequestBody],
                         session: Session = Depends(DBManager.GetSession)) -> ResponsePattern | list[ResponsePattern]:
    if type(OrderInfo) is not list:
        OrdersInfoList = [OrderInfo]
    else:
        OrdersInfoList = OrderInfo

    result = list()
    for NewOrderInfo in OrdersInfoList:
        NewOrderCreationResult = Order.Create(session, NewOrderInfo.buyer_id, NewOrderInfo.seller_id,
                                              NewOrderInfo.amount)

        result.append(NewOrderCreationResult.AsResponsePattern())

    if len(result) == 1:
        result = result[0]

    return result


@orders_v1_api.put("/{id}", response_class=JSONResponse, tags=[Tags.orders])
async def API_orders_update(OrderInfo: OrderInfoBody,
                            id: int = Path(title="order id", description="Идентификатор заказа"),
                            session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    return Order.Update(session, id, OrderInfo.buyer_id, OrderInfo.seller_id, OrderInfo.amount,
                        OrderInfo.active).AsResponsePattern()


@orders_v1_api.delete("/{id}", response_class=JSONResponse, tags=[Tags.orders])
async def API_orders_delete(id: int, session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    return Order.Delete(session, id).AsResponsePattern()


@orders_v1_api.patch("/{id}", response_class=JSONResponse, tags=[Tags.orders])
async def API_orders_patch(OrderInfo: OrderInfoBody, id: int, session: Session = Depends(DBManager.GetSession)) -> ResponsePattern:
    OrderSearchResult = Order.GetOrder(session, id)

    result = OrderSearchResult
    if OrderSearchResult.success:
        order = OrderSearchResult.result

        UpdatedFields = OrderInfo.dict(exclude_unset=True)
        if len(UpdatedFields) > 0:
            for key, value in UpdatedFields.items():
                setattr(order, key, value)

            session.commit()
            session.refresh(order)

        OrderSearchResult.result = Order.Serialize(session, order)

    return result.AsResponsePattern()
