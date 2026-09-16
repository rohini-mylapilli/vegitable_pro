# Vegetable Store Management & Business Reporting System

A Python and MySQL-based application designed to manage vegetable store operations, inventory data, customer transactions, and business reports.

This project demonstrates practical skills relevant to both **Python Development** and **Data Analytics**, including Python programming, database integration, SQL-based data management, CRUD operations, transaction processing, and business report generation.

## Key Features

- Owner authentication
- Add, update, and remove vegetable records
- Inventory management
- Customer transaction handling
- Product quantity and pricing management
- Customer report generation
- Profit report generation
- MySQL database integration
- SQL-based data retrieval and manipulation
- Input validation and menu-driven operations

## Technical Skills Demonstrated

### Python Development

- Python programming
- Functions and modular logic
- Conditional statements and loops
- User input handling
- Database connectivity
- CRUD operations
- Business logic implementation

### Database & SQL

- MySQL database integration
- SQL queries
- INSERT, SELECT, UPDATE, and DELETE operations
- Database-driven inventory management
- Transaction data handling
- Structured data storage and retrieval

### Data & Business Reporting

- Inventory data management
- Customer transaction analysis
- Cost and selling price tracking
- Profit calculation and reporting
- Customer report generation
- Business data retrieval using SQL

## Technologies Used

- Python
- MySQL
- SQL
- MySQL Connector for Python

## Project Workflow

The application connects Python with a MySQL database to manage store data.

The owner can manage inventory by adding, updating, removing, and viewing vegetable records. Customer transactions are processed through the application, while stored business data is used to generate customer and profit reports.

## Project Structure

```text
veg_database_project/
│
├── veg_database_project.py
└── README.md
```

## Database Configuration

The application requires a local MySQL database connection.

Before running the project, update the database configuration with your own MySQL credentials:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="vegetable"
)
```

> Do not upload your actual database password or other credentials to GitHub.

## Installation

Install the required MySQL connector:

```bash
pip install mysql-connector-python
```

## Run the Application

```bash
python veg_database_project.py
```

## Learning Outcomes

Through this project, I gained practical experience in:

- Building Python applications with database integration
- Connecting Python applications to MySQL
- Performing SQL CRUD operations
- Managing inventory and transaction data
- Implementing business logic using Python
- Retrieving and processing structured data
- Generating customer and profit reports from business data

## Career Relevance

This project demonstrates foundational skills applicable to:

**Python Development**
- Python programming
- MySQL integration
- Application logic
- CRUD operations
- Database-driven application development

**Data Analytics**
- SQL querying
- Structured data management
- Business data retrieval
- Transaction and inventory data handling
- Profit and customer reporting

## Author

**Rohini Mylapilli**  
Python Full Stack Developer