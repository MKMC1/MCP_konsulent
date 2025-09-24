from fastapi import FastAPI

app = FastAPI()

CONSULTANT = [
    {"id": 1, "navn": "Anna K.", "ferdigheter": ["python", "sql"], "belastning_prosent": 40},
    {"id": 2, "navn": "Leo T.", "ferdigheter": ["java", "python"], "belastning_prosent": 20},
    {"id": 3, "navn": "Mia L.", "ferdigheter": ["react", "typescript"], "belastning_prosent": 70},
]

@app.get("/konsulenter")
def get_konsulenter():
    return CONSULTANT
