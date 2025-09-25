from fastapi import FastAPI, Query
import httpx
from .openrouter_client import call_openrouter

app = FastAPI()
KONSULENT_API_URL = "http://konsulent-api:8000/konsulenter"

@app.get("/tilgjengelige-konsulenter/sammendrag")
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
                "Du er en AI assistent for bemanning. Skriv i klar og konsis menneskeleselig sammendrag"
                "hvor konsulentene er tilgjengelige gitt kriterier gitt av bruker. Svar som i dette eksempelformatet: "
                "Fant 2 konsulenter med minst 50% tilgjengelighet og ferdigheten 'python'. Anna K. har 60% tilgjengelighet. Leo T. har 80% tilgjengelighet."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Ledige Konsulenter: {filtrert}. Minimum tilgjengelighet: {min_tilgjengelighet_prosent}. "
                f"Påkrevd ferdighet: {pakrevd_ferdighet}."
            ),
        },
    ]

    svar = await call_openrouter(messages, model=model)

    return {
        "model": model,
        "sammendrag": svar["choices"][0]["message"]["content"],
    }