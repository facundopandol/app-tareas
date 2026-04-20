from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO = BASE_DIR / "tareas.json"


class TaskCreate(BaseModel):
    titulo: str


def cargar_tareas():
    if not ARCHIVO.exists():
        return []

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"Error al cargar tareas: {e}")
        return []


def guardar_tareas(tareas):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(tareas, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar tareas: {e}")
        raise HTTPException(status_code=500, detail="No se pudieron guardar las tareas")


def generar_id(tareas):
    if not tareas:
        return 1
    return max(tarea["id"] for tarea in tareas) + 1


@app.get("/")
def inicio():
    return {"mensaje": "Backend funcionando"}


@app.get("/tasks")
def obtener_tareas():
    return cargar_tareas()


@app.post("/tasks")
def agregar_tarea(task: TaskCreate):
    titulo = task.titulo.strip()

    if not titulo:
        raise HTTPException(status_code=400, detail="La tarea no puede estar vacía")

    tareas = cargar_tareas()

    if any(t["titulo"].lower() == titulo.lower() for t in tareas):
        raise HTTPException(status_code=400, detail="La tarea ya existe")

    nueva_tarea = {
        "id": generar_id(tareas),
        "titulo": titulo,
        "completada": False
    }

    tareas.append(nueva_tarea)
    guardar_tareas(tareas)

    return {"mensaje": "Tarea agregada correctamente", "tarea": nueva_tarea}


@app.delete("/tasks/{task_id}")
def eliminar_tarea(task_id: int):
    tareas = cargar_tareas()

    tarea_encontrada = next((t for t in tareas if t["id"] == task_id), None)

    if not tarea_encontrada:
        raise HTTPException(status_code=404, detail="La tarea no existe")

    tareas = [t for t in tareas if t["id"] != task_id]
    guardar_tareas(tareas)

    return {"mensaje": "Tarea eliminada correctamente"}


@app.put("/tasks/{task_id}/toggle")
def toggle_tarea(task_id: int):
    tareas = cargar_tareas()

    tarea_encontrada = next((t for t in tareas if t["id"] == task_id), None)

    if not tarea_encontrada:
        raise HTTPException(status_code=404, detail="La tarea no existe")

    tarea_encontrada["completada"] = not tarea_encontrada["completada"]
    guardar_tareas(tareas)

    return {"mensaje": "Estado de tarea actualizado", "tarea": tarea_encontrada}