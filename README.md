# Employee Performance Tracker

## Introduction
The **Employee Performance Tracker** is a data-driven project designed to evaluate and monitor employee performance using key metrics like review scores, project outcomes, and workload. This project generates synthetic data, stores it in a PostgreSQL database, extracts insights through SQL queries, and exports the results to CSV files. These CSV files can then be imported into **Power BI** for visualization, enabling deeper analysis of employee and organizational performance.

---

## Prerequisites for Running the Project
To run this project locally, ensure you have the following installed:

1. **Python**: Version 3.8 or later. [Download Python](https://www.python.org/downloads/)
2. **pip**: The Python package manager. It is usually bundled with Python.
3. **virtualenv**: For creating a virtual environment for the project. Install it using:
   ```bash
   pip install virtualenv
   ```
4. **PostgreSQL**: A relational database system. [Download PostgreSQL](https://www.postgresql.org/download/)
5. **Power BI**: Desktop version for visualizing the exported CSV data. [Download Power BI](https://powerbi.microsoft.com/)

---

## Setting Up the Project
1. **Clone the Repository** (if applicable) or create a project folder and add the provided code.
2. **Create a Virtual Environment**:
   ```bash
   virtualenv venv
   ```
   Activate it:
   - On Windows: `venv\Scripts\activate`
   - On Mac/Linux: `source venv/bin/activate`
3. **Install Dependencies**:
   Create a `requirements.txt` file (already provided) and run:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the Database**:
   Update the `DB_SETTINGS` dictionary in the code with your PostgreSQL credentials.
5. **Run the Script**:
   ```bash
   python main.py
   ```

---

## Methods Overview

### 1. **run_migrations**
This method executes SQL migration scripts to create necessary tables in the PostgreSQL database.

### 2. **clear_tables**
Clears all data from the database tables, ensuring a fresh start for each run.

### 3. **populate_database**
Generates synthetic employee, review, and project data and populates the database with these records.

### 4. **extract_data_to_csv**
Executes SQL queries to extract insights (e.g., average review scores, project completion trends) and saves the results to CSV files for visualization.

### 5. **main**
Coordinates the execution of all methods in sequence to complete the workflow: running migrations, clearing tables, populating data, and exporting CSV files.

---

## Package Usage and Rationale

1. **psycopg2**: To interact with the PostgreSQL database. It allows for executing SQL commands directly from Python.
2. **pandas**: For handling and exporting query results to CSV files efficiently.
3. **os**: For creating directories and handling file paths dynamically.
4. **random**: For generating diverse synthetic data.
5. **datetime**: For creating accurate timestamps and date-based data points.

---

## Power BI Guide
### Loading CSV Files into Power BI
1. **Open Power BI Desktop**.
2. Click on **"Get Data"** and select **"Text/CSV"**.
3. Browse and import the exported CSV files from the `output_csv` folder.

### Creating Relationships
1. Navigate to the **Model View** in Power BI.
2. Drag and drop fields to establish relationships between tables (e.g., `EmployeeID` between Employees and Reviews).
3. Ensure proper cardinality (e.g., one-to-many) and cross-filtering directions are set.

### Performing Transformations (if needed)
1. Go to the **Power Query Editor**.
2. Apply transformations, such as renaming columns, filtering rows, or splitting fields, as required.
3. Click **Close & Apply** to save changes.

### Creating Visualizations
1. In the **Report View**, drag fields into the canvas to create visuals:
   - **Bar Charts**: For department-wise project counts.
   - **Line Graphs**: For project completion trends over time.
   - **Pie Charts**: For budget adherence breakdowns.
   - **Tables**: For displaying top-performing employees.
2. Customize visuals using the formatting pane to make insights more accessible.
3. Save your report and export it as a PDF or share the `.pbix` file.

---

## Conclusion
The **Employee Performance Tracker** project provides a comprehensive framework for tracking employee and organizational performance. By leveraging PostgreSQL, Python, and Power BI, it ensures efficient data handling and insightful visualizations.

