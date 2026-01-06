from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.categorias.schemas import CategoriaInsert
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="123.456.789-00", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.75)]
    genero: Annotated[str, Field(description="Gênero do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaInsert, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]

class AtletaInsert(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta", example="João", max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", example=25)]
    peso: Annotated[Optional[PositiveFloat], Field(None, description="Peso do atleta", example=70.5)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description="Altura do atleta", example=1.75)]