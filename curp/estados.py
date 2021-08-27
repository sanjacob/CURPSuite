"""
Entidades de la República Mexicana y su código ISO
"""

from __future__ import annotations

from typing import Optional, TypedDict


class RegionData(TypedDict):
    name: str
    iso: Optional[str]


estados: dict[str, RegionData] = {
  "AS": {
    "name": "Aguascalientes",
    "iso": "MX-AGU"
  },
  "BC": {
    "name": "Baja California",
    "iso": "MX-BCN"
  },
  "BS": {
    "name": "Baja California Sur",
    "iso": "MX-BCS"
  },
  "CC": {
    "name": "Campeche",
    "iso": "MX-CAM"
  },
  "CL": {
    "name": "Coahuila de Zaragoza",
    "iso": "MX-COA"
  },
  "CM": {
    "name": "Colima",
    "iso": "MX-COL"
  },
  "CS": {
    "name": "Chiapas",
    "iso": "MX-CHP"
  },
  "CH": {
    "name": "Chihuahua",
    "iso": "MX-CHH"
  },
  "DF": {
    "name": "Ciudad de México",
    "iso": "MX-CMX"
  },
  "DG": {
    "name": "Durango",
    "iso": "MX-DUR"
  },
  "GT": {
    "name": "Guanajuato",
    "iso": "MX-GUA"
  },
  "GR": {
    "name": "Guerrero",
    "iso": "MX-GRO"
  },
  "HG": {
    "name": "Hidalgo",
    "iso": "MX-HID"
  },
  "JC": {
    "name": "Jalisco",
    "iso": "MX-JAL"
  },
  "MC": {
    "name": "México",
    "iso": "MX-MEX"
  },
  "MN": {
    "name": "Michoacán de Ocampo",
    "iso": "MX-MIC"
  },
  "MS": {
    "name": "Morelos",
    "iso": "MX-MOR"
  },
  "NT": {
    "name": "Nayarit",
    "iso": "MX-NAY"
  },
  "NL": {
    "name": "Nuevo León",
    "iso": "MX-NLE"
  },
  "OC": {
    "name": "Oaxaca",
    "iso": "MX-OAX"
  },
  "PL": {
    "name": "Puebla",
    "iso": "MX-PUE"
  },
  "QT": {
    "name": "Querétaro",
    "iso": "MX-QUE"
  },
  "QR": {
    "name": "Quintana Roo",
    "iso": "MX-ROO"
  },
  "SP": {
    "name": "San Luis Potosí",
    "iso": "MX-SLP"
  },
  "SL": {
    "name": "Sinaloa",
    "iso": "MX-SIN"
  },
  "SR": {
    "name": "Sonora",
    "iso": "MX-SON"
  },
  "TC": {
    "name": "Tabasco",
    "iso": "MX-TAB"
  },
  "TS": {
    "name": "Tamaulipas",
    "iso": "MX-TAM"
  },
  "TL": {
    "name": "Tlaxcala",
    "iso": "MX-TLA"
  },
  "VZ": {
    "name": "Veracruz de Ignacio de la Llave",
    "iso": "MX-VER"
  },
  "YN": {
    "name": "Yucatán",
    "iso": "MX-YUC"
  },
  "ZS": {
    "name": "Zacatecas",
    "iso": "MX-ZAC"
  },
  "NE": {
    "name": "Extranjero",
    "iso": None
  }
}
