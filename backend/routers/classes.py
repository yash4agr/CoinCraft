"""Teacher classes and student management router."""

from typing import List, Optional
from datetime import datetime
import secrets
import string
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from database import get_async_session
from auth import current_active_user
from models import (
    User,
    Class,
    ClassStudent,
    TeacherProfile,
    ChildProfile,
    UserModuleProgress,
)
from schemas import ClassRead, ClassCreate, ClassUpdate, StudentRead, ClassResponse

router = APIRouter()


def generate_class_code():
    """Generate a unique 8-character class code."""
    return "".join(secrets.choices(string.ascii_uppercase + string.digits, k=8))


@router.get("/teachers/{teacher_id}/classes", response_model=List[ClassRead])
async def get_teacher_classes(
    teacher_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all classes managed by a teacher."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view classes",
        )

    # Get teacher profile
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == teacher_id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()

    if not teacher_profile or teacher_profile.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only view your own classes",
        )

    # Get classes
    stmt = (
        select(Class)
        .where(Class.teacher_id == teacher_profile.id)
        .order_by(Class.created_at.desc())
    )
    result = await session.execute(stmt)
    classes = result.scalars().all()

    enriched_classes = []
    for class_obj in classes:
        student_stmt = select(ClassStudent).where(ClassStudent.class_id == class_obj.id)
        student_result = await session.execute(student_stmt)
        students = student_result.scalars().all()

        class_dict = ClassRead.model_validate(class_obj).model_dump()
        class_dict["students_count"] = len(students)
        class_dict["average_performance"] = 0.0  # TODO: Calculate actual performance

        enriched_classes.append(ClassRead(**class_dict))

    return enriched_classes


@router.post("/teachers/{teacher_id}/classes", response_model=ClassRead)
async def create_class(
    teacher_id: str,
    class_data: ClassCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new class for a teacher."""
    if current_user.role != "teacher" or current_user.id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can create classes",
        )

    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == teacher_id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()

    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found"
        )

    class_code = generate_class_code()

    new_class = Class(
        teacher_id=teacher_profile.id, class_code=class_code, **class_data.model_dump()
    )
    session.add(new_class)
    await session.commit()
    await session.refresh(new_class)

    class_dict = ClassRead.model_validate(new_class).model_dump()
    class_dict["students_count"] = 0
    class_dict["average_performance"] = 0.0

    return ClassRead(**class_dict)


@router.put("/classes/{class_id}", response_model=ClassRead)
async def update_class(
    class_id: str,
    class_update: ClassUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update class information."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can update classes",
        )

    stmt = (
        select(Class)
        .join(TeacherProfile)
        .where(and_(Class.id == class_id, TeacherProfile.user_id == current_user.id))
    )
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or insufficient permissions",
        )

    update_data = class_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(class_obj, field, value)

    await session.commit()
    await session.refresh(class_obj)

    return ClassRead.model_validate(class_obj)


@router.delete("/classes/{class_id}")
async def delete_class(
    class_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete a class."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can delete classes",
        )

    stmt = (
        select(Class)
        .join(TeacherProfile)
        .where(and_(Class.id == class_id, TeacherProfile.user_id == current_user.id))
    )
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or insufficient permissions",
        )

    await session.delete(class_obj)
    await session.commit()

    return {"message": "Class deleted successfully"}


@router.get("/classes/{class_id}/students", response_model=List[StudentRead])
async def get_class_students(
    class_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all students in a class."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view class students",
        )

    stmt = (
        select(Class)
        .join(TeacherProfile)
        .where(and_(Class.id == class_id, TeacherProfile.user_id == current_user.id))
    )
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or insufficient permissions",
        )

    student_stmt = (
        select(User)
        .join(ClassStudent)
        .join(ChildProfile)
        .where(ClassStudent.class_id == class_id)
        .options(selectinload(User.child_profile))
    )

    student_result = await session.execute(student_stmt)
    students = student_result.scalars().all()

    student_reads = []
    for student in students:
        modules_completed = 0
        total_time_spent = 0

        # Get module progress
        progress_stmt = select(UserModuleProgress).where(
            UserModuleProgress.user_id == student.id
        )
        progress_result = await session.execute(progress_stmt)
        progress_records = progress_result.scalars().all()

        modules_completed = sum(1 for p in progress_records if p.is_completed)
        total_time_spent = sum(p.time_spent for p in progress_records)

        student_read = StudentRead(
            user_id=student.id,
            name=student.name,
            email=student.email,
            avatar_url=student.avatar_url,
            age=student.child_profile.age if student.child_profile else None,
            level=student.child_profile.level if student.child_profile else 1,
            performance_score=75.0,  # TODO: Calculate actual performance
            needs_support=False,  # TODO: Determine based on performance
            last_activity_date=student.child_profile.last_activity_date
            if student.child_profile
            else None,
            modules_completed=modules_completed,
            total_time_spent=total_time_spent,
            progress={},  # TODO: Add detailed progress data
        )
        student_reads.append(student_read)

    return student_reads


@router.post("/classes/{class_id}/students", response_model=StudentRead)
async def add_student_to_class(
    class_id: str,
    student_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Add a student to a class."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can add students to classes",
        )

    stmt = (
        select(Class)
        .join(TeacherProfile)
        .where(and_(Class.id == class_id, TeacherProfile.user_id == current_user.id))
    )
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or insufficient permissions",
        )

    student_id = student_data["student_id"]

    student_stmt = select(User).join(ChildProfile).where(User.id == student_id)
    student_result = await session.execute(student_stmt)
    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )

    existing_stmt = select(ClassStudent).where(
        and_(ClassStudent.class_id == class_id, ClassStudent.student_id == student_id)
    )
    existing_result = await session.execute(existing_stmt)
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Student already in class"
        )

    # Add student to class
    class_student = ClassStudent(class_id=class_id, student_id=student_id)
    session.add(class_student)
    await session.commit()

    # Return student info
    return StudentRead(
        user_id=student.id,
        name=student.name,
        email=student.email,
        avatar_url=student.avatar_url,
        age=student.child_profile.age,
        level=student.child_profile.level,
        performance_score=0.0,
        needs_support=False,
        last_activity_date=student.child_profile.last_activity_date,
        modules_completed=0,
        total_time_spent=0,
        progress={},
    )


@router.delete("/classes/{class_id}/students/{student_id}")
async def remove_student_from_class(
    class_id: str,
    student_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Remove a student from a class."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can remove students from classes",
        )

    # Verify class ownership
    stmt = (
        select(Class)
        .join(TeacherProfile)
        .where(and_(Class.id == class_id, TeacherProfile.user_id == current_user.id))
    )
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or insufficient permissions",
        )

    # Get class student record
    class_student_stmt = select(ClassStudent).where(
        and_(ClassStudent.class_id == class_id, ClassStudent.student_id == student_id)
    )
    class_student_result = await session.execute(class_student_stmt)
    class_student = class_student_result.scalar_one_or_none()

    if not class_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found in class"
        )

    await session.delete(class_student)
    await session.commit()

    return {"message": "Student removed from class successfully"}
