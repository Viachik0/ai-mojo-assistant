import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.services.analysis_service import AnalysisService
from app.integrations.mojo_client import MojoClient


@pytest.fixture
def mock_mojo_client():
    """Create a mock MojoClient"""
    client = Mock(spec=MojoClient)
    client.get_students = AsyncMock(return_value=[
        {"id": 1, "name": "Test Student"}
    ])
    client.get_teachers = AsyncMock(return_value=[
        {"id": 1, "name": "Test Teacher"}
    ])
    client.get_grades = AsyncMock(return_value=[
        {"id": 1, "value": 5.0, "subject": "Math", "date": "2024-01-15"}
    ])
    client.get_missing_grades = AsyncMock(return_value=[])
    client.send_message = AsyncMock(return_value=True)
    client.send_teacher_alert = AsyncMock(return_value=True)
    client.send_parent_report = AsyncMock(return_value=True)
    return client


@pytest.fixture
def analysis_service(mock_mojo_client):
    """Create an AnalysisService instance with mocked dependencies"""
    return AnalysisService(mock_mojo_client)


@pytest.mark.asyncio
async def test_analysis_service_initialization(analysis_service):
    """Test that AnalysisService initializes correctly"""
    assert analysis_service is not None
    assert analysis_service.mojo_client is not None
    assert analysis_service.llm_service is not None
    assert analysis_service.db_service is not None


@pytest.mark.asyncio
async def test_check_missing_grades_no_missing(analysis_service, mock_mojo_client):
    """Test check_missing_grades when no grades are missing"""
    mock_mojo_client.get_missing_grades.return_value = []
    
    await analysis_service.check_missing_grades()
    
    # Should not send any alerts
    mock_mojo_client.send_teacher_alert.assert_not_called()


@pytest.mark.asyncio
async def test_check_missing_grades_with_missing(analysis_service, mock_mojo_client):
    """Test check_missing_grades when grades are missing"""
    mock_mojo_client.get_missing_grades.return_value = [
        {"id": 1, "lesson": "Math"},
        {"id": 2, "lesson": "Physics"}
    ]
    
    await analysis_service.check_missing_grades()
    
    # Should send alert
    mock_mojo_client.send_teacher_alert.assert_called_once()


@pytest.mark.asyncio
async def test_generate_weekly_reports(analysis_service, mock_mojo_client):
    """Test generate_weekly_reports"""
    with patch.object(analysis_service.llm_service, 'analyze_performance', 
                     new=AsyncMock(return_value={"message": "Great progress!"})):
        await analysis_service.generate_weekly_reports()
        
        # Should send report to parent
        mock_mojo_client.send_parent_report.assert_called_once()


@pytest.mark.asyncio
async def test_analyze_student_grades_no_data(analysis_service):
    """Test analyze_student_grades with no grade data"""
    with patch.object(analysis_service.db_service, 'get_grades_by_student',
                     new=AsyncMock(return_value=[])):
        result = await analysis_service.analyze_student_grades(1)
        
        assert result["status"] == "no_data"
        assert result["student_id"] == 1


@pytest.mark.asyncio
async def test_analyze_student_grades_with_data(analysis_service):
    """Test analyze_student_grades with grade data"""
    mock_grades = [
        {"id": 1, "value": 5.0, "subject": "Math", "date": "2024-01-15"},
        {"id": 2, "value": 4.5, "subject": "Math", "date": "2024-01-20"},
        {"id": 3, "value": 4.0, "subject": "Physics", "date": "2024-01-18"}
    ]
    
    mock_trend = {
        "subject": "Math",
        "average": 4.75,
        "trend": "stable",
        "count": 2
    }
    
    with patch.object(analysis_service.db_service, 'get_grades_by_student',
                     new=AsyncMock(return_value=mock_grades)):
        with patch.object(analysis_service.db_service, 'get_grade_trends',
                         new=AsyncMock(return_value=mock_trend)):
            result = await analysis_service.analyze_student_grades(1)
            
            assert result["status"] == "success"
            assert result["student_id"] == 1
            assert result["total_grades"] == 3
            assert result["subjects_count"] == 2
            assert "grade_trends" in result


@pytest.mark.asyncio
async def test_analyze_student_attendance(analysis_service):
    """Test analyze_student_attendance"""
    mock_stats = {
        "total_lessons": 10,
        "present_count": 9,
        "absent_count": 1,
        "attendance_rate": 90.0
    }
    
    with patch.object(analysis_service.db_service, 'get_attendance_stats',
                     new=AsyncMock(return_value=mock_stats)):
        with patch.object(analysis_service.llm_service, 'generate_alert',
                         new=AsyncMock(return_value={"alert": "Good attendance"})):
            result = await analysis_service.analyze_student_attendance(1)
            
            assert result["status"] == "success"
            assert result["attendance_stats"]["attendance_rate"] == 90.0


@pytest.mark.asyncio
async def test_analyze_student_attendance_low_rate(analysis_service):
    """Test analyze_student_attendance with low attendance rate"""
    mock_stats = {
        "total_lessons": 10,
        "present_count": 6,
        "absent_count": 4,
        "attendance_rate": 60.0
    }
    
    with patch.object(analysis_service.db_service, 'get_attendance_stats',
                     new=AsyncMock(return_value=mock_stats)):
        with patch.object(analysis_service.llm_service, 'generate_alert',
                         new=AsyncMock(return_value={"alert": "Low attendance warning"})):
            result = await analysis_service.analyze_student_attendance(1)
            
            assert result["status"] == "success"
            assert len(result["alerts"]) > 0


@pytest.mark.asyncio
async def test_analyze_homework_completion(analysis_service):
    """Test analyze_homework_completion"""
    mock_stats = {
        "total_assignments": 5,
        "completed_count": 4,
        "completion_rate": 80.0,
        "overdue_count": 1
    }
    
    with patch.object(analysis_service.db_service, 'get_homework_completion_rate',
                     new=AsyncMock(return_value=mock_stats)):
        with patch.object(analysis_service.llm_service, 'generate_alert',
                         new=AsyncMock(return_value={"alert": "Complete homework"})):
            result = await analysis_service.analyze_homework_completion(1)
            
            assert result["status"] == "success"
            assert result["homework_stats"]["completion_rate"] == 80.0


@pytest.mark.asyncio
async def test_analyze_homework_completion_many_overdue(analysis_service):
    """Test analyze_homework_completion with many overdue assignments"""
    mock_stats = {
        "total_assignments": 10,
        "completed_count": 5,
        "completion_rate": 50.0,
        "overdue_count": 5
    }
    
    with patch.object(analysis_service.db_service, 'get_homework_completion_rate',
                     new=AsyncMock(return_value=mock_stats)):
        with patch.object(analysis_service.llm_service, 'generate_alert',
                         new=AsyncMock(return_value={"alert": "Multiple overdue assignments"})):
            result = await analysis_service.analyze_homework_completion(1)
            
            assert result["status"] == "success"
            assert len(result["alerts"]) > 0


@pytest.mark.asyncio
async def test_generate_comprehensive_report(analysis_service):
    """Test generate_comprehensive_report"""
    # Mock all the sub-analyses
    mock_grades = {
        "student_id": 1,
        "status": "success",
        "average_grade": 4.5,
        "grade_trends": {"Math": {"average": 4.5, "trend": "stable"}},
        "total_grades": 10
    }
    
    mock_attendance = {
        "student_id": 1,
        "status": "success",
        "attendance_stats": {"attendance_rate": 95.0},
        "alerts": []
    }
    
    mock_homework = {
        "student_id": 1,
        "status": "success",
        "homework_stats": {"completion_rate": 85.0, "overdue_count": 1},
        "alerts": []
    }
    
    with patch.object(analysis_service, 'analyze_student_grades',
                     new=AsyncMock(return_value=mock_grades)):
        with patch.object(analysis_service, 'analyze_student_attendance',
                         new=AsyncMock(return_value=mock_attendance)):
            with patch.object(analysis_service, 'analyze_homework_completion',
                             new=AsyncMock(return_value=mock_homework)):
                with patch.object(analysis_service.llm_service, 'generate_insights',
                                 new=AsyncMock(return_value={"insights": "Good progress"})):
                    with patch.object(analysis_service.llm_service, 'generate_recommendations',
                                     new=AsyncMock(return_value={"recommendations": "Keep it up"})):
                        result = await analysis_service.generate_comprehensive_report(1)
                        
                        assert result["status"] == "success"
                        assert result["student_id"] == 1
                        assert "grades" in result
                        assert "attendance" in result
                        assert "homework" in result
                        assert "ai_insights" in result
                        assert "recommendations" in result


@pytest.mark.asyncio
async def test_identify_strengths(analysis_service):
    """Test _identify_strengths method"""
    grades_analysis = {
        "grade_trends": {
            "Math": {"average": 4.8, "trend": "stable"},
            "Physics": {"average": 4.2, "trend": "improving"},
            "Chemistry": {"average": 3.5, "trend": "stable"}
        }
    }
    
    strengths = analysis_service._identify_strengths(grades_analysis)
    
    assert "Math" in strengths
    assert any("Physics" in s for s in strengths)


@pytest.mark.asyncio
async def test_identify_improvements(analysis_service):
    """Test _identify_improvements method"""
    grades_analysis = {
        "grade_trends": {
            "Math": {"average": 2.5, "trend": "declining"},
            "Physics": {"average": 4.5, "trend": "stable"}
        }
    }
    
    attendance_analysis = {
        "attendance_stats": {"attendance_rate": 85.0}
    }
    
    homework_analysis = {
        "homework_stats": {"overdue_count": 3}
    }
    
    improvements = analysis_service._identify_improvements(
        grades_analysis, 
        attendance_analysis, 
        homework_analysis
    )
    
    assert len(improvements) > 0
    assert any("Math" in i for i in improvements)
    assert any("Attendance" in i for i in improvements)
    assert any("Homework" in i for i in improvements)
