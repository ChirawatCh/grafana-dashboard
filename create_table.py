import psycopg2
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

# SQL Statements to drop tables if they exist (rebuild them)
DROP_STEPS_TABLE = "DROP TABLE IF EXISTS steps CASCADE;"
DROP_DEPLOYMENT_STATUS_TABLE = "DROP TABLE IF EXISTS deployment_status CASCADE;"

# SQL Statements to create tables
CREATE_STEPS_TABLE = """
CREATE TABLE steps (
    id SERIAL PRIMARY KEY,
    step_number INT UNIQUE NOT NULL,
    step_name VARCHAR(255) UNIQUE NOT NULL,
    expected_duration VARCHAR(20) NOT NULL
);
"""

CREATE_DEPLOYMENT_STATUS_TABLE = """
CREATE TABLE deployment_status (
    store_name VARCHAR(50) PRIMARY KEY,
    status_step1 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step1 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step2 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step2 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step3 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step3 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step4 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step4 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step5 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step5 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step6 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step6 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step7 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step7 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step8 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step8 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    status_step9 VARCHAR(20) DEFAULT 'NotStart' CHECK (status_step9 IN ('NotStart', 'InProgress', 'Success', 'Fail')),
    last_log TEXT,
    start_time TIMESTAMP DEFAULT NOW(),
    finished_time TIMESTAMP,
    last_update_time TIMESTAMP DEFAULT NOW()
);
"""

# SQL Statement to create an index on store_name in deployment_status.
# (This is redundant with the primary key index, but shown here per your request.)
CREATE_INDEX_STORE_NAME = "CREATE INDEX idx_store_name ON deployment_status(store_name);"

# SQL Statement to insert predefined steps
INSERT_STEPS = """
INSERT INTO steps (step_number, step_name, expected_duration) VALUES
(1, 'Install Provider Adapter', '5 Min'),
(2, 'Install GX Server', '5 Min'),
(3, 'Install POS Client', '5 Min'),
(4, 'Logon to Office Client set DMS_Server', '5 Min'),
(5, 'RabbitMQServerMaintenance_POS at POS', '5 Min'),
(6, 'Run RTI Backup & Cold Start POS', '30 Min'),
(7, 'Install Loyalty adapter', '5 Min'),
(8, 'Create TouchPoint (POS No) every POS', '5 Min'),
(9, 'Register POS', '5 Min')
ON CONFLICT (step_name) DO NOTHING;
"""

def connect_and_execute():
    """Connect to PostgreSQL, rebuild tables, insert steps, and create index."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Drop tables if they exist
        cur.execute(DROP_DEPLOYMENT_STATUS_TABLE)
        cur.execute(DROP_STEPS_TABLE)

        # Create tables
        cur.execute(CREATE_STEPS_TABLE)
        cur.execute(CREATE_DEPLOYMENT_STATUS_TABLE)

        # Insert predefined steps into steps table
        cur.execute(INSERT_STEPS)

        # Create index on store_name in deployment_status
        cur.execute(CREATE_INDEX_STORE_NAME)

        # Commit changes and close connection
        conn.commit()
        cur.close()
        conn.close()

        print("✅ Tables rebuilt successfully, steps inserted and index created!")

    except psycopg2.Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    connect_and_execute()