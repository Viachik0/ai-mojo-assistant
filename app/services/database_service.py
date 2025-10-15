from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from typing import List, Optional
from app.models.user import User, Role
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.grade import Grade
from app.models.lesson import Lesson
from app.models.attendance import Attendance
from app.models.homework import Homework

class DatabaseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # User CRUD
    async def create_user(self, name: str, email: str, role: Role) -> User:
        user = User(name=name, email=email, role=role)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_users_by_role(self, role: Role) -> List[User]:
        result = await self.session.execute(select(User).where(User.role == role))
        return result.scalars().all()
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.session.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_user(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None, role: Optional[Role] = None) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if role is not None:
            user.role = role
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True

    # Student CRUD
    async def create_student(self, user_id: int, class_name: str) -> Student:
        student = Student(user_id=user_id, class_name=class_name)
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def get_students_by_class(self, class_name: str) -> List[Student]:
        result = await self.session.execute(select(Student).where(Student.class_name == class_name))
        return result.scalars().all()
    
    async def get_student_by_id(self, student_id: int) -> Optional[Student]:
        result = await self.session.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()
    
    async def get_students(self, skip: int = 0, limit: int = 100) -> List[Student]:
        result = await self.session.execute(select(Student).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_student(self, student_id: int, class_name: Optional[str] = None) -> Optional[Student]:
        student = await self.get_student_by_id(student_id)
        if not student:
            return None
        if class_name is not None:
            student.class_name = class_name
        await self.session.commit()
        await self.session.refresh(student)
        return student
    
    async def delete_student(self, student_id: int) -> bool:
        student = await self.get_student_by_id(student_id)
        if not student:
            return False
        await self.session.delete(student)
        await self.session.commit()
        return True
    
    # Teacher CRUD
    async def create_teacher(self, user_id: int, subjects: List[str]) -> Teacher:
        teacher = Teacher(user_id=user_id, subjects=subjects)
        self.session.add(teacher)
        await self.session.commit()
        await self.session.refresh(teacher)
        return teacher
    
    async def get_teacher_by_id(self, teacher_id: int) -> Optional[Teacher]:
        result = await self.session.execute(select(Teacher).where(Teacher.id == teacher_id))
        return result.scalar_one_or_none()
    
    async def get_teachers(self, skip: int = 0, limit: int = 100) -> List[Teacher]:
        result = await self.session.execute(select(Teacher).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_teacher(self, teacher_id: int, subjects: Optional[List[str]] = None) -> Optional[Teacher]:
        teacher = await self.get_teacher_by_id(teacher_id)
        if not teacher:
            return None
        if subjects is not None:
            teacher.subjects = subjects
        await self.session.commit()
        await self.session.refresh(teacher)
        return teacher
    
    async def delete_teacher(self, teacher_id: int) -> bool:
        teacher = await self.get_teacher_by_id(teacher_id)
        if not teacher:
            return False
        await self.session.delete(teacher)
        await self.session.commit()
        return True

    # Grade CRUD
    async def create_grade(self, student_id: int, teacher_id: int, subject: str, grade: str, date, lesson_topic: Optional[str] = None) -> Grade:
        grade_obj = Grade(student_id=student_id, teacher_id=teacher_id, subject=subject, grade=grade, date=date, lesson_topic=lesson_topic)
        self.session.add(grade_obj)
        await self.session.commit()
        await self.session.refresh(grade_obj)
        return grade_obj

    async def get_grades_for_student(self, student_id: int, days: int = 7) -> List[Grade]:
        from datetime import datetime, timedelta
        since = datetime.now() - timedelta(days=days)
        result = await self.session.execute(select(Grade).where(Grade.student_id == student_id, Grade.date >= since))
        return result.scalars().all()
    
    async def get_grade_by_id(self, grade_id: int) -> Optional[Grade]:
        result = await self.session.execute(select(Grade).where(Grade.id == grade_id))
        return result.scalar_one_or_none()
    
    async def get_grades(self, skip: int = 0, limit: int = 100) -> List[Grade]:
        result = await self.session.execute(select(Grade).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_grade(self, grade_id: int, subject: Optional[str] = None, grade: Optional[str] = None, 
                          date = None, lesson_topic: Optional[str] = None) -> Optional[Grade]:
        grade_obj = await self.get_grade_by_id(grade_id)
        if not grade_obj:
            return None
        if subject is not None:
            grade_obj.subject = subject
        if grade is not None:
            grade_obj.grade = grade
        if date is not None:
            grade_obj.date = date
        if lesson_topic is not None:
            grade_obj.lesson_topic = lesson_topic
        await self.session.commit()
        await self.session.refresh(grade_obj)
        return grade_obj
    
    async def delete_grade(self, grade_id: int) -> bool:
        grade_obj = await self.get_grade_by_id(grade_id)
        if not grade_obj:
            return False
        await self.session.delete(grade_obj)
        await self.session.commit()
        return True

    # Lesson CRUD
    async def create_lesson(self, date, subject: str, class_name: str, teacher_id: int, topic: Optional[str] = None) -> Lesson:
        lesson = Lesson(date=date, subject=subject, class_name=class_name, teacher_id=teacher_id, topic=topic)
        self.session.add(lesson)
        await self.session.commit()
        await self.session.refresh(lesson)
        return lesson
    
    async def get_lesson_by_id(self, lesson_id: int) -> Optional[Lesson]:
        result = await self.session.execute(select(Lesson).where(Lesson.id == lesson_id))
        return result.scalar_one_or_none()
    
    async def get_lessons(self, skip: int = 0, limit: int = 100) -> List[Lesson]:
        result = await self.session.execute(select(Lesson).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_lesson(self, lesson_id: int, date = None, subject: Optional[str] = None, 
                           class_name: Optional[str] = None, topic: Optional[str] = None) -> Optional[Lesson]:
        lesson = await self.get_lesson_by_id(lesson_id)
        if not lesson:
            return None
        if date is not None:
            lesson.date = date
        if subject is not None:
            lesson.subject = subject
        if class_name is not None:
            lesson.class_name = class_name
        if topic is not None:
            lesson.topic = topic
        await self.session.commit()
        await self.session.refresh(lesson)
        return lesson
    
    async def delete_lesson(self, lesson_id: int) -> bool:
        lesson = await self.get_lesson_by_id(lesson_id)
        if not lesson:
            return False
        await self.session.delete(lesson)
        await self.session.commit()
        return True

    # Attendance CRUD
    async def mark_attendance(self, student_id: int, lesson_id: int, present: bool = True, date = None) -> Attendance:
        from datetime import datetime as dt
        if date is None:
            date = dt.now()
        attendance = Attendance(student_id=student_id, lesson_id=lesson_id, present=present, date=date)
        self.session.add(attendance)
        await self.session.commit()
        await self.session.refresh(attendance)
        return attendance
    
    async def get_attendance_by_id(self, attendance_id: int) -> Optional[Attendance]:
        result = await self.session.execute(select(Attendance).where(Attendance.id == attendance_id))
        return result.scalar_one_or_none()
    
    async def get_attendance_records(self, skip: int = 0, limit: int = 100) -> List[Attendance]:
        result = await self.session.execute(select(Attendance).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_attendance(self, attendance_id: int, present: Optional[bool] = None) -> Optional[Attendance]:
        attendance = await self.get_attendance_by_id(attendance_id)
        if not attendance:
            return None
        if present is not None:
            attendance.present = present
        await self.session.commit()
        await self.session.refresh(attendance)
        return attendance
    
    async def delete_attendance(self, attendance_id: int) -> bool:
        attendance = await self.get_attendance_by_id(attendance_id)
        if not attendance:
            return False
        await self.session.delete(attendance)
        await self.session.commit()
        return True

    # Homework CRUD
    async def create_homework(self, lesson_id: int, title: str, description: str, due_date, teacher_id: int) -> Homework:
        homework = Homework(lesson_id=lesson_id, title=title, description=description, due_date=due_date, teacher_id=teacher_id)
        self.session.add(homework)
        await self.session.commit()
        await self.session.refresh(homework)
        return homework
    
    async def get_homework_by_id(self, homework_id: int) -> Optional[Homework]:
        result = await self.session.execute(select(Homework).where(Homework.id == homework_id))
        return result.scalar_one_or_none()
    
    async def get_homework_list(self, skip: int = 0, limit: int = 100) -> List[Homework]:
        result = await self.session.execute(select(Homework).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_homework(self, homework_id: int, title: Optional[str] = None, 
                             description: Optional[str] = None, due_date = None) -> Optional[Homework]:
        homework = await self.get_homework_by_id(homework_id)
        if not homework:
            return None
        if title is not None:
            homework.title = title
        if description is not None:
            homework.description = description
        if due_date is not None:
            homework.due_date = due_date
        await self.session.commit()
        await self.session.refresh(homework)
        return homework
    
    async def delete_homework(self, homework_id: int) -> bool:
        homework = await self.get_homework_by_id(homework_id)
        if not homework:
            return False
        await self.session.delete(homework)
        await self.session.commit()
        return True
