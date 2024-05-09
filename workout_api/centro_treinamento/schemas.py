from typing import Annotated

from pydantic import Field

from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento", examples="CT", max_length=20
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Endereço do centro de treinamento",
            examples="Rua Paraná, 123",
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str,
        Field(
            description="Nome do proprietário", examples="João da Silva", max_length=30
        ),
    ]
