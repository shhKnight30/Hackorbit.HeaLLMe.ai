from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId
from .user import PyObjectId

class VitalSigns(BaseModel):
    heart_rate: Optional[int] = Field(None, ge=0, le=300, description="Heart rate in BPM")
    blood_pressure_systolic: Optional[int] = Field(None, ge=0, le=300, description="Systolic blood pressure")
    blood_pressure_diastolic: Optional[int] = Field(None, ge=0, le=200, description="Diastolic blood pressure")
    temperature: Optional[float] = Field(None, ge=30, le=45, description="Body temperature in Celsius")
    oxygen_saturation: Optional[float] = Field(None, ge=0, le=100, description="Blood oxygen saturation percentage")
    respiratory_rate: Optional[int] = Field(None, ge=0, le=100, description="Respiratory rate per minute")

class HealthMetrics(BaseModel):
    weight: Optional[float] = Field(None, ge=0, le=500, description="Weight in kg")
    height: Optional[float] = Field(None, ge=0, le=300, description="Height in cm")
    bmi: Optional[float] = Field(None, ge=0, le=100, description="Body Mass Index")
    body_fat_percentage: Optional[float] = Field(None, ge=0, le=100, description="Body fat percentage")
    muscle_mass: Optional[float] = Field(None, ge=0, le=200, description="Muscle mass in kg")

class HealthData(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(..., description="ID of the user who owns this health data")
    date_recorded: datetime = Field(default_factory=datetime.utcnow, description="Date when data was recorded")
    vital_signs: Optional[VitalSigns] = Field(default_factory=VitalSigns, description="Vital signs measurements")
    health_metrics: Optional[HealthMetrics] = Field(default_factory=HealthMetrics, description="Health metrics")
    symptoms: Optional[List[str]] = Field(default_factory=list, description="List of reported symptoms")
    medications: Optional[List[str]] = Field(default_factory=list, description="List of current medications")
    notes: Optional[str] = Field(None, description="Additional notes about health status")
    mood: Optional[str] = Field(None, description="User's mood/emotional state")
    sleep_hours: Optional[float] = Field(None, ge=0, le=24, description="Hours of sleep")
    exercise_minutes: Optional[int] = Field(None, ge=0, le=1440, description="Minutes of exercise")
    water_intake_ml: Optional[int] = Field(None, ge=0, le=10000, description="Water intake in ml")
    calories_consumed: Optional[int] = Field(None, ge=0, le=10000, description="Calories consumed")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "date_recorded": "2024-01-01T10:00:00Z",
                "vital_signs": {
                    "heart_rate": 72,
                    "blood_pressure_systolic": 120,
                    "blood_pressure_diastolic": 80,
                    "temperature": 36.8,
                    "oxygen_saturation": 98.5,
                    "respiratory_rate": 16
                },
                "health_metrics": {
                    "weight": 70.5,
                    "height": 175.0,
                    "bmi": 23.0,
                    "body_fat_percentage": 15.0,
                    "muscle_mass": 55.0
                },
                "symptoms": ["fatigue", "headache"],
                "medications": ["vitamin D", "omega-3"],
                "notes": "Feeling better today",
                "mood": "good",
                "sleep_hours": 7.5,
                "exercise_minutes": 30,
                "water_intake_ml": 2000,
                "calories_consumed": 1800
            }
        }

class HealthDataCreate(BaseModel):
    vital_signs: Optional[VitalSigns] = None
    health_metrics: Optional[HealthMetrics] = None
    symptoms: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    notes: Optional[str] = None
    mood: Optional[str] = None
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    water_intake_ml: Optional[int] = None
    calories_consumed: Optional[int] = None

class HealthDataUpdate(BaseModel):
    vital_signs: Optional[VitalSigns] = None
    health_metrics: Optional[HealthMetrics] = None
    symptoms: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    notes: Optional[str] = None
    mood: Optional[str] = None
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    water_intake_ml: Optional[int] = None
    calories_consumed: Optional[int] = None

class HealthAnalysis(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    analysis_type: str  # nutrition, symptoms, general_health
    recommendations: List[str]
    vitamins_minerals: Dict[str, str]  # vitamin/mineral -> status (low/normal/high)
    dietary_suggestions: List[str]
    risk_factors: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class HealthQuote(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    quote: str
    author: Optional[str] = None
    category: str = "general"
    is_active: bool = True
