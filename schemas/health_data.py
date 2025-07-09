from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class VitalSignsBase(BaseModel):
    heart_rate: Optional[int] = Field(None, ge=0, le=300, description="Heart rate in BPM")
    blood_pressure_systolic: Optional[int] = Field(None, ge=0, le=300, description="Systolic blood pressure")
    blood_pressure_diastolic: Optional[int] = Field(None, ge=0, le=200, description="Diastolic blood pressure")
    temperature: Optional[float] = Field(None, ge=30, le=45, description="Body temperature in Celsius")
    oxygen_saturation: Optional[float] = Field(None, ge=0, le=100, description="Blood oxygen saturation percentage")
    respiratory_rate: Optional[int] = Field(None, ge=0, le=100, description="Respiratory rate per minute")

class HealthMetricsBase(BaseModel):
    weight: Optional[float] = Field(None, ge=0, le=500, description="Weight in kg")
    height: Optional[float] = Field(None, ge=0, le=300, description="Height in cm")
    bmi: Optional[float] = Field(None, ge=0, le=100, description="Body Mass Index")
    body_fat_percentage: Optional[float] = Field(None, ge=0, le=100, description="Body fat percentage")
    muscle_mass: Optional[float] = Field(None, ge=0, le=200, description="Muscle mass in kg")

class HealthDataBase(BaseModel):
    vital_signs: Optional[VitalSignsBase] = None
    health_metrics: Optional[HealthMetricsBase] = None
    symptoms: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    notes: Optional[str] = Field(None, max_length=1000)
    mood: Optional[str] = Field(None, regex="^(excellent|good|neutral|poor|terrible)$")
    sleep_hours: Optional[float] = Field(None, ge=0, le=24, description="Hours of sleep")
    exercise_minutes: Optional[int] = Field(None, ge=0, le=1440, description="Minutes of exercise")
    water_intake_ml: Optional[int] = Field(None, ge=0, le=10000, description="Water intake in ml")
    calories_consumed: Optional[int] = Field(None, ge=0, le=10000, description="Calories consumed")

class HealthDataCreate(HealthDataBase):
    pass

class HealthDataUpdate(BaseModel):
    vital_signs: Optional[VitalSignsBase] = None
    health_metrics: Optional[HealthMetricsBase] = None
    symptoms: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    notes: Optional[str] = Field(None, max_length=1000)
    mood: Optional[str] = Field(None, regex="^(excellent|good|neutral|poor|terrible)$")
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    exercise_minutes: Optional[int] = Field(None, ge=0, le=1440)
    water_intake_ml: Optional[int] = Field(None, ge=0, le=10000)
    calories_consumed: Optional[int] = Field(None, ge=0, le=10000)

class HealthDataResponse(HealthDataBase):
    id: str
    user_id: str
    date_recorded: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
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
                "calories_consumed": 1800,
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        }

class HealthDataListResponse(BaseModel):
    id: str
    date_recorded: datetime
    vital_signs: Optional[VitalSignsBase] = None
    health_metrics: Optional[HealthMetricsBase] = None
    symptoms: List[str] = []
    mood: Optional[str] = None
    notes: Optional[str] = None

class HealthTrendsResponse(BaseModel):
    period: str
    vital_signs_trends: Dict[str, List[float]] = {}
    health_metrics_trends: Dict[str, List[float]] = {}
    mood_trends: Dict[str, int] = {}
    sleep_trends: List[float] = []
    exercise_trends: List[int] = []
    water_intake_trends: List[int] = []
    calories_trends: List[int] = []

class HealthInsightsResponse(BaseModel):
    overall_health_score: float
    recommendations: List[str] = []
    risk_factors: List[str] = []
    positive_trends: List[str] = []
    areas_for_improvement: List[str] = []
    next_checkup_date: Optional[datetime] = None

# New schemas for HealthAnalysis and HealthQuote
class HealthAnalysisBase(BaseModel):
    analysis_type: str = Field(..., regex="^(nutrition|symptoms|general_health)$")
    recommendations: List[str] = []
    vitamins_minerals: Dict[str, str] = Field(default_factory=dict)  # vitamin/mineral -> status
    dietary_suggestions: List[str] = []
    risk_factors: List[str] = []

class HealthAnalysisCreate(HealthAnalysisBase):
    pass

class HealthAnalysisUpdate(BaseModel):
    analysis_type: Optional[str] = Field(None, regex="^(nutrition|symptoms|general_health)$")
    recommendations: Optional[List[str]] = None
    vitamins_minerals: Optional[Dict[str, str]] = None
    dietary_suggestions: Optional[List[str]] = None
    risk_factors: Optional[List[str]] = None

class HealthAnalysisResponse(HealthAnalysisBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "analysis_type": "nutrition",
                "recommendations": [
                    "Increase vitamin D intake",
                    "Add more leafy greens to your diet"
                ],
                "vitamins_minerals": {
                    "vitamin_d": "low",
                    "iron": "normal",
                    "calcium": "low"
                },
                "dietary_suggestions": [
                    "Eat more salmon and eggs",
                    "Include spinach in your meals"
                ],
                "risk_factors": [
                    "Low vitamin D levels",
                    "Insufficient calcium intake"
                ],
                "created_at": "2024-01-01T10:00:00Z"
            }
        }

class HealthQuoteBase(BaseModel):
    quote: str = Field(..., min_length=1, max_length=500)
    author: Optional[str] = None
    category: str = Field("general", regex="^(general|motivation|wellness|fitness|mental_health)$")
    is_active: bool = True

class HealthQuoteCreate(HealthQuoteBase):
    pass

class HealthQuoteUpdate(BaseModel):
    quote: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = None
    category: Optional[str] = Field(None, regex="^(general|motivation|wellness|fitness|mental_health)$")
    is_active: Optional[bool] = None

class HealthQuoteResponse(HealthQuoteBase):
    id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "quote": "Health is not just about what you're eating. It's about what you're thinking and saying, too.",
                "author": "Anonymous",
                "category": "wellness",
                "is_active": True
            }
        }
