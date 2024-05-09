from typing import Annotated

from pydantic import Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema


class Atleta(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome do atleta", examples="Joao", max_length=50)
    ]
    cpf: Annotated[
        str, Field(description="CPF do atleta", examples="08667676892", max_length=11)
    ]
    idade: Annotated[int, Field(description="Idade do atleta", examples="21")]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", examples="80.6")]
    altura: Annotated[
        PositiveFloat, Field(description="Altura do atleta", examples="1.81")
    ]
    sexo: Annotated[
        str, Field(description="Sexo do atleta", examples="M", max_length=1)
    ]
