#encoding=utf-8

# -----------------------------------------------------------libraries------------------------------------------------------
# Standard library


# Third-party libraries
import MySQLdb
import MySQLdb.cursors

# User define module


# --------------------------------------------------------Global Variables--------------------------------------------------


# --------------------------------------------------------Class MySQLdbEx---------------------------------------------------
class MySQLdbEx(object):
    """This class is responsible for building up and shutting down connection to mysql server,
        and common database operations.
    """
    def __init__(self, host=None, db_name=None, port=3306, user=None, password=None):
        """Constructor.
        :Param(str) db_host: the host name of mysql server
        :Param(str) db_user: user name to login mysql server
        :Param(str) db_password: user name to login mysql server
        :Param(str) db_name: the name of database
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = None  # client object

    def __repr__(self):
        """Instance display format.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT version()')
        except Exception:
            return '<Server: %s:%d, Status: disconnected>' % (self.host, self.port)
        return '<Server: %s:%d, Version: %s, Status: connected>' % (self.host, 
            self.port, cursor.fetchone()['version()'])

    def connect(self):
        """ Building up connection to mysql server if not.
        -Param(str) db_host: the host name of database server
        -Param(str) db_user: user name to login database server
        -Param(str) db_password: user name to login database server
        -Param(str) db_name: the name of database
        """
        if self.connection is not None:
            self.disconnect()
        self.connection = MySQLdb.connect(host=self.host, port=self.port, user=self.user,
            passwd=self.password, db=self.db_name, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)

    def disconnect(self):
        """Close the connection to mysql server.
        """
        try:
            if self.connection is not None:
                self.connection.close()
                self.connection = None
        except Exception as e:
            print "Failed to close the connection to database: %s" % e
        self.connection = None

    def execute(self, sql):
        """Execute SQL command.
        :Param(str) sql: SQL command string.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()  # reconnect to mysql service if disconnect
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        return cursor

    def query(self, sql):
        """Get records from database.
        :Param(str) sql: SQL command string
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()  # reconnect to mysql service if disconnect
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
        return cursor.fetchall()

    def uuid(self):
        """Generate uuid using the function UUID().
        """
        sql = 'SELECT UUID()'
        record = self.query(sql)
        return record[0]['UUID()']

    def is_exists(self, table, conditions):
        """Check if one or more records exist for given conditions, like:
        ['field1=value1', 'AND', 'field2>value2', 'OR', 'field3<>value3', ...]
        :Param(str) table: the name of target table
        :Param(list) conditions: the conditions for records to be seleted
        """
        sql = 'SELECT * FROM %s WHERE %s LIMIT 1' % (table, ' '.join(conditions))
        record = self.query(sql)
        return True if record else False

    def get_fields(self, table):
        """Get the field names of a table.
        :Param(str) table: the name of target table
        """
        sql = ('SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE ' +
              'table_name = %r AND table_schema = %r' % (table, self.db_name))
        return [x['COLUMN_NAME'] for x in self.query(sql)]

    def count(self, table, conditions=["1",]):
        """Count records from database according to given conditions, like:
        ["field1=value1", "AND", "field2>value2", "OR", "field3<>value3", ...]
        :Param(str) table: the name of target table
        :Param(list) conditions: the conditions for records to be seleted
        """
        sql = "SELECT COUNT(*) AS 'count' FROM %s WHERE %s " % (table, " ".join(conditions))
        record = self.query(sql)
        return record[0]['count']

    def get_page(self, table, page, number, order="ID ASC", fields="*", conditions=["1",]):
        """Get a page of records from database according to given conditions, like:
        ["field1=value1", "AND", "field2>value2", "OR", "field3<>value3", ...]
        :Param(str) table: the name of target table
        :Param(int) page: page index of records
        :Param(int) number: number of records will be return
        :Param(list) fields: the name of columns whose data will be selected
        :Param(list) conditions: the conditions for records to be seleted
        """
        sql = "SELECT %s FROM %s WHERE %s ORDER BY %s LIMIT %d, %d" % (", ".join(fields),
            table, " ".join(conditions), order, page*number, number)
        return self.query(sql)

    def get_one(self, table, fields='*', conditions=['1',]):
        """Get one record from database according to given conditions, like:
        ['field1=value1', 'AND', 'field2>value2', 'OR', 'field3<>value3', ...]
        :Param(str) table: the name of target table
        :Param(list) fields: the name of columns whose data will be selected
        :Param(list) conditions: the conditions for records to be seleted
        """
        sql = "SELECT %s FROM %s WHERE %s" % (", ".join(fields), table, ' '.join(conditions))
        record = self.query(sql)
        return record[0] if record else {}

    def get(self, table, fields='*', conditions=['1',]):
        """Get records from database according to given conditions, like:
        ['field1=value1', 'AND', 'field2>value2', 'OR', 'field3<>value3', ...]
        :Param(str) table: the name of target table
        :Param(list) fields: the name of columns whose data will be selected
        :Param(list) conditions: the conditions for records to be seleted
        """
        sql = "SELECT %s FROM %s WHERE %s" % (", ".join(fields), table, ' '.join(conditions))
        return self.query(sql)

    def insert(self, table, data):
        """Add data into database.
        Param(str) table: the name of target table
        Param(dict) data: data in dict, like {field: value, ...}
        """
        fields = []
        values = []
        for key, value in data.items():
            if isinstance(value, unicode) or isinstance(value, str):
                values.append(("'%s'" % value))
            else:
                values.append(("%r" % value))
            fields.append(key)
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, ",".join(fields), ",".join(values))
        return self.execute(sql).lastrowid

    def delete(self, table, conditions=['1', ]):
        """Delete records in database accoridng to given conditions, like:
        ['field1=value1', 'AND', 'field2>value2', 'OR', 'field3<>value3', ...]
        :Param(str) table: the name of target table
        :Param(list) conditions: the conditions for records to be deleted
        """
        sql = "DELETE FROM %s WHERE %s" % (table, ' '.join(conditions))
        return self.execute(sql).rowcount

    def update(self, table, data, conditions=["1", ]):
        """Modify the value of existing record specified by conditions, like:
        ["field1=value1", "AND", "field2>value2", "OR", "field3<>value3", ...]
        :Param(str) table: the name of target table
        :Param(dict) data: new data
        :Param(list) conditions: the conditions for records to be modified
        """
        values = []
        for key, value in data.items():
            if isinstance(value, unicode) or isinstance(value, str):
                values.append(("%s='%s'" % (key, value)))
            else:
                values.append(("%s=%r" % (key, value)))
        sql = "UPDATE %s SET %s WHERE %s" % (table, ", ".join(values), " ".join(conditions))
        return self.execute(sql).rowcount

    def clear_table(self, table):
        """Delete all records in a table.
        :Param(str) table: the name of target table
        """
        self.execute('TRUNCATE %s' % table)