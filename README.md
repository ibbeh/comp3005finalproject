# COMP 3005 Final Project - Soccer Events Database

## Overview
This project focuses on the design and implementation of a database system to store and query soccer event data across multiple competitions and seasons. The tasks include data importation from JSON files into a PostgreSQL database and executing queries as specified in the project guidelines.

### Team Members
- Ibraheem Refai (101259968)
- Abdulla Abdalla (101259092)
- Ahmed Elnimah (10127369)

**Last Updated:** 2024-04-12


## Prerequisites
Before you begin, ensure you have the following software installed:
- PostgreSQL (Verify version compatibility)
- pgAdmin 4 or equivalent PostgreSQL management tool
- Python 3.x for script execution

## Setup Instructions
1. **Database Setup:** Create a PostgreSQL database using pgAdmin.
Run the SQL script dbexport.sql to create tables and initialize schemas.
2. **Data Importation:** Ensure JSON data files are prepared in the data/events and data/lineups directories. Python scripts must be run in the specified order to correctly populate the database.

Note: deleteMatches.py and seasonMatchIDsExtractor.py are used to manage data selectively based on project requirements. Execute these scripts as needed to adjust the dataset.


# Directory Structure 
```
COMP_3005_Final_Project/
│
├── json_loader/
│   ├── 1-seasons.py/
│   ├── ...
│   └── seasonMatchIDsExtractor.py/
│
├── queries.sql/
│
├── dbexport.sql/
│
└── README.md

```

# Execution Instructions

To populate the database correctly, run the Python scripts located in src/ in the following order:

1. **seasons.py**
2. **countries.py**
3. **managers.py**
4. **stadiums.py**
5. **referees.py**
6. **teams.py**
7. **player_positions.py**
8. **matches.py**
9. **events.py**
10. **unique_events_1.py**
11. **unique_events_2.py**

## Running Scripts and Queries:  
1. **Script Execution**:
- Navigate to the root directory of the project.
- Execute Python scripts in the order listed above to populate the database: python src/seasons.py, etc.
2. **Query Execution**:
  - After populating the database, use pgAdmin or a similar tool to run queries directly against the PostgreSQL database.
# Project Report
- For detailed information including the ER model, database schema, and additional project details, please refer to our Project Report https://docs.google.com/document/d/1cvFwiHebgy-iq0zfb6QTHr2Ubg-0gJ6eFI7Iu-wkEOs/edit?usp=sharing.
- 
## Submission and Grading
This project is submitted through a Google Form link. Grading will focus on the report, query correctness, and efficiency as outlined in the project specification document.

Important: Ensure your PostgreSQL database is configured and running with the correct credentials as specified in the project documentation.


