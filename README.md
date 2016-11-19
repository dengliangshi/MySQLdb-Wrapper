# MySQLdb Wrapper
A simple wrapper for MySQLdb, supports comman database operations with friendly interfaces.

## Usage
Build up connection to MySQL server using this module: 
```
>> from mysqldb_ex import MySQLdb_Ex

>> db = MySQLdb_Ex(host='localhost',  # host name of MySQL server
                port=3306,         # port number of MySQL server, default is 3306
                user='root',       # user account for connecting to MySQL server, default is None
                password='123456', # password for connecting to MySQL server, default is None
                db_name='test')    # database name
>> db
>> <Server: localhost:3306, Version: 5.6.31-log, Status: connected>
>> db  # if disconnect
>> <Server: localhost:3306, Status: disconnected>
```

Table example(table's name is 'users'):

| ID |    Name    | FirstName | LastName |    Job   |  Pay  |
|:--:|:-----------|:----------|:---------|:---------|:------|
| 1  | John Smith | John      | Smith    | Manager  | 12000 |
| 2  | Peter Lutz | Peter     | Lutz     | Teacher  | 6000  |
| 3  | Tom Jones  | Tom       | Jones    | Engineer | 8000  |

* Get fields' name of any table:
```
>> db.get_fields(table='users')
>> [u'ID', u'Name', u'FirstName', u'LastName', u'Job', u'Pay']
```

* Get records from any table:
```
>> db.get(table='users')
>> <MySQLdb.cursors.SSDictCursor object at 0x01875F30>
>> list(db.get(table='users'))
>> ({'Name': u'John Smith', 'FirstName': u'John', 'Pay': 1200L, 
     'Job': u'Manager', 'LastName': u'Smith', 'ID': 1L}, 
    {'Name': u'Peter Lutz', 'FirstName': u'Peter', 'Pay': 6000L, 
     'Job': u'Teacher', 'LastName': u'Lutz', 'ID': 2L}, 
    {'Name': u'Tom Jones', 'FirstName': u'Tom', 'Pay': 8000L, 
     'Job': u'Engineer', 'LastName': u'Jones', 'ID': 3L})

>> db.get(table='users', fields=['Name', 'Pay'], conditions=['Job="Teacher"', 'OR', 'Job="Engineer"'])
>> ({'Pay': 6000L, 'Name': u'Peter Lutz'}, 
    {'Pay': 8000L, 'Name': u'Tom Jones'})
```

* Delete an record in any table
```
>> db.delete(table='users', conditions=['FirstName="John"', 'AND', 'LastName="Smith"'])
>> 1  # the number of records have been deleted
```

* Insert a new record into any table
```
>> db.insert(table='users', data={'Name': 'John Smith', 'FirstName': 'John', 'Pay': 1200, 
        'Job': 'Manager', 'LastName': 'Smith'})
>> 4  # the row id for this new record
```

* Update records in any table
```
>> db.update(table='users', data={'Pay': 7000})
>> 3  # the number of records have been changed
>> db.get(table='users', fields=['Name', 'Pay'])
>> ({'Pay': 7000L, 'Name': u'Peter Lutz'}, 
    {'Pay': 7000L, 'Name': u'Tom Jones'}, 
    {'Pay': 7000L, 'Name': u'John Smith'})

>> db.update(table='users', data={'Pay': 9000}, conditions=['Name="John Smith"', ])
>> 1
>> db.get(table='users', fields=['Name', 'Pay'])
>> ({'Pay': 7000L, 'Name': u'Peter Lutz'}, 
    {'Pay': 7000L, 'Name': u'Tom Jones'}, 
    {'Pay': 9000L, 'Name': u'John Smith'})
```

* Clear up any table
```
>> db.clear_table(table='users')
>> db.get(table='users')
>> ()
```

## Cursor Class
Default, mysqldb returns query result as rows, but in practice, results as a dict may be more usable. So the cursor class is set to be MySQLdb.cursors.SSDictCursor in this module. In additon, with this cursor class, query results will be saved in server and return a iterator which will save space and maybe enhance efficiency.

## Timeout Issue
MySQL server will automatically break the connection to any client which keeps unactive for a certain time, default is 8 hours, and MySQLdb will raise an error when excuting any SQL query in this case. This module deals with this issue by reconnecting to the server when catch the error.

## License
The module is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
