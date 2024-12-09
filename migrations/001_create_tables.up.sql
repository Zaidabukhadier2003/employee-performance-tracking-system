-- employees table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    joining_date DATE NOT NULL
);

-- performance_reviews table
CREATE TABLE IF NOT EXISTS performance_reviews (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    review_score INT NOT NULL CHECK (review_score BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    reviewer VARCHAR(255) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE
);

-- projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    deadline_met BOOLEAN NOT NULL,
    budget_adherence VARCHAR(255) NOT NULL,
    employee_id INT NOT NULL,
    start_date DATE NOT NULL,
    deadline DATE NOT NULL,
    completion_date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE
);
