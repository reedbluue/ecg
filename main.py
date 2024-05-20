from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import csv
import os
from datetime import datetime

app = FastAPI()
csv_file_path = "data.csv"

# Cria o arquivo CSV ao iniciar a aplicação
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "value"])


class ValueModel(BaseModel):
    value: float


@app.get("/")
async def live():
    return "ON LIVE"


@app.post("/add_value/")
async def add_value(value: ValueModel):
    try:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), value.value])
        return {"message": "Value added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download_csv/")
async def download_csv():
    try:
        return FileResponse(path=csv_file_path, filename="data.csv", media_type='text/csv')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
