"""Clasificación de correos por temas usando palabras clave.

Las categorías y sus palabras clave se leen de ``categorias.json`` (junto a
este archivo) para que se puedan editar sin tocar el código.
"""
import json
import os
import re
import unicodedata

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CATEGORIAS = os.path.join(CARPETA, "categorias.json")

OTROS = "Otros"
SPAM = "Spam"


def normalizar(texto):
    """Minúsculas y sin tildes, para comparar 'Psicología' con 'psicologia'."""
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower()


def cargar_categorias(ruta=ARCHIVO_CATEGORIAS):
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    categorias = {}
    for nombre, info in datos["categorias"].items():
        categorias[nombre] = {
            "palabras": [normalizar(p) for p in info.get("palabras", [])],
            "remitentes": [normalizar(r) for r in info.get("remitentes", [])],
        }
    return categorias


def _cuenta(palabras, texto):
    total = 0
    for p in palabras:
        # Coincidencia al inicio de palabra: "farmac" encaja con "farmacia",
        # "farmacéutico", "farmacología"...
        total += len(re.findall(r"(?<![a-z0-9])" + re.escape(p), texto))
    return total


def clasificar(remitente, asunto, cuerpo, categorias, en_carpeta_spam=False,
               reglas_usuario=None):
    """Devuelve el nombre de la categoría para un correo.

    Prioridad:
      1. Lo que el propio usuario decidió para ese remitente.
      2. Si Gmail ya lo tiene en la carpeta de spam -> Spam.
      3. Remitentes conocidos de cada categoría (p. ej. dominio de la uni).
      4. Puntuación por palabras clave (asunto pesa más que el cuerpo).
    """
    rem = normalizar(remitente)
    if reglas_usuario:
        for clave, cat in reglas_usuario.items():
            if clave and clave in rem:
                return cat
    if en_carpeta_spam:
        return SPAM

    for nombre, info in categorias.items():
        if any(r and r in rem for r in info["remitentes"]):
            return nombre

    asu = normalizar(asunto)
    cue = normalizar(cuerpo)[:20000]
    mejor, mejor_puntos = OTROS, 0
    for nombre, info in categorias.items():
        puntos = (3 * _cuenta(info["palabras"], asu)
                  + 2 * _cuenta(info["palabras"], rem)
                  + _cuenta(info["palabras"], cue))
        if puntos > mejor_puntos:
            mejor, mejor_puntos = nombre, puntos
    # El spam necesita algo más de evidencia para no "comerse" correos buenos.
    if mejor == SPAM and mejor_puntos < 3:
        return OTROS
    return mejor
