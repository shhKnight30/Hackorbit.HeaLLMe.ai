import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    database: motor.motor_asyncio.AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    db.client = motor.motor_asyncio.AsyncIOMotorClient(
        os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    )
    db.database = db.client[os.getenv("DATABASE_NAME", "healme_db")]
    print("Connected to MongoDB")

async def close_mongo_connection():
    """Close database connection"""
    db.client.close()
    print("Disconnected from MongoDB")

async def get_database():
    """Get database instance"""
    return db.database

USERS_COLLECTION = "users"
CHAT_SESSIONS_COLLECTION = "chat_sessions"
CHAT_MESSAGES_COLLECTION = "chat_messages"
HEALTH_DATA_COLLECTION = "health_data"
HEALTH_ANALYSIS_COLLECTION = "health_analysis"
HEALTH_QUOTES_COLLECTION = "health_quotes"


def get_users_collection():
    """Get users collection"""
    return db.database[USERS_COLLECTION] if db.database else None

def get_chat_sessions_collection():
    """Get chat sessions collection"""
    return db.database[CHAT_SESSIONS_COLLECTION] if db.database else None

def get_chat_messages_collection():
    """Get chat messages collection"""
    return db.database[CHAT_MESSAGES_COLLECTION] if db.database else None

def get_health_data_collection():
    """Get health data collection"""
    return db.database[HEALTH_DATA_COLLECTION] if db.database else None

def get_health_analysis_collection():
    """Get health analysis collection"""
    return db.database[HEALTH_ANALYSIS_COLLECTION] if db.database else None

def get_health_quotes_collection():
    """Get health quotes collection"""
    return db.database[HEALTH_QUOTES_COLLECTION] if db.database else None


async def create_indexes():
    """Create database indexes for better performance"""
    try:

        users_collection = get_users_collection()
        if users_collection:
            await users_collection.create_index("email", unique=True)
            await users_collection.create_index("username", unique=True)
            await users_collection.create_index("created_at")
        

        chat_sessions_collection = get_chat_sessions_collection()
        if chat_sessions_collection:
            await chat_sessions_collection.create_index("user_id")
            await chat_sessions_collection.create_index("created_at")
            await chat_sessions_collection.create_index("last_activity")
            await chat_sessions_collection.create_index([("user_id", 1), ("last_activity", -1)])
        

        chat_messages_collection = get_chat_messages_collection()
        if chat_messages_collection:
            await chat_messages_collection.create_index("user_id")
            await chat_messages_collection.create_index("session_id")
            await chat_messages_collection.create_index("timestamp")
            await chat_messages_collection.create_index([("session_id", 1), ("timestamp", -1)])
        

        health_data_collection = get_health_data_collection()
        if health_data_collection:
            await health_data_collection.create_index("user_id")
            await health_data_collection.create_index("date_recorded")
            await health_data_collection.create_index([("user_id", 1), ("date_recorded", -1)])
        

        health_analysis_collection = get_health_analysis_collection()
        if health_analysis_collection:
            await health_analysis_collection.create_index("user_id")
            await health_analysis_collection.create_index("analysis_type")
            await health_analysis_collection.create_index("created_at")
            await health_analysis_collection.create_index([("user_id", 1), ("analysis_type", 1)])
        
        health_quotes_collection = get_health_quotes_collection()
        if health_quotes_collection:
            await health_quotes_collection.create_index("category")
            await health_quotes_collection.create_index("is_active")
            await health_quotes_collection.create_index([("category", 1), ("is_active", 1)])
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"❌ Failed to create indexes: {e}")
        raise e
