from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation

from ..main import logger
from .schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


@router.get("/")
@logger.catch
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": [list(row) for row in result.all()],
            "details": None,
        }

        # return result.all()
    except Exception as e:
        return {
                "status": "error",
                "data": None,
                "details": f"{e}",
            }


@router.post("/")
@logger.catch
async def add_specific_operations(
    new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        statement = insert(operation).values(**new_operation.dict())
        await session.execute(statement)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": f"{e}",
        }
