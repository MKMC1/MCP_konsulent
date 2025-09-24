from fastapi import FastAPI, Query
import httpx

app = FastAPI()

KONSULENT_API_URL = "http://konsulent-api:8000/konsulenter"

@app.get("/tilgjengelige-konsulenter/sammendrag")
async def tilgjengelige_konsulenter(
    min_tilgjengelighet_prosent: int = Query(..., ge=0, le=100),
    påkrevd_ferdighet: str = Query(...)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(KONSULENT_API_URL)
        konsulenter = response.json()

    tilgjengelige = []
    for k in konsulenter:
        tilgjengelighet = 100 - k["belastning_prosent"]
        if (
            tilgjengelighet >= min_tilgjengelighet_prosent
            and påkrevd_ferdighet.lower() in [f.lower() for f in k["ferdigheter"]]
        ):
            tilgjengelige.append((k["navn"], tilgjengelighet))

    if not tilgjengelige:
        return {"sammendrag": f"Ingen konsulenter med minst {min_tilgjengelighet_prosent}% tilgjengelighet og ferdigheten '{påkrevd_ferdighet}'."}

    sammendrag = (
        f"Fant {len(tilgjengelige)} konsulenter med minst {min_tilgjengelighet_prosent}% tilgjengelighet "
        f"og ferdigheten '{påkrevd_ferdighet}'. "
    )
    sammendrag += " ".join([f"{navn} har {tilg}% tilgjengelighet." for navn, tilg in tilgjengelige])

    return {"sammendrag": sammendrag}
