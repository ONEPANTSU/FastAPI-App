from fastapi import FastAPI
from loguru import logger

logger.add(
    "app.log",
    format="{time}\t|\t{level}\t|\t{message}",
    level="INFO",
    rotation="10MB",
    compression="zip",
)

app = FastAPI(title="Trading App")

users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
]

trades = [
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 123,
        "amount": 2.12,
    },
    {
        "id": 2,
        "user_id": 1,
        "currency": "BTC",
        "side": "sell",
        "price": 123,
        "amount": 2.12,
    },
]


@app.get("/users/{user_id}", tags=["users"])
@logger.catch
def get_user(user_id: int):
    logger.info(f"GET\t/users/{user_id}\t|\tparams: user_id={user_id}")
    return [user for user in users if user.get("id") == user_id]


@app.get("/trades", tags=["trades"])
@logger.catch
def get_trades(limit: int = 10, offset: int = 0):
    logger.info(f"GET\t/trades\t|\tparams: limit={limit}, offset={offset}")
    return trades[offset:][:limit]


@app.post("/users/{user_id}", tags=["users"])
@logger.catch
def change_user_name(user_id: int, new_name: str):
    logger.info(f"POST\t/users/{user_id}\t|\tparams: user_id={user_id}, new_name={new_name}")
    current_user = list(filter(lambda user: user.get("id") == user_id, users))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}
