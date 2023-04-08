from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pages.router import router as router_pages
from orders.router import router as router_orders
from pathlib import Path

base_dir = Path(__file__).parent
app = FastAPI()
app.mount("/static", StaticFiles(directory=base_dir.joinpath('static')), name="static")
app.include_router(router_pages)
app.include_router(router_orders)
