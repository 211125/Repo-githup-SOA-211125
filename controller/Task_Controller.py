from fastapi import APIRouter, Depends, HTTPException, Path, Body, Query
from sqlalchemy.orm import Session
from model.model import Task
from router.schemas import TaskCreate, TaskRead, TaskUpdate
from config.database import get_db
from datetime import datetime
from typing import List

router = APIRouter()




@router.post("/tasks/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Verificar si el campo 'title' o 'description' están vacíos o en blanco
    if not task.title.strip() or not task.description.strip():
        raise HTTPException(status_code=400, detail="Los campos 'title' y 'description' no pueden estar vacíos")
    
    current_time = datetime.now()  # Obtiene la fecha y hora actual
    new_task = Task(**task.dict(), created_at=current_time)  # Agrega la fecha de creación
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
@router.get("/tasks/{task_id}/", response_model=TaskRead)
def read_task(task_id: int = Path(..., title="The ID of the task to retrieve"), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.deleted == False).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.get("/tasks/", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.deleted == False).all()
    return tasks

@router.put("/tasks/complete/{task_id}/", response_model=TaskRead)
def complete_task(task_id: int = Path(..., title="The ID of the task to mark as completed"), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True  # Marcar la tarea como completada
    db.commit()
    return task


@router.put("/tasks/{task_id}/", response_model=TaskRead)
def update_task(task_id: int = Path(..., title="The ID of the task to update"), task_update: TaskUpdate = Body(...), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_update.dict().items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}/", response_model=TaskRead)
def delete_task(task_id: int = Path(..., title="The ID of the task to delete"), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.deleted = True  # Marcar la tarea como eliminada
    db.commit()
    return task



@router.get("/tasks/pagina", response_model=List[TaskRead])
def list_tasks(
    page: int = Query(1, description="Número de página", ge=1),  # Página predeterminada es 1
    page_size: int = Query(10, description="Tamaño de página", ge=1, le=100),  # Tamaño de página predeterminado es 10
    db: Session = Depends(get_db)
):
    # Calcular el índice de inicio y fin para la paginación
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Consulta las tareas en el rango especificado
    tasks = db.query(Task).filter(Task.deleted == False).slice(start_index, end_index).all()

    return tasks