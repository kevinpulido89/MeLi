from typing import Literal

from pydantic import BaseModel


class Country(BaseModel):
    country: Literal[
        "Chile",
        "Ecuador",
        "Nicaragua",
        "Perú",
        "Colombia",
        "Cuba",
        "Bolivia",
        "Venezuela",
        "Uruguay",
        "Panamá",
        "Argentina",
        "Brasil",
        "Costa Rica",
        "Guatemala",
        "Dominicana",
        "El Salvador",
        "Paraguay",
        "Mexico",
        "Honduras",
    ]
