from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.atleta.schemas import AtletaInsert, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.future import select
from pydantic import UUID4

router = APIRouter()

@router.post(
    "/",
    summary="Cria um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DataBaseDependency,
    atleta_ins: AtletaInsert = Body(...)
):
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=atleta_ins.categoria.nome))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria nao encontrada"
        )

    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=atleta_ins.centro_treinamento.nome))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Centro de treinamento nao encontrado"
        )

    atleta = (await db_session.execute(
        select(AtletaModel).filter_by(cpf=atleta_ins.cpf))
    ).scalars().first()

    if atleta:
        raise HTTPException(
            status_code=status.HTTP_303_BAD_REQUEST, detail="Já existe um atleta cadastrado com o cpf: " + atleta_ins.cpf
        )

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_ins.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao inserir atleta: " + str(e)
        )
    
    return atleta_out


@router.get(
    "/",
    summary="Lista todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut]
)
async def query(db_session: DataBaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (
        await db_session.execute(select(AtletaModel))
    ).scalars().all()

    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
    "/{id}",
    summary="Lista um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def query(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta nao encontrado")

    return AtletaOut.model_validate(atleta)


@router.patch(
    "/{id}",
    summary="Atualiza um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def query(id: UUID4, db_session: DataBaseDependency, atleta_update: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta

@router.delete(
    "/{id}",
    summary="Deleta um atleta pelo id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def query(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    await db_session.delete(atleta)
    await db_session.commit()