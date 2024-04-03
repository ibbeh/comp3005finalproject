# COMP 3005 Final Project README

Database Interaction with PostgreSQL and Application Programming for COMP 3005 Assignment 3

Authors: Ibraheem Refai, Abdulla Abdalla, Ahmed Elnimah  
Student IDs: 101259968, 101259092, 101273769
Last Updated: 2024-04-2

## Before Starting
- Ensure you have the Java Development Kit (JDK) installed
- Ensure you have pgAdmin4 or later installed
- Create a database in pgAdmin and ensure it is compatible with the credentials and URL specified in the PostgreSQLStudentDBConnectionA3Q1.java file
- Create the tables required and initialize data using the query tool in pgAdmin4. Run the query in the 'createAndInitializeStudentDB.sql' file in the sql directory

# Video Demonstration (IMPORTANT)
https://youtu.be/z4wEbmgiYgQ
OR
https://youtu.be/z4wEbmgiYgQ?si=aDTD6WXtgCp5dajP

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
|
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

