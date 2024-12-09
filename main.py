import os
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import random

# Environment file configuration
DB_SETTINGS = {
    "dbname": os.getenv("DB_NAME", "epts"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
}

OUTPUT_DIR = "output_csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def connect_db():
    """Establish database connection."""
    return psycopg2.connect(**DB_SETTINGS)

def clear_tables():
    """Clear all table data."""
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE performance_reviews, projects, employees RESTART IDENTITY CASCADE;")
        print("Tables cleared successfully.")
        
# Path to migration file
MIGRATION_FILE = "migrations/001_create_tables.up.sql"

def run_migrations():
    """Run SQL migrations to set up the database schema."""
    with open(MIGRATION_FILE, "r") as file:
        migration_sql = file.read()
    with psycopg2.connect(**DB_SETTINGS) as conn:
        with conn.cursor() as cursor:
            cursor.execute(migration_sql)
        print("Migrations executed successfully.")

def populate_database():
    """Generate and populate synthetic data."""
    today = datetime.today()
    employees = [{"EmployeeID": i, "Name": f"Employee_{i}", "Department": random.choice(["HR", "IT", "Finance"]),
                  "JoiningDate": (today - timedelta(days=random.randint(365, 2000))).strftime("%Y-%m-%d")}
                 for i in range(1, 101)]
    reviews = []
    projects = []
    for emp in employees:
        for _ in range(random.randint(1, 5)):
            reviews.append({"EmployeeID": emp["EmployeeID"], "ReviewScore": random.randint(1, 5),
                            "ReviewDate": (today - timedelta(days=random.randint(30, 500))).strftime("%Y-%m-%d"),
                            "Reviewer": f"Reviewer_{random.randint(1, 10)}"})
        for _ in range(random.randint(1, 3)):
            start_date = today - timedelta(days=random.randint(100, 300))
            deadline_date = start_date + timedelta(days=random.randint(30, 90))
            completion_date = deadline_date + timedelta(days=random.randint(-15, 30))
            projects.append({
                "ProjectName": f"Project_{random.randint(1, 1000)}",
                "EmployeeID": emp["EmployeeID"],
                "DeadlineMet": "Yes" if completion_date <= deadline_date else "No",
                "BudgetAdherence": random.choice(["Within Budget", "Exceeded Budget"]),
                "StartDate": start_date.strftime("%Y-%m-%d"),
                "Deadline": deadline_date.strftime("%Y-%m-%d"),
                "CompletionDate": completion_date.strftime("%Y-%m-%d"),
            })

    with connect_db() as conn:
        with conn.cursor() as cursor:
            for emp in employees:
                cursor.execute(
                    "INSERT INTO employees (name, department, joining_date) VALUES (%s, %s, %s)",
                    (emp["Name"], emp["Department"], emp["JoiningDate"]),
                )
            for rev in reviews:
                cursor.execute(
                    "INSERT INTO performance_reviews (employee_id, review_score, review_date, reviewer) VALUES (%s, %s, %s, %s)",
                    (rev["EmployeeID"], rev["ReviewScore"], rev["ReviewDate"], rev["Reviewer"]),
                )
            for proj in projects:
                cursor.execute(
                    "INSERT INTO projects (project_name, employee_id, deadline_met, budget_adherence, start_date, deadline, completion_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (proj["ProjectName"], proj["EmployeeID"], proj["DeadlineMet"], proj["BudgetAdherence"],
                     proj["StartDate"], proj["Deadline"], proj["CompletionDate"]),
                )
        print("Database populated successfully.")

def extract_data_to_csv(query, filename):
    """Run SQL query and save result to CSV."""
    with connect_db() as conn:
        df = pd.read_sql_query(query, conn)
        output_path = os.path.join(OUTPUT_DIR, filename)
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")

def main():
    run_migrations()
    clear_tables()
    populate_database()

    queries = {
        # Employee performance with average review scores
        "employee_performance.csv": """
            SELECT e.name, e.department, AVG(r.review_score) AS avg_score
            FROM employees e
            JOIN performance_reviews r ON e.id = r.employee_id
            GROUP BY e.name, e.department
            ORDER BY avg_score DESC;
        """,

        # Project completion trends over time
        "project_trends.csv": """
            SELECT DATE_TRUNC('month', completion_date) AS month, COUNT(*) AS projects_completed
            FROM projects
            GROUP BY month
            ORDER BY month;
        """,

        # Department-wise project count
        "department_project_count.csv": """
            SELECT e.department, COUNT(p.id) AS total_projects
            FROM employees e
            JOIN projects p ON e.id = p.employee_id
            GROUP BY e.department
            ORDER BY total_projects DESC;
        """,

        # Employee-specific project success rates
        "employee_project_success.csv": """
            SELECT e.name, 
                COUNT(p.id) AS total_projects, 
                ROUND((SUM(CASE WHEN p.deadline_met = 'Yes' THEN 1 ELSE 0 END)::DECIMAL / COUNT(p.id)) * 100, 2) AS success_rate
            FROM employees e
            JOIN projects p ON e.id = p.employee_id
            GROUP BY e.name
            ORDER BY success_rate DESC, total_projects DESC;
        """,

        # Department-specific project success rates
        "department_project_success.csv": """
            SELECT e.department, 
                COUNT(p.id) AS total_projects, 
                ROUND((SUM(CASE WHEN p.deadline_met = 'Yes' THEN 1 ELSE 0 END)::DECIMAL / COUNT(p.id)) * 100, 2) AS success_rate
            FROM employees e
            JOIN projects p ON e.id = p.employee_id
            GROUP BY e.department
            ORDER BY success_rate DESC, total_projects DESC;
        """,

        # Budget adherence trends over time
        "budget_adherence_trends.csv": """
            SELECT DATE_TRUNC('month', completion_date) AS month,
                SUM(CASE WHEN p.budget_adherence = 'Within Budget' THEN 1 ELSE 0 END) AS within_budget,
                SUM(CASE WHEN p.budget_adherence = 'Exceeded Budget' THEN 1 ELSE 0 END) AS exceeded_budget
            FROM projects p
            GROUP BY month
            ORDER BY month;
        """,

        # Employee-specific average project duration
        "employee_project_duration.csv": """
            SELECT e.name, 
                ROUND(AVG(p.completion_date - p.start_date), 2) AS avg_project_duration
            FROM employees e
            JOIN projects p ON e.id = p.employee_id
            GROUP BY e.name
            ORDER BY avg_project_duration ASC;
        """,

        # Project performance trends (Deadline met vs not met)
        "project_performance_trends.csv": """
            SELECT DATE_TRUNC('month', completion_date) AS month,
                SUM(CASE WHEN p.deadline_met = 'Yes' THEN 1 ELSE 0 END) AS met_deadline,
                SUM(CASE WHEN p.deadline_met = 'No' THEN 1 ELSE 0 END) AS missed_deadline
            FROM projects p
            GROUP BY month
            ORDER BY month;
        """
    }

    for filename, query in queries.items():
        extract_data_to_csv(query, filename)

if __name__ == "__main__":
    main()
