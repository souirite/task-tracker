from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, like
from datetime import datetime
from typing import List, Optional

from backend.database import engine, get_db, Base
from backend.models import Area, Task, PriorityEnum, StatusEnum
from backend.schemas import (
    AreaCreate, AreaUpdate, AreaResponse, AreaWithTasks,
    TaskCreate, TaskUpdate, TaskResponse, TaskStats
)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Task Tracker API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== AREA ENDPOINTS ====================

@app.get("/api/areas", response_model=List[AreaResponse])
def get_areas(db: Session = Depends(get_db)):
    """Get all areas"""
    return db.query(Area).all()


@app.post("/api/areas", response_model=AreaResponse)
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    """Create a new area"""
    db_area = Area(**area.dict())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


@app.get("/api/areas/{area_id}", response_model=AreaWithTasks)
def get_area(area_id: int, db: Session = Depends(get_db)):
    """Get a specific area with its tasks"""
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area


@app.put("/api/areas/{area_id}", response_model=AreaResponse)
def update_area(area_id: int, area: AreaUpdate, db: Session = Depends(get_db)):
    """Update an area"""
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    
    update_data = area.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_area, field, value)
    
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


@app.delete("/api/areas/{area_id}")
def delete_area(area_id: int, db: Session = Depends(get_db)):
    """Delete an area and all its tasks"""
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    
    db.delete(db_area)
    db.commit()
    return {"message": "Area deleted successfully"}


# ==================== TASK ENDPOINTS ====================

@app.get("/api/tasks", response_model=List[TaskResponse])
def get_tasks(
    area_id: int,
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get tasks for an area with optional filtering"""
    query = db.query(Task).filter(Task.area_id == area_id)
    
    if status and status != "all":
        query = query.filter(Task.status == status)
    
    if priority and priority != "all":
        query = query.filter(Task.priority == priority)
    
    if search:
        query = query.filter(Task.description.ilike(f"%{search}%"))
    
    return query.order_by(Task.date_raised).all()


@app.post("/api/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    # Verify area exists
    area = db.query(Area).filter(Area.id == task.area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}


# ==================== STATISTICS ENDPOINT ====================

@app.get("/api/tasks/stats/{area_id}", response_model=TaskStats)
def get_task_stats(area_id: int, db: Session = Depends(get_db)):
    """Get task statistics for an area"""
    tasks = db.query(Task).filter(Task.area_id == area_id).all()
    
    total = len(tasks)
    open_count = len([t for t in tasks if t.status == StatusEnum.OPEN])
    closed_count = len([t for t in tasks if t.status == StatusEnum.CLOSED])
    critical_count = len([t for t in tasks if t.priority == PriorityEnum.CRITICAL])
    
    return TaskStats(
        total=total,
        open=open_count,
        closed=closed_count,
        critical=critical_count
    )


# ==================== HEALTH CHECK ====================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
