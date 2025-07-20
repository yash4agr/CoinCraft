"""Teacher management router for CoinCraft."""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from database import get_async_session
from auth import current_active_user, get_user_manager, UserManager
from models import (
    User, TeacherProfile, Class, ClassStudent, Module, ModuleSection, 
    QuizQuestion, QuizOption, UserModuleProgress, Transaction, Goal, Achievement, UserAchievement
)
from schemas import UserRead

router = APIRouter()

# Teacher-specific data models
class ClassSummary:
    def __init__(self, class_obj: Class, student_count: int, avg_performance: float):
        self.id = class_obj.id
        self.name = class_obj.name
        self.grade = class_obj.grade
        self.description = class_obj.description
        self.student_count = student_count
        self.avg_performance = avg_performance
        self.created_at = class_obj.created_at

class StudentSummary:
    def __init__(self, user: User, progress_data: dict):
        self.id = user.id
        self.name = user.name
        self.avatar = user.avatar_url
        self.grade = progress_data.get('grade', 0)
        self.performance = progress_data.get('performance', 0)
        self.needs_support = progress_data.get('needs_support', False)
        self.last_activity = progress_data.get('last_activity')
        self.progress = progress_data.get('progress', {})

class ModuleSummary:
    def __init__(self, module: Module, stats: dict):
        self.id = module.id
        self.title = module.title
        self.description = module.description
        self.difficulty = module.difficulty
        self.duration = module.estimated_duration
        self.category = module.category
        self.published = module.is_published
        self.completion_rate = stats.get('completion_rate', 0)
        self.avg_score = stats.get('avg_score', 0)

@router.get("/dashboard", response_model=dict)
async def get_teacher_dashboard(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get teacher dashboard data including classes overview and analytics."""
    
    # Verify user is a teacher
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can access this endpoint"
        )
    
    # Get teacher profile 
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()
    
    if not teacher_profile:
     
        teacher_profile = TeacherProfile(
            user_id=current_user.id,
            school_name="",
            grade_level="",
            subject=""
        )
        session.add(teacher_profile)
        await session.commit()
    
    # Get teacher's classes
    classes_stmt = select(Class).where(Class.teacher_id == teacher_profile.id)
    classes_result = await session.execute(classes_stmt)
    classes_data = classes_result.scalars().all()
    
    print(f"[BACKEND] Teacher Dashboard: Found {len(classes_data)} classes for teacher {current_user.id}")
    
    classes = []
    total_students = 0
    total_performance = 0
    students_needing_support = 0
    
    for class_obj in classes_data:
        # Get students in this class
        students_stmt = select(ClassStudent).where(ClassStudent.class_id == class_obj.id)
        students_result = await session.execute(students_stmt)
        class_students = students_result.scalars().all()
        
        student_count = len(class_students)
        total_students += student_count
        
        # Calculate class performance
        class_performance = 0
        class_students_needing_support = 0
        
        if student_count > 0:
            for class_student in class_students:
                # Get student's overall performance
                student_user_stmt = select(User).where(User.id == class_student.student_id)
                student_result = await session.execute(student_user_stmt)
                student_user = student_result.scalar_one_or_none()
                
                if student_user:
                 
                    progress_stmt = select(UserModuleProgress).where(
                        UserModuleProgress.user_id == student_user.id
                    )
                    progress_result = await session.execute(progress_stmt)
                    student_progress = progress_result.scalars().all()
                    
                    if student_progress:
                        completed_modules = [p for p in student_progress if p.is_completed]
                        if completed_modules:
                            avg_score = sum(p.score or 0 for p in completed_modules) / len(completed_modules)
                            class_performance += avg_score
                            
                            
                            if avg_score < 70:
                                class_students_needing_support += 1
                        else:
                            class_performance += 0 
                    else:
                        class_performance += 0 
            
            class_performance = class_performance / student_count if student_count > 0 else 0
            students_needing_support += class_students_needing_support
        
        total_performance += class_performance
        
        class_summary = {
            "id": class_obj.id,
            "name": class_obj.name,
            "grade": class_obj.grade,
            "description": class_obj.description,
            "student_count": student_count,
            "avg_performance": round(class_performance, 1),
            "students_needing_support": class_students_needing_support,
            "created_at": class_obj.created_at.isoformat()
        }
        classes.append(class_summary)
    
   
    overall_avg_performance = total_performance / len(classes) if classes else 0
    
    return {
        "teacher": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "school": teacher_profile.school_name,
            "grade_level": teacher_profile.grade_level,
            "subject": teacher_profile.subject,
            "avatar": current_user.avatar_url
        },
        "classes": classes,
        "analytics": {
            "total_classes": len(classes),
            "total_students": total_students,
            "avg_performance": round(overall_avg_performance, 1),
            "students_needing_support": students_needing_support
        }
    }

@router.post("/classes", response_model=dict)
async def create_class(
    class_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new class."""
    
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can create classes"
        )
    
    # Get teacher profile
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()
    
    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )
    
    # Generate unique class code
    import secrets
    import string
    class_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    # Create class
    new_class = Class(
        name=class_data['name'],
        teacher_id=teacher_profile.id,
        description=class_data.get('description', ''),
        class_code=class_code,
        is_active=True
    )
    
    session.add(new_class)
    await session.commit()
    
    print(f"[BACKEND] Created class: {new_class.name} (ID: {new_class.id})")
    
    return {
        "message": "Class created successfully",
        "class": {
            "id": new_class.id,
            "name": new_class.name,
            "description": new_class.description,
            "class_code": new_class.class_code,
            "grade": new_class.grade,
            "created_at": new_class.created_at.isoformat()
        }
    }

@router.get("/classes", response_model=List[dict])
async def get_teacher_classes(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all classes for the teacher."""
    
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view classes"
        )
    
    # Get teacher profile
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()
    
    if not teacher_profile:
        return []
    
    # Get classes
    classes_stmt = select(Class).where(Class.teacher_id == teacher_profile.id)
    classes_result = await session.execute(classes_stmt)
    classes = classes_result.scalars().all()
    
    classes_data = []
    for class_obj in classes:
        # Get student count
        students_stmt = select(ClassStudent).where(ClassStudent.class_id == class_obj.id)
        students_result = await session.execute(students_stmt)
        student_count = len(students_result.scalars().all())
        
        # Calculate average performance
        avg_performance = 0
        if student_count > 0:
            # This would need more complex calculation based on student progress
            # For now, return a default value
            avg_performance = 75.0
        
        classes_data.append({
            "id": class_obj.id,
            "name": class_obj.name,
            "description": class_obj.description,
            "class_code": class_obj.class_code,
            "grade": class_obj.grade,
            "student_count": student_count,
            "avg_performance": avg_performance,
            "is_active": class_obj.is_active,
            "created_at": class_obj.created_at.isoformat()
        })
    
    return classes_data

@router.get("/classes/{class_id}", response_model=dict)
async def get_class_details(
    class_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get detailed information about a specific class."""
    
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view class details"
        )
    
    # Get teacher profile
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()
    
    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )
    
    # Get class
    class_stmt = select(Class).where(
        and_(Class.id == class_id, Class.teacher_id == teacher_profile.id)
    )
    class_result = await session.execute(class_stmt)
    class_obj = class_result.scalar_one_or_none()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Get students in this class
    students_stmt = select(ClassStudent, User).join(
        User, ClassStudent.student_id == User.id
    ).where(ClassStudent.class_id == class_id)
    students_result = await session.execute(students_stmt)
    students_data = students_result.all()
    
    students = []
    for class_student, user in students_data:
      
        progress_stmt = select(UserModuleProgress).where(
            UserModuleProgress.user_id == user.id
        )
        progress_result = await session.execute(progress_stmt)
        progress_data = progress_result.scalars().all()
        
        
        performance = 0
        needs_support = False
        if progress_data:
            completed_modules = [p for p in progress_data if p.is_completed]
            if completed_modules:
                performance = sum(p.score or 0 for p in completed_modules) / len(completed_modules)
                needs_support = performance < 70
        
        students.append({
            "id": user.id,
            "name": user.name,
            "avatar": user.avatar_url,
            "grade": class_obj.grade,
            "performance": round(performance, 1),
            "needs_support": needs_support,
            "last_activity": user.updated_at.isoformat(),
            "progress": {
                str(p.module_id): {
                    "completed": p.is_completed,
                    "score": p.score or 0,
                    "time_spent": p.time_spent or 0
                } for p in progress_data
            }
        })
    
    return {
        "id": class_obj.id,
        "name": class_obj.name,
        "description": class_obj.description,
        "class_code": class_obj.class_code,
        "grade": class_obj.grade,
        "students": students,
        "avg_performance": sum(s['performance'] for s in students) / len(students) if students else 0,
        "created_at": class_obj.created_at.isoformat()
    }

@router.post("/classes/{class_id}/students", response_model=dict)
async def add_student_to_class(
    class_id: str,
    student_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Add a student to a class."""
    
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can add students to classes"
        )
    
  
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()
    
    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
        )
    
    class_stmt = select(Class).where(
        and_(Class.id == class_id, Class.teacher_id == teacher_profile.id)
    )
    class_result = await session.execute(class_stmt)
    class_obj = class_result.scalar_one_or_none()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    
    student_email = student_data.get('email')
    student_stmt = select(User).where(User.email == student_email)
    student_result = await session.execute(student_stmt)
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    
    existing_stmt = select(ClassStudent).where(
        and_(ClassStudent.class_id == class_id, ClassStudent.student_id == student.id)
    )
    existing_result = await session.execute(existing_stmt)
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already in this class"
        )
    
    # Add student to class
    class_student = ClassStudent(
        class_id=class_id,
        student_id=student.id
    )
    
    session.add(class_student)
    await session.commit()
    
    return {
        "message": "Student added to class successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "avatar": student.avatar_url
        }
    }

@router.post("/modules", response_model=dict)
async def create_module(
    module_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new learning module with enhanced content (sections, activities, quiz)."""
    
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can create modules"
        )
    
    try:
        # Create module
        new_module = Module(
            title=module_data['title'],
            description=module_data['description'],
            category=module_data.get('category', 'General'),
            difficulty=module_data.get('difficulty', 'beginner'),
            estimated_duration=module_data.get('duration', 30),
            points_reward=module_data.get('points_reward', 0),
            created_by=current_user.id,
            is_published=module_data.get('published', False)
        )
        
        session.add(new_module)
        await session.flush()  # Get the module ID
        
        # Create sections if provided
        sections_data = []
        if 'sections' in module_data and module_data['sections']:
            for i, section_data in enumerate(module_data['sections']):
                section = ModuleSection(
                    module_id=new_module.id,
                    title=section_data['title'],
                    type=section_data.get('type', 'lesson'),
                    content=section_data.get('content', ''),
                    order_index=section_data.get('orderIndex', i + 1),
                    points_reward=0
                )
                session.add(section)
                sections_data.append({
                    "title": section.title,
                    "type": section.type,
                    "content": section.content,
                    "duration": section_data.get('duration', ''),
                    "orderIndex": section.order_index
                })
        

        quiz_data = []
        if 'quiz' in module_data and module_data['quiz']:
            # Create a quiz section first
            quiz_section = ModuleSection(
                module_id=new_module.id,
                title="Module Quiz",
                type="quiz",
                content="Knowledge check for this module",
                order_index=len(module_data.get('sections', [])) + 1,
                points_reward=0
            )
            session.add(quiz_section)
            await session.flush() 
            
            for i, question_data in enumerate(module_data['quiz']):
                question = QuizQuestion(
                    section_id=quiz_section.id,
                    question_text=question_data['question'],
                    explanation=question_data.get('explanation', ''),
                    points=1,
                    order_index=i + 1
                )
                session.add(question)
                await session.flush() 
                
                # Create options
                options_data = []
                for j, option_data in enumerate(question_data.get('options', [])):
                    option = QuizOption(
                        question_id=question.id,
                        option_text=option_data['text'],
                        is_correct=option_data.get('isCorrect', False),
                        order_index=j + 1
                    )
                    session.add(option)
                    options_data.append({
                        "text": option.option_text,
                        "isCorrect": option.is_correct
                    })
                
                quiz_data.append({
                    "question": question.question_text,
                    "type": question_data.get('type', 'multiple_choice'),
                    "options": options_data,
                    "explanation": question.explanation
                })
        
        await session.commit()
        
        print(f"[BACKEND] Created enhanced module: {new_module.title} (ID: {new_module.id})")
        print(f"[BACKEND] - Sections: {len(sections_data)}")
        print(f"[BACKEND] - Activities: {len(module_data.get('activities', []))}")
        print(f"[BACKEND] - Quiz questions: {len(quiz_data)}")
        
        return {
            "message": "Module created successfully",
            "module": {
                "id": new_module.id,
                "title": new_module.title,
                "description": new_module.description,
                "category": new_module.category,
                "difficulty": new_module.difficulty,
                "duration": new_module.estimated_duration,
                "ageGroup": module_data.get('targetAge', module_data.get('ageGroup', 'Unknown')),
                "skills": module_data.get('skills', module_data.get('keyTopics', [])),
                "points_reward": new_module.points_reward,
                "published": new_module.is_published,
                "created_at": new_module.created_at.isoformat(),
                "sections": sections_data,
                "activities": module_data.get('activities', []),
                "quiz": quiz_data,
                "learningObjectives": module_data.get('learningObjectives', []),
                "prerequisites": module_data.get('prerequisites', []),
                "keyTopics": module_data.get('keyTopics', [])
            }
        }
        
    except Exception as e:
        await session.rollback()
        print(f"[BACKEND] Error creating module: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create module: {str(e)}"
        )

@router.get("/modules", response_model=List[dict])
async def get_teacher_modules(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all modules created by the teacher."""
    
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view modules"
        )
    

    modules_stmt = select(Module).where(Module.created_by == current_user.id)
    modules_result = await session.execute(modules_stmt)
    modules = modules_result.scalars().all()
    
    modules_data = []
    for module in modules:
        progress_stmt = select(UserModuleProgress).where(UserModuleProgress.module_id == module.id)
        progress_result = await session.execute(progress_stmt)
        progress_data = progress_result.scalars().all()
        
        completion_rate = 0
        avg_score = 0
        
        if progress_data:
            completed = [p for p in progress_data if p.is_completed]
            completion_rate = len(completed) / len(progress_data) * 100
            if completed:
                avg_score = sum(p.score or 0 for p in completed) / len(completed)


        sections_stmt = select(ModuleSection).where(
            and_(ModuleSection.module_id == module.id, ModuleSection.type != 'quiz')
        ).order_by(ModuleSection.order_index)
        sections_result = await session.execute(sections_stmt)
        sections = sections_result.scalars().all()
        
        sections_data = []
        for section in sections:
            sections_data.append({
                "title": section.title,
                "type": section.type,
                "content": section.content,
                "duration": "10 minutes", 
                "orderIndex": section.order_index
            })

        # Get quiz questions
        quiz_stmt = select(ModuleSection).where(
            and_(ModuleSection.module_id == module.id, ModuleSection.type == 'quiz')
        )
        quiz_section_result = await session.execute(quiz_stmt)
        quiz_section = quiz_section_result.scalar_one_or_none()
        
        quiz_data = []
        if quiz_section:
            questions_stmt = select(QuizQuestion).where(
                QuizQuestion.section_id == quiz_section.id
            ).order_by(QuizQuestion.order_index)
            questions_result = await session.execute(questions_stmt)
            questions = questions_result.scalars().all()
            
            for question in questions:
                options_stmt = select(QuizOption).where(
                    QuizOption.question_id == question.id
                ).order_by(QuizOption.order_index)
                options_result = await session.execute(options_stmt)
                options = options_result.scalars().all()
                
                options_data = []
                for option in options:
                    options_data.append({
                        "text": option.option_text,
                        "isCorrect": option.is_correct
                    })
                
                quiz_data.append({
                    "question": question.question_text,
                    "type": "multiple_choice",  # Default type
                    "options": options_data,
                    "explanation": question.explanation or ""
                })
        
        modules_data.append({
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "category": module.category,
            "difficulty": module.difficulty,
            "duration": module.estimated_duration,
            "ageGroup": "Unknown",  
            "skills": [],  
            "points_reward": module.points_reward,
            "published": module.is_published,
            "completion_rate": round(completion_rate, 1),
            "avg_score": round(avg_score, 1),
            "created_at": module.created_at.isoformat(),
            "updated_at": module.updated_at.isoformat(),
            "sections": sections_data,
            "activities": [],  
            "quiz": quiz_data,
            "learningObjectives": [], 
            "prerequisites": [],
            "keyTopics": []
        })
    
    return modules_data

@router.get("/analytics/performance", response_model=dict)
async def get_performance_analytics(
    timeframe: str = "month",
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get performance analytics for the teacher's classes."""
    
    if current_user.role != 'teacher':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can view analytics"
        )
    
    # Calculate timeframe
    now = datetime.utcnow()
    if timeframe == "week":
        start_date = now - timedelta(days=7)
    elif timeframe == "month":
        start_date = now - timedelta(days=30)
    elif timeframe == "quarter":
        start_date = now - timedelta(days=90)
    else:  # year
        start_date = now - timedelta(days=365)
    
    # Get teacher profile
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()
    
    if not teacher_profile:
        return {
            "overall_performance": 0,
            "class_performance": [],
            "student_progress": [],
            "module_completion": []
        }
    
    # Get teacher's classes
    classes_stmt = select(Class).where(Class.teacher_id == teacher_profile.id)
    classes_result = await session.execute(classes_stmt)
    classes = classes_result.scalars().all()
    
    class_performance = []
    overall_performance = 0
    total_students = 0
    
    for class_obj in classes:
        # Get students in class
        students_stmt = select(ClassStudent).where(ClassStudent.class_id == class_obj.id)
        students_result = await session.execute(students_stmt)
        class_students = students_result.scalars().all()
        
        class_avg = 0
        if class_students:
            for class_student in class_students:
                progress_stmt = select(UserModuleProgress).where(
                    and_(
                        UserModuleProgress.user_id == class_student.student_id,
                        UserModuleProgress.completed_at >= start_date
                    )
                )
                progress_result = await session.execute(progress_stmt)
                progress_data = progress_result.scalars().all()
                
                if progress_data:
                    completed = [p for p in progress_data if p.is_completed]
                    if completed:
                        student_avg = sum(p.score or 0 for p in completed) / len(completed)
                        class_avg += student_avg
            
            class_avg = class_avg / len(class_students) if class_students else 0
            total_students += len(class_students)
        
        overall_performance += class_avg
        
        class_performance.append({
            "class_id": class_obj.id,
            "class_name": class_obj.name,
            "avg_performance": round(class_avg, 1),
            "student_count": len(class_students)
        })
    
    overall_performance = overall_performance / len(classes) if classes else 0
    
    return {
        "overall_performance": round(overall_performance, 1),
        "class_performance": class_performance,
        "total_students": total_students,
        "timeframe": timeframe
    }