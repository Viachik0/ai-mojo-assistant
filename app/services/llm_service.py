import aiohttp
import logging
from typing import Dict, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.vllm_api_base = settings.VLLM_API_BASE
        self.llm_model_name = settings.LLM_MODEL_NAME
    
    async def _call_vllm(self, prompt: str, system_message: str = None) -> str:
        """Call vLLM API (OpenAI-compatible) for generating insights"""
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.vllm_api_base}/chat/completions",
                    json={
                        "model": self.llm_model_name,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        logger.error(f"Error calling vLLM API: {response.status} - {error_text}")
                        return "AI analysis unavailable. Please check vLLM server."
        except Exception as e:
            logger.error(f"Error calling vLLM API: {e}")
            return f"Error generating AI insights: {str(e)}"
    
    async def analyze_performance(self, grades: List[Dict], student_name: str = "Student") -> Dict:
        """Use AI to analyze student performance from grades"""
        if not grades:
            return {"message": "No grades available for analysis."}
        
        # Prepare grade summary
        grade_summary = "\n".join([
            f"- {g.get('subject', 'Unknown')}: {g.get('value', 'N/A')} on {g.get('date', 'Unknown date')}"
            for g in grades[:10]  # Limit to recent 10 grades
        ])
        
        prompt = f"""Analyze the following student grades and provide a brief, encouraging summary report for parents (2-3 sentences):

{grade_summary}

Focus on:
1. Overall performance trends
2. Strengths in specific subjects
3. Areas that might need attention
Keep the tone positive and constructive."""
        
        system_message = "You are an educational AI assistant helping teachers communicate student progress to parents. Be encouraging, specific, and constructive."
        
        summary = await self._call_vllm(prompt, system_message)
        
        return {"message": summary}
    
    async def generate_insights(self, analytics_data: Dict) -> Dict:
        """Generate AI-powered insights from analytics data"""
        grade_trends = analytics_data.get("grade_trends", {})
        attendance = analytics_data.get("attendance", {})
        homework = analytics_data.get("homework", {})
        
        prompt = f"""Analyze this student's educational data and provide actionable insights (3-4 bullet points):

Grade Trends:
{self._format_grade_trends(grade_trends)}

Attendance:
- Attendance Rate: {attendance.get('attendance_rate', 0)}%
- Present: {attendance.get('present_count', 0)}/{attendance.get('total_lessons', 0)} lessons

Homework:
- Total Assignments: {homework.get('total_assignments', 0)}
- Overdue: {homework.get('overdue_count', 0)}

Provide specific, actionable insights for improvement."""
        
        system_message = "You are an educational data analyst providing insights to teachers. Be specific and actionable."
        
        insights = await self._call_vllm(prompt, system_message)
        
        return {"insights": insights}
    
    async def generate_alert(self, alert_type: str, data: Dict) -> Dict:
        """Generate AI-powered alerts for concerning patterns"""
        if alert_type == "low_attendance":
            attendance_rate = data.get("attendance_rate", 0)
            prompt = f"""A student has an attendance rate of {attendance_rate}%. Generate a brief, professional alert message for the teacher (2 sentences) suggesting action."""
        
        elif alert_type == "declining_grades":
            subject = data.get("subject", "a subject")
            trend = data.get("trend", "declining")
            prompt = f"""A student's grades in {subject} are {trend}. Generate a brief alert for the teacher (2 sentences) with suggestions."""
        
        elif alert_type == "missing_homework":
            overdue_count = data.get("overdue_count", 0)
            prompt = f"""A student has {overdue_count} overdue homework assignments. Generate a brief alert (2 sentences) for action."""
        
        else:
            return {"alert": "Alert type not recognized"}
        
        system_message = "You are an educational alert system. Be concise, professional, and action-oriented."
        
        alert = await self._call_vllm(prompt, system_message)
        
        return {"alert": alert}
    
    async def generate_recommendations(self, student_data: Dict) -> Dict:
        """Generate personalized recommendations for teachers and parents"""
        prompt = f"""Based on this student profile, generate 3 specific recommendations for improvement:

Student Performance Summary:
- Average Grade: {student_data.get('average_grade', 'N/A')}
- Attendance Rate: {student_data.get('attendance_rate', 'N/A')}%
- Homework Completion: {student_data.get('homework_completion', 'N/A')}%
- Strengths: {', '.join(student_data.get('strengths', ['Unknown']))}
- Areas for Improvement: {', '.join(student_data.get('areas_for_improvement', ['Unknown']))}

Provide actionable recommendations for both teachers and parents."""
        
        system_message = "You are an educational consultant providing personalized recommendations. Be specific and practical."
        
        recommendations = await self._call_vllm(prompt, system_message)
        
        return {"recommendations": recommendations}
    
    def _format_grade_trends(self, grade_trends: Dict) -> str:
        """Format grade trends for AI prompt"""
        if not grade_trends:
            return "No grade data available"
        
        formatted = []
        for subject, trend_data in grade_trends.items():
            avg = trend_data.get('average', 0)
            trend = trend_data.get('trend', 'stable')
            formatted.append(f"- {subject}: Average {avg}, Trend: {trend}")
        
        return "\n".join(formatted) if formatted else "No grade data available"
