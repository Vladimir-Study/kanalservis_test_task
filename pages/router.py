from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from orders.router import get_data_orders

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)


templates = Jinja2Templates(directory="templates")


@router.get("/home")
def get_home_page(request: Request):
    return templates.TemplateResponse("base.html", {'request': request})