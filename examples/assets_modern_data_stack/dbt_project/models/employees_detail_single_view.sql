{# {{
config(
     materialized='materialized_view',
)
}} #}
SELECT  e.emp_no,
        e.birth_date,
        e.first_name,
        e.last_name,
        e.gender,
        e.hire_date,
        d.dept_no,
        d.dept_name,
        m.from_date as dept_manager_from_date,
        m.to_date as dept_manager_to_date, 
        de.from_date as dept_emp_from_date,
        de.to_date as dept_emp_to_date,
        t.title,
        t.from_date as title_from_date,
        t.to_date as title_to_date,
        s.salary,
        s.from_date as salary_from_date,
        s.to_date as salary_to_date
FROM {{ source('ql_ws', 'employees') }} e
FULL JOIN {{ source('ql_ws', 'dept_emp') }} de ON e.emp_no = de.emp_no
FULL JOIN {{ source('ql_ws', 'departments') }} d ON de.dept_no = d.dept_no
FULL JOIN {{ source('ql_ws', 'titles') }} t ON e.emp_no = t.emp_no
FULL JOIN {{ source('ql_ws', 'salaries') }} s ON e.emp_no = s.emp_no
FULL JOIN {{ source('ql_ws', 'dept_manager') }} m ON e.emp_no = m.emp_no
order by e.emp_no,d.dept_no,m.from_date desc

