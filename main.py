from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel, Field

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
    {
        "id": 2,
        "role": "investor",
        "name": "John",
        "degree": [
            {"id": 1, "created_at": "2023-06-21T02:35:00", "type_degree": "newbie"}
        ],
    },
    {
        "id": 3,
        "role": "trader",
        "name": "Matt",
        "degree": [
            {"id": 1, "created_at": "2023-05-21T02:35:00", "type_degree": "newbie"},
            {"id": 2, "created_at": "2023-06-21T02:35:00", "type_degree": "expert"},
        ],
    },
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]]


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


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get("/users/{user_id}", tags=["users"], response_model=List[User])
@logger.catch
def get_user(user_id: int):
    logger.info(f"GET\t/users/{user_id}\t|\tparams: user_id={user_id}")
    return [user for user in users if user.get("id") == user_id]


@app.post("/trades", tags=["trades"])
@logger.catch
def post_trades(new_trades: List[Trade]):
    logger.info(f"POST\t/trades\t|\tparams: new_trades={new_trades}")
    trades.extend(new_trades)
    return {"status": 200, "data": trades}
