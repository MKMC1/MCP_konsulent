from fastapi import FastAPI, Query
import httpx
from .openrouter_client import call_openrouter
from .schemas import SammendragOut
import json

app = FastAPI()
KONSULENT_API_URL = "http://konsulent-api:8000/konsulenter"

@app.get("/tilgjengelige-konsulenter/sammendrag", response_model=SammendragOut)
async def tilgjengelige_konsulenter_sammendrag(
    min_tilgjengelighet_prosent: int = Query(..., description="Minimum tilgjengelighet prosent"),
    pakrevd_ferdighet: str = Query(..., description="Påkrevd ferdighet"),
    model: str = Query("openai/gpt-4o-mini", description="Hvilken OpenRouter modell å bruke"),
):
    
    # hent konsulenter fra konsulent-api
    async with httpx.AsyncClient() as client:
        resp = await client.get(KONSULENT_API_URL)
        resp.raise_for_status()
        konsulenter = resp.json()

    # filtrer konsulenter
    filtrert = [
        k for k in konsulenter
        if pakrevd_ferdighet.lower() in [f.lower() for f in k["ferdigheter"]]
        and (100 - k["belastning_prosent"]) >= min_tilgjengelighet_prosent
    ]
    
    # bygg prompt for OpenRouter
    messages = [
        {
            "role": "system",
            "content": (
                "Du er en AI-assistent for bemanning av konsulenter. Svar kun i JSON-format. "
                "JSON-objektet må inneholde to felter: "
                "'sammendrag' (en menneskeleselig oppsummering av resultatet. Svar som i dette eksempel formatet: "
                "Fant 2 konsulenter med minst 50% tilgjengelighet og ferdigheten 'python'. Anna K. har 60% tilgjengelighet. Leo T. har 80% tilgjengelighet.) "
                "og 'konsulenter' (en liste med objekter for hver konsulent med 'navn', 'tilgjengelighet' og 'ferdighet'). "
            ),
        },
        {
            "role": "user",
            "content": (
                f"Ledige Konsulenter: {filtrert}." 
                f"Minimum tilgjengelighet: {min_tilgjengelighet_prosent}. "
                f"Påkrevd ferdighet: {pakrevd_ferdighet}."
            ),
        },
    ]

    try:
        svar = await call_openrouter(messages, model=model)
        ai_innhold = svar["choices"][0]["message"]["content"]
        data = json.loads(ai_innhold)  # prøv å parse til JSON
        return data
    except Exception:
        # fallback: enkel oppsummering
        if not filtrert:
            return {
                "sammendrag": f"Ingen konsulenter funnet med minst {min_tilgjengelighet_prosent}% tilgjengelighet og ferdigheten '{pakrevd_ferdighet}'.",
                "konsulenter": [],
            }
        return {
            "sammendrag": f"Fant {len(filtrert)} konsulenter med ferdigheten '{pakrevd_ferdighet}'.",
            "konsulenter": [
                {"navn": k["navn"], "tilgjengelighet": f"{100 - k['belastning_prosent']}%"}
                for k in filtrert
            ],
        }