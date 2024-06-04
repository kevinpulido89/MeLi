"""This module contains the base models for the application."""

from typing import Literal

from pydantic import BaseModel


class Country(BaseModel):
    """This class represents a country object."""

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
