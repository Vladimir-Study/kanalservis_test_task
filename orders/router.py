from google_services.sheets import GoogleSheets
from quotes.get_quotes import get_quotes
from fastapi import APIRouter, Depends
from orders.models import OrdersDb, OrdersApi, session
from datetime import datetime, date
from tg_bot.bot_message import bot
from config import CHAT_ID, SPREADSHEETS_ID

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.get("/send_message")
def send_message():
    orders = session.query(OrdersDb.order_number).filter(OrdersDb.delivery_date < date.today()).all()
    lst_ord_num = [order[0] for order in orders]
    bot.send_message(CHAT_ID, text=f'Для следующих заказов истек срок: {lst_ord_num}')


@router.get("/get_orders")
def get_data_orders():
    orders = session.query(OrdersDb).all()
    return {
        'orders': orders
    }


@router.get("/update_data")
def update_data():
    try:
        dt_from = datetime.today().replace(hour=8, minute=0, second=0)
        dt_to = datetime.today().replace(hour=8, minute=0, second=3)
        if (dt_from < datetime.now() < dt_to):
            send_message()
        test_sheets_two = GoogleSheets(SPREADSHEETS_ID)
        tcontent = test_sheets_two.read_sheets('lst_one!A2:D1000')
        quotes_rur = get_quotes()
        quotes_rur = float(quotes_rur.replace(',', '.'))
        lst_orders_number = [int(row[1]) for row in tcontent]
        for row in tcontent:
            lst_date = row[3].split('.')
            tb_date = date.fromisoformat(f"{lst_date[2]}-{lst_date[1]}-{lst_date[0]}")
            order = session.query(OrdersDb).filter(OrdersDb.order_number == int(row[1])).all()
            if order == []:
                test_order = OrdersDb(
                    order_number=row[1],
                    price_dollar=row[2],
                    price_rur='{:.2f}'.format(int(row[2])*quotes_rur),
                    delivery_date=tb_date
                )
                session.add(test_order)
                session.commit()
                print('Update or add')
            else:
                comparison = (int(row[1]), float(row[2]), f"{lst_date[2]}-{lst_date[1]}-{lst_date[0]}") == \
                             (order[0].order_number, order[0].price_dollar, order[0].delivery_date.isoformat())
                if not comparison:
                    order[0].price_dollar = row[2]
                    order[0].price_rur = '{:.2f}'.format(int(row[2])*quotes_rur)
                    order[0].delivery_date = tb_date
                    session.commit()
                    print("UPDATE")
        orders = session.query(OrdersDb.order_number).all()
        for on in orders:
            if on[0] not in lst_orders_number:
                delete_obj = session.query(OrdersDb).filter(OrdersDb.order_number == on[0]).all()[-1]
                session.delete(delete_obj)
                session.commit()
                print(f"DELETE: {on[0]}")
        return {
            "status": 200
        }
    except Exception as E:
        return {
            "error": E
        }

