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
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

def execute_query(query, params=None, fetch=False):
    """
    Connects to the PostgreSQL database, executes a query, and commits changes.
    If `fetch=True`, it returns the query results.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query, params)

        if fetch:
            result = cur.fetchall()
        else:
            result = None
            conn.commit()

        cur.close()
        conn.close()
        return result

    except psycopg2.Error as e:
        print(f"❌ Error: {e}")

# 1️⃣ Example Insert (No Need to Define Status)
def insert_new_store(store_name):
    """
    Inserts a new store deployment record.
    Since status columns have a default value of 'NotStart', they do not need to be explicitly set.
    """
    query = "INSERT INTO deployment_status (store_name) VALUES (%s);"
    execute_query(query, (store_name,))
    print(f"✅ Deployment started for store: {store_name}")

# 2️⃣ Query Examples with Default Values

# 2.1 Start Deployment for a Store (Automatically "NotStart" for All Steps)
def start_deployment(store_name):
    """
    Initializes a deployment for a store.
    Since 'NotStart' is the default value for all steps, this just inserts a new record.
    """
    insert_new_store(store_name)

# 2.2 Update Step Status When a Step Starts
def update_step_status(store_name, step_number, status, log_message=""):
    """
    Updates the status of a specific step for a given store.
    Valid statuses: 'NotStart', 'InProgress', 'Success', 'Fail'
    """
    column_name = f"status_step{step_number}"  # Dynamically determine column name
    query = f"""
        UPDATE deployment_status
        SET {column_name} = %s, last_log = %s, last_update_time = NOW()
        WHERE store_name = %s;
    """
    execute_query(query, (status, log_message, store_name))
    print(f"✅ Step {step_number} updated to '{status}' for store: {store_name}")

# 2.3 Mark a Step as Successful
def mark_step_success(store_name, step_number):
    """
    Marks a specific step as 'Success' for a given store.
    """
    update_step_status(store_name, step_number, "Success", f"Step {step_number} completed successfully.")

# 2.4 Find All Stores Where Deployment is Still Running
def find_running_deployments():
    """
    Retrieves all stores where deployment is still in progress (i.e., finished_time is NULL).
    """
    query = "SELECT store_name FROM deployment_status WHERE finished_time IS NULL;"
    results = execute_query(query, fetch=True)
    if results:
        print("🚀 Running Deployments:", [row[0] for row in results])
    else:
        print("✅ No active deployments.")

# 2.5 Find Stores Where Any Step is "Fail"
def find_failed_deployments():
    """
    Retrieves all stores where any step has failed.
    """
    query = """
        SELECT store_name FROM deployment_status 
        WHERE status_step1 = 'Fail'
           OR status_step2 = 'Fail'
           OR status_step3 = 'Fail'
           OR status_step4 = 'Fail'
           OR status_step5 = 'Fail'
           OR status_step6 = 'Fail'
           OR status_step7 = 'Fail'
           OR status_step8 = 'Fail'
           OR status_step9 = 'Fail';
    """
    results = execute_query(query, fetch=True)
    if results:
        print("❌ Stores with Failed Steps:", [row[0] for row in results])
    else:
        print("✅ No stores have failed steps.")

# 3️⃣ Delete a Store Deployment
def delete_store(store_name):
    """
    Deletes a store's deployment record from the database.
    """
    query = "DELETE FROM deployment_status WHERE store_name = %s;"
    execute_query(query, (store_name,))
    print(f"🗑️ Deployment record deleted for store: {store_name}")

# Example usage
if __name__ == "__main__":
    print("🔹 Running Database Operations 🔹")

    # Example Inserts
    start_deployment("1101")
    start_deployment("1102")

    # Update Steps
    update_step_status("1101", 1, "InProgress", "Step 1 is in progress.")
    mark_step_success("1101", 1)
    update_step_status("1101", 2, "Fail", "Step 2 encountered an error.")

    # Queries
    find_running_deployments()
    find_failed_deployments()

    # Delete a store
    delete_store("1102")
