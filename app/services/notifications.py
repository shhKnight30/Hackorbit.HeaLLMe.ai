import httpx
import os
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# n8n webhook configuration
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
N8N_TIMEOUT = int(os.getenv("N8N_TIMEOUT", "30"))

async def notify_n8n(user_id: str, message: str, event_type: str = "general", metadata: Optional[Dict[str, Any]] = None):
    """
    Send notification to n8n webhook for workflow automation
    
    Args:
        user_id: The user ID
        message: The message to send
        event_type: Type of event (general, health_alert, chat_message, etc.)
        metadata: Additional data to include in the payload
    """
    if not N8N_WEBHOOK_URL:
        print("⚠️ N8N_WEBHOOK_URL not configured")
        return
    
    payload = {
        "user_id": user_id,
        "message": message,
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": metadata or {}
    }

    try:
        async with httpx.AsyncClient(timeout=N8N_TIMEOUT) as client:
            response = await client.post(N8N_WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                print(f"✅ Sent to n8n: {response.status_code} - {event_type}")
            else:
                print(f"⚠️ n8n webhook returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send to n8n: {e}")

async def notify_health_alert(user_id: str, alert_type: str, severity: str, details: str):
    """Send health alert to n8n workflow"""
    metadata = {
        "alert_type": alert_type,
        "severity": severity,
        "details": details
    }
    
    message = f"Health Alert: {alert_type} - {severity} - {details}"
    await notify_n8n(user_id, message, "health_alert", metadata)

async def notify_chat_message(user_id: str, session_id: str, message: str, response: str):
    """Send chat message notification to n8n workflow"""
    metadata = {
        "session_id": session_id,
        "user_message": message,
        "ai_response": response
    }
    
    await notify_n8n(user_id, f"Chat message in session {session_id}", "chat_message", metadata)

async def notify_health_data_update(user_id: str, data_type: str, value: Any):
    """Send health data update to n8n workflow"""
    metadata = {
        "data_type": data_type,
        "value": value,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    message = f"Health data updated: {data_type} = {value}"
    await notify_n8n(user_id, message, "health_data_update", metadata)

async def notify_user_registration(user_id: str, email: str, username: str):
    """Send user registration notification to n8n workflow"""
    metadata = {
        "email": email,
        "username": username,
        "registration_date": datetime.utcnow().isoformat()
    }
    
    message = f"New user registered: {username} ({email})"
    await notify_n8n(user_id, message, "user_registration", metadata)

async def notify_health_analysis(user_id: str, analysis_type: str, recommendations: list):
    """Send health analysis notification to n8n workflow"""
    metadata = {
        "analysis_type": analysis_type,
        "recommendations": recommendations,
        "analysis_date": datetime.utcnow().isoformat()
    }
    
    message = f"Health analysis completed: {analysis_type} with {len(recommendations)} recommendations"
    await notify_n8n(user_id, message, "health_analysis", metadata)

async def notify_emergency_alert(user_id: str, emergency_type: str, location: Optional[str] = None):
    """Send emergency alert to n8n workflow"""
    metadata = {
        "emergency_type": emergency_type,
        "location": location,
        "alert_time": datetime.utcnow().isoformat()
    }
    
    message = f"EMERGENCY ALERT: {emergency_type}"
    if location:
        message += f" at {location}"
    
    await notify_n8n(user_id, message, "emergency_alert", metadata)

async def notify_medication_reminder(user_id: str, medication: str, dosage: str, time: str):
    """Send medication reminder to n8n workflow"""
    metadata = {
        "medication": medication,
        "dosage": dosage,
        "reminder_time": time,
        "reminder_date": datetime.utcnow().isoformat()
    }
    
    message = f"Medication reminder: {medication} - {dosage} at {time}"
    await notify_n8n(user_id, message, "medication_reminder", metadata)

async def notify_appointment_reminder(user_id: str, appointment_type: str, date: str, time: str):
    """Send appointment reminder to n8n workflow"""
    metadata = {
        "appointment_type": appointment_type,
        "appointment_date": date,
        "appointment_time": time,
        "reminder_date": datetime.utcnow().isoformat()
    }
    
    message = f"Appointment reminder: {appointment_type} on {date} at {time}"
    await notify_n8n(user_id, message, "appointment_reminder", metadata)

async def notify_batch_events(events: list):
    """Send multiple events to n8n in batch"""
    if not N8N_WEBHOOK_URL:
        print("⚠️ N8N_WEBHOOK_URL not configured")
        return
    
    batch_payload = {
        "events": events,
        "batch_timestamp": datetime.utcnow().isoformat(),
        "total_events": len(events)
    }
    
    try:
        async with httpx.AsyncClient(timeout=N8N_TIMEOUT) as client:
            response = await client.post(N8N_WEBHOOK_URL, json=batch_payload)
            if response.status_code == 200:
                print(f"✅ Sent batch to n8n: {response.status_code} - {len(events)} events")
            else:
                print(f"⚠️ n8n batch webhook returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send batch to n8n: {e}")

async def notify_vital_signs_alert(user_id: str, vital_sign: str, value: Any, threshold: Any, status: str):
    """Send vital signs alert to n8n workflow"""
    metadata = {
        "vital_sign": vital_sign,
        "current_value": value,
        "threshold": threshold,
        "status": status,  # normal, warning, critical
        "alert_time": datetime.utcnow().isoformat()
    }
    
    message = f"Vital signs alert: {vital_sign} = {value} ({status})"
    await notify_n8n(user_id, message, "vital_signs_alert", metadata)

async def notify_symptom_tracking(user_id: str, symptoms: list, severity: str):
    """Send symptom tracking notification to n8n workflow"""
    metadata = {
        "symptoms": symptoms,
        "severity": severity,
        "tracking_date": datetime.utcnow().isoformat()
    }
    
    message = f"Symptom tracking: {', '.join(symptoms)} - {severity} severity"
    await notify_n8n(user_id, message, "symptom_tracking", metadata) 