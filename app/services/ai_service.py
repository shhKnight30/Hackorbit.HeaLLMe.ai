import google.generativeai as genai
import json
import random
import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from notifications import notify_n8n

load_dotenv()

class HealthAIService:
    def __init__(self):
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Enhanced health quotes
        self.health_quotes = [
            "An apple a day keeps the doctor away",
            "Health is wealth",
            "Take care of your body. It's the only place you have to live",
            "The groundwork for all happiness is good health",
            "Your body is a temple. Keep it pure and clean for the soul to reside in",
            "Prevention is better than cure",
            "A healthy outside starts from the inside",
            "The greatest wealth is health",
            "Wellness is the complete integration of body, mind, and spirit",
            "Health is not simply the absence of sickness"
        ]
        
        # Health analysis templates
        self.symptom_analysis_template = """
        You are HealLLMe.ai, a medical AI assistant. Analyze the following symptoms and provide comprehensive guidance.
        
        PATIENT INFORMATION:
        Symptoms: {symptoms}
        Medical History: {medical_history}
        Age: {age}
        Gender: {gender}
        
        Please provide a detailed analysis in the following JSON format:
        {{
            "possible_conditions": ["condition1", "condition2"],
            "recommendations": ["immediate action 1", "immediate action 2"],
            "urgency_level": "low/medium/high",
            "suggested_tests": ["test1", "test2"],
            "lifestyle_advice": ["advice1", "advice2"],
            "warning_signs": ["sign1", "sign2"],
            "when_to_seek_help": "specific guidance",
            "confidence_level": "percentage"
        }}
        
        IMPORTANT: This is for guidance only, not medical diagnosis. Always recommend consulting healthcare professionals for serious symptoms.
        """
        
        self.health_recommendations_template = """
        Generate personalized health recommendations for a user with the following profile:
        
        USER PROFILE:
        Age: {age}
        Gender: {gender}
        Medical History: {medical_history}
        Current Health Data: {health_data}
        Lifestyle: {lifestyle}
        
        Provide comprehensive recommendations in JSON format:
        {{
            "dietary_suggestions": ["food1", "food2"],
            "vitamins_minerals": {{
                "vitamin_d": "status (low/normal/high)",
                "iron": "status",
                "calcium": "status",
                "vitamin_b12": "status"
            }},
            "exercise_recommendations": ["exercise1", "exercise2"],
            "general_health_tips": ["tip1", "tip2"],
            "foods_to_avoid": ["food1", "food2"],
            "sleep_recommendations": ["recommendation1"],
            "stress_management": ["technique1", "technique2"],
            "preventive_measures": ["measure1", "measure2"]
        }}
        """
        
        self.chat_template = """
        You are HealLLMe.ai, a friendly and empathetic medical AI assistant. You provide health guidance, support, and education.
        
        CONVERSATION CONTEXT:
        Previous messages: {chat_history}
        
        CURRENT MESSAGE: {message}
        
        RESPONSE GUIDELINES:
        1. Be empathetic and supportive
        2. Provide evidence-based health information
        3. Always recommend consulting healthcare professionals for serious concerns
        4. Use simple, understandable language
        5. Include practical tips and actionable advice
        6. Maintain a warm, caring tone
        
        Respond naturally and helpfully to the user's health-related question or concern.
        """
    
    async def analyze_symptoms(self, symptoms: str, user_history: List[str], user_data: Dict = None) -> Dict:
        """AI-powered symptom analysis using Gemini"""
        try:
            # Prepare user data
            age = user_data.get('age', 'Not specified') if user_data else 'Not specified'
            gender = user_data.get('gender', 'Not specified') if user_data else 'Not specified'
            medical_history = ', '.join(user_history) if user_history else 'None'
            
            # Create prompt
            prompt = self.symptom_analysis_template.format(
                symptoms=symptoms,
                medical_history=medical_history,
                age=age,
                gender=gender
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "possible_conditions": ["Consult a healthcare professional"],
                    "recommendations": ["Please consult a healthcare professional for proper diagnosis"],
                    "urgency_level": "medium",
                    "suggested_tests": ["General health checkup"],
                    "lifestyle_advice": ["Maintain a healthy lifestyle"],
                    "warning_signs": ["Persistent symptoms"],
                    "when_to_seek_help": "If symptoms persist or worsen",
                    "confidence_level": "60%"
                }
            
            # Send notification to n8n
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"Symptom analysis completed for: {symptoms}",
                event_type="symptom_analysis",
                metadata={
                    "symptoms": symptoms,
                    "urgency_level": result.get("urgency_level", "medium"),
                    "possible_conditions": result.get("possible_conditions", []),
                    "confidence_level": result.get("confidence_level", "unknown")
                }
            )
            
            return result
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "recommendations": ["Please consult a healthcare professional"],
                "urgency_level": "medium",
                "possible_conditions": ["Unable to analyze at this time"],
                "suggested_tests": ["General health checkup"],
                "lifestyle_advice": ["Maintain a healthy lifestyle"],
                "warning_signs": ["Persistent symptoms"],
                "when_to_seek_help": "If symptoms persist or worsen",
                "confidence_level": "0%"
            }
            
            # Notify n8n about the error
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"Symptom analysis failed: {str(e)}",
                event_type="symptom_analysis_error",
                metadata={"error": str(e), "symptoms": symptoms}
            )
            
            return error_result
    
    async def generate_health_recommendations(self, user_data: Dict) -> Dict:
        """Generate personalized health recommendations using Gemini"""
        try:
            # Prepare health data
            health_data = user_data.get('health_data', {})
            lifestyle = user_data.get('lifestyle', {})
            
            # Create prompt
            prompt = self.health_recommendations_template.format(
                age=user_data.get('age', 'Not specified'),
                gender=user_data.get('gender', 'Not specified'),
                medical_history=', '.join(user_data.get('medical_history', [])) if user_data.get('medical_history') else 'None',
                health_data=json.dumps(health_data),
                lifestyle=json.dumps(lifestyle)
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                # Fallback recommendations
                result = {
                    "dietary_suggestions": ["Eat a balanced diet with fruits and vegetables"],
                    "vitamins_minerals": {
                        "vitamin_d": "Consider supplementation",
                        "iron": "Include iron-rich foods",
                        "calcium": "Include dairy or fortified foods",
                        "vitamin_b12": "Include animal products or supplements"
                    },
                    "exercise_recommendations": ["30 minutes of moderate exercise daily"],
                    "general_health_tips": ["Stay hydrated", "Get adequate sleep"],
                    "foods_to_avoid": ["Excessive processed foods"],
                    "sleep_recommendations": ["7-9 hours of sleep per night"],
                    "stress_management": ["Practice meditation or deep breathing"],
                    "preventive_measures": ["Regular health checkups"]
                }
            
            # Send notification to n8n
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"Health recommendations generated for user",
                event_type="health_recommendations",
                metadata={
                    "recommendations_count": len(result.get("dietary_suggestions", [])),
                    "vitamins_analyzed": list(result.get("vitamins_minerals", {}).keys()),
                    "exercise_count": len(result.get("exercise_recommendations", []))
                }
            )
            
            return result
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "dietary_suggestions": ["Eat a balanced diet with fruits and vegetables"],
                "vitamins_minerals": {"vitamin_d": "Consider supplementation", "iron": "Include iron-rich foods"},
                "exercise_recommendations": ["30 minutes of moderate exercise daily"],
                "general_health_tips": ["Stay hydrated", "Get adequate sleep"],
                "foods_to_avoid": ["Excessive processed foods"],
                "sleep_recommendations": ["7-9 hours of sleep per night"],
                "stress_management": ["Practice meditation or deep breathing"],
                "preventive_measures": ["Regular health checkups"]
            }
            
            # Notify n8n about the error
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"Health recommendations generation failed: {str(e)}",
                event_type="health_recommendations_error",
                metadata={"error": str(e)}
            )
            
            return error_result
    
    def get_daily_health_quote(self) -> str:
        """Return a random health quote"""
        return random.choice(self.health_quotes)
    
    async def chat_with_ai(self, message: str, chat_history: List[Dict], user_data: Dict = None) -> str:
        """General health chat with Gemini AI"""
        try:
            # Prepare chat history
            history_text = ""
            if chat_history:
                history_text = "\n".join([
                    f"User: {msg.get('message', '')}\nAI: {msg.get('response', '')}"
                    for msg in chat_history[-5:]  # Last 5 messages for context
                ])
            
            # Create prompt
            prompt = self.chat_template.format(
                chat_history=history_text,
                message=message
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            ai_response = response.text
            
            # Send notification to n8n
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"AI chat interaction: {message[:100]}...",
                event_type="ai_chat",
                metadata={
                    "user_message": message,
                    "ai_response": ai_response[:200],
                    "chat_history_length": len(chat_history)
                }
            )
            
            return ai_response
            
        except Exception as e:
            error_message = f"I'm sorry, I'm having trouble responding right now. Please try again later. Error: {str(e)}"
            
            # Notify n8n about the error
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"AI chat failed: {str(e)}",
                event_type="ai_chat_error",
                metadata={"error": str(e), "user_message": message}
            )
            
            return error_message
    
    async def analyze_health_data(self, health_data: Dict, user_data: Dict) -> Dict:
        """Analyze health data and provide insights"""
        try:
            prompt = f"""
            Analyze the following health data and provide insights:
            
            USER DATA:
            Age: {user_data.get('age', 'Not specified')}
            Gender: {user_data.get('gender', 'Not specified')}
            Medical History: {', '.join(user_data.get('medical_history', [])) if user_data.get('medical_history') else 'None'}
            
            HEALTH DATA:
            {json.dumps(health_data, indent=2)}
            
            Provide analysis in JSON format:
            {{
                "overall_health_score": "percentage",
                "trends": ["trend1", "trend2"],
                "concerns": ["concern1", "concern2"],
                "improvements": ["improvement1", "improvement2"],
                "recommendations": ["recommendation1", "recommendation2"],
                "risk_factors": ["risk1", "risk2"],
                "positive_aspects": ["positive1", "positive2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                result = {
                    "overall_health_score": "70%",
                    "trends": ["General health appears stable"],
                    "concerns": ["Continue monitoring"],
                    "improvements": ["Maintain current healthy habits"],
                    "recommendations": ["Regular health checkups"],
                    "risk_factors": ["None identified"],
                    "positive_aspects": ["Good overall health indicators"]
                }
            
            # Send notification to n8n
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"Health data analysis completed",
                event_type="health_data_analysis",
                metadata={
                    "health_score": result.get("overall_health_score", "unknown"),
                    "concerns_count": len(result.get("concerns", [])),
                    "recommendations_count": len(result.get("recommendations", []))
                }
            )
            
            return result
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "overall_health_score": "Unable to analyze",
                "trends": ["Analysis unavailable"],
                "concerns": ["Please consult healthcare professional"],
                "improvements": ["Maintain healthy lifestyle"],
                "recommendations": ["Regular health checkups"],
                "risk_factors": ["Unable to assess"],
                "positive_aspects": ["Continue healthy habits"]
            }
            
            # Notify n8n about the error
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"Health data analysis failed: {str(e)}",
                event_type="health_data_analysis_error",
                metadata={"error": str(e)}
            )
            
            return error_result
    
    async def generate_emergency_response(self, emergency_type: str, user_data: Dict) -> Dict:
        """Generate emergency response guidance"""
        try:
            prompt = f"""
            Emergency situation: {emergency_type}
            
            User Information:
            Age: {user_data.get('age', 'Not specified')}
            Medical History: {', '.join(user_data.get('medical_history', [])) if user_data.get('medical_history') else 'None'}
            
            Provide emergency guidance in JSON format:
            {{
                "immediate_actions": ["action1", "action2"],
                "emergency_contacts": ["contact1", "contact2"],
                "warning_signs": ["sign1", "sign2"],
                "do_not_do": ["action1", "action2"],
                "when_to_call_emergency": "specific guidance",
                "preparation_steps": ["step1", "step2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                result = {
                    "immediate_actions": ["Call emergency services if needed"],
                    "emergency_contacts": ["911", "Local emergency services"],
                    "warning_signs": ["Severe symptoms"],
                    "do_not_do": ["Don't delay seeking help"],
                    "when_to_call_emergency": "If symptoms are severe or life-threatening",
                    "preparation_steps": ["Stay calm", "Call for help"]
                }
            
            # Send emergency notification to n8n
            await notify_n8n(
                user_id=user_data.get('user_id', 'unknown'),
                message=f"EMERGENCY: {emergency_type}",
                event_type="emergency_alert",
                metadata={
                    "emergency_type": emergency_type,
                    "user_age": user_data.get('age'),
                    "medical_history": user_data.get('medical_history', [])
                }
            )
            
            return result
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "immediate_actions": ["Call emergency services immediately"],
                "emergency_contacts": ["911"],
                "warning_signs": ["Any severe symptoms"],
                "do_not_do": ["Don't delay seeking help"],
                "when_to_call_emergency": "Immediately for severe symptoms",
                "preparation_steps": ["Call emergency services"]
            }
            
            return error_result
