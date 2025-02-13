import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST_PROD"),
    "port": os.getenv("DB_PORT"),
}

# Allowed status options
STATUS_OPTIONS = ["NotStart", "InProgress", "Success", "Fail"]

# Static mock data from CSV:
# StoreName,StatusStep1,StatusStep2,StatusStep3,StatusStep4,StatusStep5,StatusStep6,StatusStep7,StatusStep8,StatusStep9
MOCK_DATA = [
    ("1101", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success"),
    ("1102", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success"),
    ("1103", "Success", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart"),
    ("1104", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1105", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1106", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1107", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1108", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1109", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1110", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1111", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success"),
    ("1112", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success"),
    ("1113", "Success", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart"),
    ("1114", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1115", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1116", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1117", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1118", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1119", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1120", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1121", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success"),
    ("1122", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success", "Success"),
    ("1123", "Success", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart"),
    ("1124", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1125", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
    ("1126", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1127", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1128", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1129", "Success", "Success", "Success", "Fail",    "NotStart", "NotStart", "NotStart", "NotStart", "NotStart"),
    ("1130", "Success", "Success", "Success", "Success", "Success", "Inprogress", "NotStart", "NotStart", "NotStart"),
]

def normalize_status(status):
    """
    Normalizes a status string to one of the allowed STATUS_OPTIONS.
    """
    mapping = {
        "notstart": "NotStart",
        "inprogress": "InProgress",
        "success": "Success",
        "fail": "Fail"
    }
    return mapping.get(status.lower(), status)

def execute_query(query, params=None):
    """
    Connects to the PostgreSQL database, executes a query, and commits changes.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"❌ Error: {e}")

def generate_mock_data():
    """
    Inserts or updates static mock deployment data for stores using provided CSV data,
    ensuring each status is normalized to one of the allowed options.
    """
    print("🛠️ Generating mock data...")

    for row in MOCK_DATA:
        (
            store_name,
            status_step1,
            status_step2,
            status_step3,
            status_step4,
            status_step5,
            status_step6,
            status_step7,
            status_step8,
            status_step9,
        ) = row

        # Normalize statuses to ensure they match one of the allowed options
        statuses = [
            status_step1,
            status_step2,
            status_step3,
            status_step4,
            status_step5,
            status_step6,
            status_step7,
            status_step8,
            status_step9,
        ]
        normalized_statuses = [normalize_status(s) for s in statuses]

        # Set timestamps:
        # start_time is set to one day ago,
        # finished_time is set to current time only if all statuses are Success,
        # and last_update_time is the current time.
        start_time = datetime.now() - timedelta(days=1)
        if all(status == "Success" for status in normalized_statuses):
            finished_time = datetime.now()
        else:
            finished_time = None
        last_update_time = datetime.now()
        last_log = f"Static mock data inserted/updated for store {store_name}"

        query = """
            INSERT INTO deployment_status (
                store_name, status_step1, status_step2, status_step3, status_step4,
                status_step5, status_step6, status_step7, status_step8, status_step9,
                last_log, start_time, finished_time, last_update_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (store_name) DO UPDATE SET
                status_step1 = EXCLUDED.status_step1,
                status_step2 = EXCLUDED.status_step2,
                status_step3 = EXCLUDED.status_step3,
                status_step4 = EXCLUDED.status_step4,
                status_step5 = EXCLUDED.status_step5,
                status_step6 = EXCLUDED.status_step6,
                status_step7 = EXCLUDED.status_step7,
                status_step8 = EXCLUDED.status_step8,
                status_step9 = EXCLUDED.status_step9,
                last_log = EXCLUDED.last_log,
                start_time = EXCLUDED.start_time,
                finished_time = EXCLUDED.finished_time,
                last_update_time = EXCLUDED.last_update_time;
        """

        params = (
            store_name,
            *normalized_statuses,
            last_log,
            start_time,
            finished_time,
            last_update_time,
        )

        execute_query(query, params)
        print(f"✅ Mock data inserted/updated for store {store_name}")

if __name__ == "__main__":
    generate_mock_data()