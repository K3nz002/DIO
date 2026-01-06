from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamentoInsert, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.future import select
from pydantic import UUID4

router = APIRouter()

@router.post(
    "/",
    summary="Cria um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)
async def post(
    db_session: DataBaseDependency,
    centro_treinamento_ins: CentroTreinamentoInsert = Body(...)
) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_ins.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()
    
    return centro_treinamento_out


@router.get(
    "/",
    summary="Lista todos os centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut]
)
async def query(db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento_out = list[CentroTreinamentoOut] = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()
    return centros_treinamento_out


@router.get(
    "/{id}",
    summary="Lista um centro de treinamento pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut
)
async def query(id: UUID4, db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centro_treinamento_out = CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de treinamento nao encontrado")

    return centro_treinamento_out