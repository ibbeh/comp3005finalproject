# COMP 3005 Final Project README

## Overview
This project involves designing and implementing a database to store and query a soccer events dataset spanning multiple competitions and seasons. Our task includes data importation from JSON format into PostgreSQL and querying the database as per the specifications provided. This README outlines the setup instructions, project structure, and compilation steps necessary to run the project.


### Team Members
- Ibraheem Refai (101259968)
- Abdulla Abdalla (101259092)
- Ahmed Elnimah (10127369)

**Last Updated:** 2024-04-02


## Prerequisites
Before you begin, ensure the following software is installed:
- Java Development Kit (JDK)
- PostgreSQL (Ensure version compatibility)
- pgAdmin 4 or later

## Setup Instructions
1. **Database Setup:** Use pgAdmin to create a database that matches the credentials specified in `PostgreSQLStudentDBConnectionA3Q1.java`.
2. **Table Creation and Data Initialization:** Execute the SQL script found in `createAndInitializeStudentDB.sql` within the `sql` directory using the pgAdmin query tool.

## Video Demonstration
For a comprehensive walkthrough of the project's functionality and features, refer to our video demonstrations:
- [Video Link 1]()
- [Video Link 2]()

# Directory Structure 
```
comp3005finalproject/
│
├── data/
│   └──
│
├── docs/
│   └── 
│
│── src/
│   └── 
│
|── tests/
│   └── 
│
└── README.md
```

# Compilation & Execution Instructions

Navigate to the root directory of the project (COMP_3005_Assignment_3/) and run the following command in a terminal to compile PostgreSQLStudentDBConnectionA3Q1.java:

```
javac -cp ".;libraries/*" src/PostgreSQLStudentDBConnectionA3Q1.java -d src
```

After successful compilation, from the root directory root directory of the project (COMP_3005_Assignment_3/), run the application by executing the following command in a terminal: 

```
java -cp ".;libraries/*;src" PostgreSQLStudentDBConnectionA3Q1
```

## NOTES:   
- On Unix-based system, replace ';' with ':' in the classpath separator.  
- Ensure your PostgreSQL database is running and accessible with the credentials and URL specified in the PostgreSQLStudentDBConnectionA3Q1.java file.

# Functions Information
- getAllStudents(): Retrieves and displays all records from the students table.
- addStudent(first_name, last_name, email, enrollment_date): Inserts a new student record into the students table.
- updateStudentEmail(student_id, new_email): Updates the email address for a student with the specified student_id.
- deleteStudent(student_id): Deletes the record of the student with the specified student_id.

## Submission and Grading
This project will be submitted via a Google Form link, adhering to the due date of **April 10th, 2024 (11:59 PM)**. It includes a comprehensive grading rubric focusing on project reports, query correctness, and efficiency.

For detailed submission instructions and the grading rubric, refer to the project specification document.

