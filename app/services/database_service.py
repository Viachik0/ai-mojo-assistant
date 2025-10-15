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

    # Lesson CRUD
    async def create_lesson(self, date, subject: str, class_name: str, teacher_id: int, topic: Optional[str] = None) -> Lesson:
        lesson = Lesson(date=date, subject=subject, class_name=class_name, teacher_id=teacher_id, topic=topic)
        self.session.add(lesson)
        await self.session.commit()
        await self.session.refresh(lesson)
        return lesson

    # Attendance CRUD
    async def mark_attendance(self, student_id: int, lesson_id: int, present: bool = True) -> Attendance:
        attendance = Attendance(student_id=student_id, lesson_id=lesson_id, present=present)
        self.session.add(attendance)
        await self.session.commit()
        await self.session.refresh(attendance)
        return attendance

    # Homework CRUD
    async def create_homework(self, lesson_id: int, description: str, due_date) -> Homework:
        homework = Homework(lesson_id=lesson_id, description=description, due_date=due_date)
        self.session.add(homework)
        await self.session.commit()
        await self.session.refresh(homework)
        return homework
