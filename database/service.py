from database.models import get_db_connection
import json
from datetime import datetime
import pandas as pd

def add_analysis_record(analysis_type, result_score, details_dict=None):
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details_json = json.dumps(details_dict) if details_dict else "{}"
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO analyses (date, type, result_score, details)
            VALUES (?, ?, ?, ?)
        ''', (date_str, analysis_type, result_score, details_json))
        conn.commit()

def get_recent_analyses(limit=10):
    with get_db_connection() as conn:
        query = "SELECT date as Date, type as Type, result_score as 'Result / Score' FROM analyses ORDER BY id DESC LIMIT ?"
        df = pd.read_sql_query(query, conn, params=(limit,))
    return df

def save_setting(key, value):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, value))
        conn.commit()

def get_setting(key, default=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row['value'] if row else default

def clear_history():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM analyses')
        conn.commit()
