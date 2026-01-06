from typing import Annotated
from pydantic import Field, UUID4
from workout_api.contrib.schemas import BaseSchema


class CategoriaInsert(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Categoria 1", max_length=10)]
    
class CategoriaOut(CategoriaInsert):
    id: Annotated[UUID4, Field(description="ID da categoria")]