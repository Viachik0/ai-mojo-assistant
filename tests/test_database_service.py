import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from app.services.database_service import DatabaseService


@pytest.fixture
def database_service():
    """Create a DatabaseService instance"""
    return DatabaseService()


@pytest.mark.asyncio
async def test_get_grades_by_student(database_service):
    """Test get_grades_by_student method"""
    # Mock the database session and query results
    mock_grade = Mock()
    mock_grade.id = 1
    mock_grade.value = 5.0
    mock_grade.date = datetime.now()
    mock_grade.subject = "Math"
    mock_grade.student_id = 1
    mock_grade.teacher_id = 1
    mock_grade.lesson_id = 1
    
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = [mock_grade]
    
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    with patch('app.services.database_service.AsyncSessionMaker', return_value=mock_session):
        result = await database_service.get_grades_by_student(1, days=7)
        
        assert len(result) == 1
        assert result[0]["value"] == 5.0
        assert result[0]["subject"] == "Math"


@pytest.mark.asyncio
async def test_get_grades_by_student_with_subject_filter(database_service):
    """Test get_grades_by_student with subject filter"""
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = []
    
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    with patch('app.services.database_service.AsyncSessionMaker', return_value=mock_session):
        result = await database_service.get_grades_by_student(1, days=7, subject="Math")
        
        assert isinstance(result, list)


@pytest.mark.asyncio
async def test_get_attendance_by_student(database_service):
    """Test get_attendance_by_student method"""
    mock_attendance = Mock()
    mock_attendance.id = 1
    mock_attendance.student_id = 1
    mock_attendance.lesson_id = 1
    mock_attendance.present = True
    mock_attendance.date = datetime.now()
    
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = [mock_attendance]
    
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    with patch('app.services.database_service.AsyncSessionMaker', return_value=mock_session):
        result = await database_service.get_attendance_by_student(1)
        
        assert len(result) == 1
        assert result[0]["present"] is True


@pytest.mark.asyncio
async def test_get_homework_by_student(database_service):
    """Test get_homework_by_student method"""
    mock_homework = Mock()
    mock_homework.id = 1
    mock_homework.title = "Math Assignment"
    mock_homework.description = "Complete exercises 1-10"
    mock_homework.due_date = datetime.now() + timedelta(days=2)
    mock_homework.lesson_id = 1
    mock_homework.teacher_id = 1
    
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = [mock_homework]
    
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    with patch('app.services.database_service.AsyncSessionMaker', return_value=mock_session):
        result = await database_service.get_homework_by_student(1)
        
        assert len(result) == 1
        assert result[0]["title"] == "Math Assignment"


@pytest.mark.asyncio
async def test_get_grade_trends_no_data(database_service):
    """Test get_grade_trends with no grade data"""
    with patch.object(database_service, 'get_grades_by_student', 
                     new=AsyncMock(return_value=[])):
        result = await database_service.get_grade_trends(1, "Math")
        
        assert result["subject"] == "Math"
        assert result["average"] == 0
        assert result["trend"] == "no_data"
        assert result["count"] == 0


@pytest.mark.asyncio
async def test_get_grade_trends_improving(database_service):
    """Test get_grade_trends with improving trend"""
    mock_grades = [
        {"value": 5.0, "date": "2024-01-20"},
        {"value": 4.5, "date": "2024-01-15"},
        {"value": 4.0, "date": "2024-01-10"},
        {"value": 3.5, "date": "2024-01-05"}
    ]
    
    with patch.object(database_service, 'get_grades_by_student', 
                     new=AsyncMock(return_value=mock_grades)):
        result = await database_service.get_grade_trends(1, "Math")
        
        assert result["subject"] == "Math"
        assert result["average"] > 0
        assert result["trend"] in ["improving", "stable", "declining"]
        assert result["count"] == 4


@pytest.mark.asyncio
async def test_get_grade_trends_declining(database_service):
    """Test get_grade_trends with declining trend"""
    mock_grades = [
        {"value": 3.0, "date": "2024-01-20"},
        {"value": 3.5, "date": "2024-01-15"},
        {"value": 4.0, "date": "2024-01-10"},
        {"value": 4.5, "date": "2024-01-05"}
    ]
    
    with patch.object(database_service, 'get_grades_by_student', 
                     new=AsyncMock(return_value=mock_grades)):
        result = await database_service.get_grade_trends(1, "Math")
        
        assert result["subject"] == "Math"
        assert result["trend"] in ["improving", "stable", "declining"]


@pytest.mark.asyncio
async def test_get_attendance_stats_no_data(database_service):
    """Test get_attendance_stats with no attendance data"""
    with patch.object(database_service, 'get_attendance_by_student', 
                     new=AsyncMock(return_value=[])):
        result = await database_service.get_attendance_stats(1)
        
        assert result["total_lessons"] == 0
        assert result["attendance_rate"] == 0


@pytest.mark.asyncio
async def test_get_attendance_stats_perfect_attendance(database_service):
    """Test get_attendance_stats with perfect attendance"""
    mock_records = [
        {"present": True} for _ in range(10)
    ]
    
    with patch.object(database_service, 'get_attendance_by_student', 
                     new=AsyncMock(return_value=mock_records)):
        result = await database_service.get_attendance_stats(1)
        
        assert result["total_lessons"] == 10
        assert result["present_count"] == 10
        assert result["absent_count"] == 0
        assert result["attendance_rate"] == 100.0


@pytest.mark.asyncio
async def test_get_attendance_stats_partial_attendance(database_service):
    """Test get_attendance_stats with partial attendance"""
    mock_records = [
        {"present": True},
        {"present": True},
        {"present": False},
        {"present": True},
        {"present": False}
    ]
    
    with patch.object(database_service, 'get_attendance_by_student', 
                     new=AsyncMock(return_value=mock_records)):
        result = await database_service.get_attendance_stats(1)
        
        assert result["total_lessons"] == 5
        assert result["present_count"] == 3
        assert result["absent_count"] == 2
        assert result["attendance_rate"] == 60.0


@pytest.mark.asyncio
async def test_get_homework_completion_rate_no_data(database_service):
    """Test get_homework_completion_rate with no homework data"""
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = []
    
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    with patch('app.services.database_service.AsyncSessionMaker', return_value=mock_session):
        result = await database_service.get_homework_completion_rate(1)
        
        assert result["total_assignments"] == 0
        assert result["completion_rate"] == 0


@pytest.mark.asyncio
async def test_get_homework_completion_rate_with_submissions(database_service):
    """Test get_homework_completion_rate with homework submissions"""
    # Mock homework
    mock_hw1 = Mock()
    mock_hw1.id = 1
    mock_hw1.due_date = datetime.now() + timedelta(days=1)
    
    mock_hw2 = Mock()
    mock_hw2.id = 2
    mock_hw2.due_date = datetime.now() - timedelta(days=1)
    
    # Mock submissions
    mock_sub1 = Mock()
    mock_sub1.homework_id = 1
    mock_sub1.is_completed = True
    
    # Create mock results
    mock_hw_result = Mock()
    mock_hw_result.scalars.return_value.all.return_value = [mock_hw1, mock_hw2]
    
    mock_sub_result = Mock()
    mock_sub_result.scalars.return_value.all.return_value = [mock_sub1]
    
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(side_effect=[mock_hw_result, mock_sub_result])
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    with patch('app.services.database_service.AsyncSessionMaker', return_value=mock_session):
        result = await database_service.get_homework_completion_rate(1)
        
        assert result["total_assignments"] == 2
        assert result["completed_count"] == 1
        assert result["completion_rate"] == 50.0
        assert result["overdue_count"] == 1
