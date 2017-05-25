#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library


# Third-party libraries


# User define module
from mysqldbex import MySQLdbEx

# ----------------------------------------------------Global Variables------------------------------------------------------
db = MySQLdbEx(host='localhost', user='root', password='ydm830025', db_name='mysqldb')
print db.connect()
print db

# generate uuid
print db.uuid()

# ---------------------------------------------------------Tests------------------------------------------------------------
"""
To run these test code, you should have a table named 'users' in database 'mysqldb', which likes:
| ID |    Name    | FirstName | LastName |    Job   |  Pay  |
|:--:|:-----------|:----------|:---------|:---------|:------|
| 1  | John Smith | John      | Smith    | Manager  | 12000 |
| 2  | Peter Lutz | Peter     | Lutz     | Teacher  | 6000  |
| 3  | Tom Jones  | Tom       | Jones    | Engineer | 8000  |
"""

# Insert new records
print db.insert(table='users', data={'Name': 'John Smith', 'FirstName': 'John', 'Pay': 12000, 
        'Job': 'Manager', 'LastName': 'Smith'})
print db.insert(table='users', data={'Name': 'Peter Lutz', 'FirstName': 'Peter', 'Pay': 6000, 
        'Job': 'Teacher', 'LastName': 'Lutz'})
print db.insert(table='users', data={'Name': 'Tom Jones', 'FirstName': 'Tom', 'Pay': 8000, 
        'Job': 'Engineer', 'LastName': 'Jones'})

# Get the column name of a table. 
print db.get_fields(table='users')

# Count the number of records
print db.count(table='users')

# Get a specified page of records
print db.get_page(table='users', page=0, number=10, order='Name ASC')

# Get all records in a table.
print db.get('users')

# Get one record filted by conditions.
print db.get_one(table='users', conditions=['job="Teacher"', ])

# Get one record filted by conditions.
print db.get_one(table='users', conditions=['job="Teacher"', ])

# Get specified columns of the records filted by conditions.
print db.get(table='users', fields=['firstname', 'pay'], 
            conditions=['job="Teacher"', 'OR', 'job="Engineer"'])

# Insert a new record into table.
print db.insert(table='users', data={'Name': 'Mary Chun', 'FirstName': 'Mary', 'Pay': 1200, 
        'Job': 'HR', 'LastName': 'Chun'})
print db.get('users')

# Delete any records in table.
print db.delete(table='users', conditions=['FirstName="Mary"', 
            'AND', 'LastName="Chun"'])
print db.get('users')

# update any records.
print db.update(table='users', data={'Pay': 7000})
print db.get(table='users', fields=['Name', 'Pay'])

print db.update(table='users', data={'Pay': 9000}, conditions=['Name="John Smith"', ])
print db.get(table='users', fields=['Name', 'Pay'])

# Clear up a table
print db.clear_table(table='users')
print db.get(table='users')