from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
import psycopg2
from typing import List, Optional

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='your_pass',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

app = FastAPI()

# Function to get all logs with pagination and time filtering
@app.get("/logs")
def get_all_logs(
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Page size"),
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time")
):
    # Calculate the offset for pagination
    offset = (page - 1) * page_size
    
    # Build the base query
    query = "SELECT * FROM logs WHERE TRUE"
    
    # Time filtering
    params = []
    if start_time:
        query += " AND timestamp >= %s"
        params.append(start_time)
    if end_time:
        query += " AND timestamp <= %s"
        params.append(end_time)
    
    # Add pagination
    query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
    params.extend([page_size, offset])
    
    # Execute the query
    cursor.execute(query, tuple(params))
    logs = cursor.fetchall()
    
    if not logs:
        raise HTTPException(status_code=404, detail="Logs for user was not found")
    
    return logs

# Function to get logs for a specific user with pagination and time filtering
@app.get("/logs/{user_id}")
def get_logs_by_user(
    user_id: int,
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Page size"),
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time")
):
    # Calculate the offset for pagination
    offset = (page - 1) * page_size
    
    # Build the base query
    query = "SELECT * FROM logs WHERE user_id = %s"
    
    # Time filtering
    params = [user_id]
    if start_time:
        query += " AND timestamp >= %s"
        params.append(start_time)
    if end_time:
        query += " AND timestamp <= %s"
        params.append(end_time)
    
    # Add pagination
    query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
    params.extend([page_size, offset])
    
    # Execute the query
    cursor.execute(query, tuple(params))
    logs = cursor.fetchall()
    
    if not logs:
        raise HTTPException(status_code=404, detail="Logs for user was not found")
    
    return logs
