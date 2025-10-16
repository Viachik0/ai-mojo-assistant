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
import logging
from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy import func, and_, or_
from app.models.homework_submission import HomeworkSubmission

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, session: Optional[AsyncSession] = None):
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

    # Analytics query methods
    async def get_grades_by_student(
        self, 
        student_id: int, 
        days: Optional[int] = None,
        subject: Optional[str] = None
    ) -> List[Dict]:
        """Get grades for a student with optional filters"""
        try:
            query = select(Grade).where(Grade.student_id == student_id)
            
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                query = query.where(Grade.date >= cutoff_date)
            
            if subject:
                query = query.where(Grade.subject == subject)
            
            query = query.order_by(Grade.date.desc())
            result = await self.session.execute(query)
            grades = result.scalars().all()
            
            return [
                {
                    "id": g.id,
                    "value": g.value,
                    "date": g.date.isoformat() if g.date else None,
                    "subject": g.subject,
                    "student_id": g.student_id,
                    "teacher_id": g.teacher_id,
                    "lesson_id": g.lesson_id
                }
                for g in grades
            ]
        except Exception as e:
            logger.error(f"Error getting grades for student {student_id}: {e}")
            return []
    
    async def get_attendance_by_student(
        self, 
        student_id: int, 
        days: Optional[int] = None
    ) -> List[Dict]:
        """Get attendance records for a student"""
        try:
            query = select(Attendance).where(Attendance.student_id == student_id)
            
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                query = query.where(Attendance.date >= cutoff_date)
            
            query = query.order_by(Attendance.date.desc())
            result = await self.session.execute(query)
            records = result.scalars().all()
            
            return [
                {
                    "id": a.id,
                    "student_id": a.student_id,
                    "lesson_id": a.lesson_id,
                    "present": a.present,
                    "date": a.date.isoformat() if a.date else None
                }
                for a in records
            ]
        except Exception as e:
            logger.error(f"Error getting attendance for student {student_id}: {e}")
            return []
    
    async def get_homework_by_student(
        self, 
        student_id: int, 
        days: Optional[int] = None
    ) -> List[Dict]:
        """Get homework assignments for a student"""
        try:
            # Join with lessons to get student's class homework
            query = select(Homework).join(Lesson)
            
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                query = query.where(Homework.due_date >= cutoff_date)
            
            query = query.order_by(Homework.due_date.desc())
            result = await self.session.execute(query)
            homework = result.scalars().all()
            
            return [
                {
                    "id": h.id,
                    "title": h.title,
                    "description": h.description,
                    "due_date": h.due_date.isoformat() if h.due_date else None,
                    "lesson_id": h.lesson_id,
                    "teacher_id": h.teacher_id
                }
                for h in homework
            ]
        except Exception as e:
            logger.error(f"Error getting homework for student {student_id}: {e}")
            return []
    
    async def get_grade_trends(
        self, 
        student_id: int, 
        subject: str, 
        days: int = 30
    ) -> Dict:
        """Analyze grade trends for a student in a subject"""
        try:
            grades = await self.get_grades_by_student(student_id, days, subject)
            
            if not grades:
                return {
                    "subject": subject,
                    "average": 0,
                    "trend": "no_data",
                    "count": 0
                }
            
            values = [g["value"] for g in grades]
            average = sum(values) / len(values)
            
            # Calculate trend (compare first half vs second half)
            mid = len(values) // 2
            if mid > 0:
                first_half_avg = sum(values[:mid]) / mid
                second_half_avg = sum(values[mid:]) / (len(values) - mid)
                
                if second_half_avg > first_half_avg + 0.5:
                    trend = "improving"
                elif second_half_avg < first_half_avg - 0.5:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            return {
                "subject": subject,
                "average": round(average, 2),
                "trend": trend,
                "count": len(grades),
                "latest_grade": values[0] if values else None,
                "highest_grade": max(values) if values else None,
                "lowest_grade": min(values) if values else None
            }
        except Exception as e:
            logger.error(f"Error analyzing grade trends: {e}")
            return {
                "subject": subject,
                "average": 0,
                "trend": "error",
                "count": 0
            }
    
    async def get_attendance_stats(
        self, 
        student_id: int, 
        days: int = 30
    ) -> Dict:
        """Calculate attendance statistics for a student"""
        try:
            records = await self.get_attendance_by_student(student_id, days)
            
            if not records:
                return {
                    "total_lessons": 0,
                    "present_count": 0,
                    "absent_count": 0,
                    "attendance_rate": 0
                }
            
            present_count = sum(1 for r in records if r["present"])
            total_lessons = len(records)
            attendance_rate = (present_count / total_lessons * 100) if total_lessons > 0 else 0
            
            return {
                "total_lessons": total_lessons,
                "present_count": present_count,
                "absent_count": total_lessons - present_count,
                "attendance_rate": round(attendance_rate, 2)
            }
        except Exception as e:
            logger.error(f"Error calculating attendance stats: {e}")
            return {
                "total_lessons": 0,
                "present_count": 0,
                "absent_count": 0,
                "attendance_rate": 0
            }
    
    async def get_homework_completion_rate(
        self, 
        student_id: int, 
        days: int = 30
    ) -> Dict:
        """Calculate homework completion rate for a student"""
        try:
            # Get homework assigned in the period
            cutoff_date = datetime.now() - timedelta(days=days)
            
            query = select(Homework).join(Lesson).where(
                Homework.due_date >= cutoff_date
            )
            result = await self.session.execute(query)
            homework_list = result.scalars().all()
            
            if not homework_list:
                return {
                    "total_assignments": 0,
                    "completed_count": 0,
                    "completion_rate": 0,
                    "overdue_count": 0
                }
            
            total_assignments = len(homework_list)
            
            # Get submissions for this student
            submission_query = select(HomeworkSubmission).where(
                and_(
                    HomeworkSubmission.student_id == student_id,
                    HomeworkSubmission.homework_id.in_([h.id for h in homework_list])
                )
            )
            submission_result = await self.session.execute(submission_query)
            submissions = submission_result.scalars().all()
            
            completed_count = sum(1 for s in submissions if s.is_completed)
            
            # Count overdue assignments
            now = datetime.now()
            submitted_ids = {s.homework_id for s in submissions if s.is_completed}
            overdue_count = sum(
                1 for h in homework_list 
                if h.due_date < now and h.id not in submitted_ids
            )
            
            completion_rate = (completed_count / total_assignments * 100) if total_assignments > 0 else 0
            
            return {
                "total_assignments": total_assignments,
                "completed_count": completed_count,
                "completion_rate": round(completion_rate, 2),
                "overdue_count": overdue_count
            }
        except Exception as e:
            logger.error(f"Error calculating homework completion: {e}")
            return {
                "total_assignments": 0,
                "completed_count": 0,
                "completion_rate": 0,
                "overdue_count": 0
            }
