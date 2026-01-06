from typing import Annotated
from pydantic import Field, UUID4
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoInsert(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Centro de Treinamento 1", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example="Rua x, 123", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="João Silva", max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Centro de Treinamento 1", max_length=20)]
    
class CentroTreinamentoOut(CentroTreinamentoInsert):
    id: Annotated[UUID4, Field(description="ID do centro de treinamento")]
