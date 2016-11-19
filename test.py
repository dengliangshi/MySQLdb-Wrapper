#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library


# Third-party libraries


# User define module
from mysqldbex import MySQLdbEx

# ----------------------------------------------------Global Variables------------------------------------------------------
db = MySQLdbEx(host='localhost', user='root', password='123456', db_name='mysqldb')
print db
# ---------------------------------------------------------Tests------------------------------------------------------------
"""
In order to run these test code, you should have a table named 'users' in your database, which likes:
| ID |    Name    | FirstName | LastName |    Job   |  Pay  |
|:--:|:-----------|:----------|:---------|:---------|:------|
| 1  | John Smith | John      | Smith    | Manager  | 12000 |
| 2  | Peter Lutz | Peter     | Lutz     | Teacher  | 6000  |
| 3  | Tom Jones  | Tom       | Jones    | Engineer | 8000  |
"""

# Get the column name of a table. 
print db.get_fields(table='users')

# Get all records in a table.
print db.get('users')
print list(db.get('users'))

# Get records filted by conditions.
print list(db.get(table='users', conditions=['job="Teacher"', ]))

# Get specified columns of the records filted by conditions.
print list(db.get(table='users', fields=['firstname', 'pay'], 
            conditions=['job="Teacher"', 'OR', 'job="Engineer"']))

# Delete any records in table.
print db.delete(table='users', conditions=['firstname="Mary"', 
            'AND', 'lastname="Chun"'])
print list(db.get('users'))

# Insert a new record into table.
print db.insert(table='users', data={'Name': 'John Smith', 'FirstName': 'John', 'Pay': 1200, 
        'Job': 'Manager', 'LastName': 'Smith'})
print list(db.get('users'))

# update any records.
print db.update(table='users', data={'Pay': 7000})
print list(db.get(table='users', fields=['Name', 'Pay']))

print db.update(table='users', data={'Pay': 9000}, conditions=['Name="John Smith"', ])
print list(db.get(table='users', fields=['Name', 'Pay']))

# Clear up a table
db.clear_table(table='users')
print list(db.get(table='users'))