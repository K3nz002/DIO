from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.categorias.schemas import CategoriaInsert, CategoriaOut
from workout_api.categorias.models import CategoriaModel
from sqlalchemy.future import select
from pydantic import UUID4

router = APIRouter()

@router.post(
    "/",
    summary="Cria uma nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut
)
async def post(
    db_session: DataBaseDependency,
    categoria_ins: CategoriaInsert = Body(...)
) -> CategoriaOut:

    categoria_out = CategoriaOut(id=uuid4(), **categoria_ins.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()
    
    return categoria_out


@router.get(
    "/",
    summary="Lista todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut]
)
async def query(db_session: DataBaseDependency) -> list[CategoriaOut]:
    categorias = list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias


@router.get(
    "/{id}",
    summary="Lista uma categoria pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut
)
async def query(id: UUID4, db_session: DataBaseDependency) -> list[CategoriaOut]:
    categoria_out = CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria nao encontrada")

    return categoria_out