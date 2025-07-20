"""Tasks management router."""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from database import get_async_session
from auth import current_active_user
from models import User, Task, ChildProfile, Transaction
from schemas import TaskRead, TaskCreate, TaskUpdate

router = APIRouter()


@router.get("/parents/{parent_id}/tasks", response_model=List[TaskRead])
async def get_assigned_tasks(
    parent_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get tasks assigned by a parent."""
    if parent_id != current_user.id or current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view their assigned tasks"
        )
    
    # Get tasks assigned by this parent
    stmt = select(Task).where(Task.assigned_by == parent_id).order_by(Task.created_at.desc())
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    
    return [TaskRead.model_validate(task) for task in tasks]


@router.post("/parents/{parent_id}/tasks", response_model=TaskRead)
async def assign_task(
    parent_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Assign a new task to a child."""
    if parent_id != current_user.id or current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can assign tasks"
        )
    

    stmt = select(ChildProfile).where(
        and_(ChildProfile.user_id == task_data.assigned_to, ChildProfile.parent_id == parent_id)
    )
    result = await session.execute(stmt)
    child_profile = result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only assign tasks to your children"
        )
    
    # Create task
    task = Task(
        assigned_by=parent_id,
        **task_data.model_dump()
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    return TaskRead.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task_status(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update task status (complete, approve, reject)."""
    # Get task
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check permissions based on action
    if task_update.status in ["completed", "in_progress"]:

        if current_user.id != task.assigned_to:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigned child can complete tasks"
            )
    elif task_update.status in ["approved", "rejected"]:
 
        if current_user.id != task.assigned_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigning parent can approve/reject tasks"
            )
    else:
 
        if current_user.id != task.assigned_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
    
    # Update task
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
   
    if task_update.status == "completed":
        task.completed_at = datetime.utcnow()
    elif task_update.status == "approved":
        task.approved_at = datetime.utcnow()
        
        # Award coins to child
        stmt = select(ChildProfile).where(ChildProfile.user_id == task.assigned_to)
        result = await session.execute(stmt)
        child_profile = result.scalar_one()
        
        child_profile.coins += task.coins_reward
        
        # Create transaction record
        transaction = Transaction(
            user_id=task.assigned_to,
            type="earn",
            amount=task.coins_reward,
            description=f"Task completed: {task.title}",
            category="task",
            reference_id=task_id,
            reference_type="task"
        )
        session.add(transaction)
    
    await session.commit()
    await session.refresh(task)
    
    return TaskRead.model_validate(task)


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a task."""
    # Get task
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    

    if current_user.id != task.assigned_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the assigning parent can delete tasks"
        )
    
    await session.delete(task)
    await session.commit()
    
    return {"message": "Task deleted successfully"} 