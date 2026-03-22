-- =========================
-- Query 1 — Count of employees per city
-- =========================

-- Q1: How many employees are in each city?
SELECT
    address_city     AS city,      -- Select the city from the address_city column and rename it as "city"
    COUNT(*)         AS employee_count  -- Count total number of rows (employees) in each city
FROM dbo.employees               -- Source table containing employee data
GROUP BY address_city           -- Group records based on each unique city
ORDER BY employee_count DESC;   -- Sort results from highest to lowest employee count



-- =========================
-- Query 2 — Average salary by department
-- =========================

-- Q2: What is the average salary per department?
SELECT
    department,                 -- Department name
    COUNT(*)             AS headcount,   -- Total number of employees in each department
    ROUND(AVG(salary),2) AS avg_salary,  -- Average salary rounded to 2 decimal places
    MIN(salary)          AS min_salary,  -- Lowest salary in the department
    MAX(salary)          AS max_salary   -- Highest salary in the department
FROM dbo.employees             -- Source employee table
GROUP BY department           -- Group records by department
ORDER BY avg_salary DESC;     -- Sort departments by highest average salary



-- =========================
-- Query 3 — Salary band distribution
-- =========================

-- Q3: How are employees distributed across salary bands?
SELECT
    salary_band,                     -- Salary category (e.g., Low, Medium, High)
    COUNT(*) AS count,              -- Number of employees in each salary band
    ROUND(AVG(salary),2) AS avg_salary_in_band  -- Average salary within each band (rounded)
FROM dbo.employees                 -- Source employee table
GROUP BY salary_band              -- Group data by salary band
ORDER BY avg_salary_in_band DESC; -- Sort bands by highest average salary



-- =========================
-- Query 4 — Employees above company average salary
-- =========================

-- Q4: Which employees earn above the company average?
SELECT
    name,                          -- Employee name
    department,                    -- Department the employee belongs to
    salary,                        -- Employee salary
    ROUND(salary - AVG(salary) OVER (), 2) AS diff_from_avg  
    -- Calculate the difference between each employee's salary and the overall company average
    -- AVG(salary) OVER () computes the average salary across ALL rows (no grouping)
FROM dbo.employees                -- Source employee table
ORDER BY salary DESC;            -- Sort employees from highest to lowest salary
