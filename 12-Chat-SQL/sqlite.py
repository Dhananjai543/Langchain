import sqlite3

# connect to the database
connection = sqlite3.connect('student.db')

# create a cursor object to insert records and create table
cursor = connection.cursor()

# create a table
table_info= """
create table if not exists STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(10),
    SECTION VARCHAR(5),
    MARKS INT
    
)
"""

cursor.execute(table_info)


# insert records
cursor.execute("insert into STUDENT values('John', '10th', 'A', 85)")
cursor.execute("insert into STUDENT values('Alice', '10th', 'B', 90)")
cursor.execute("insert into STUDENT values('Bob', '9th', 'A', 78)")
cursor.execute("insert into STUDENT values('Eve', '9th', 'B', 88)")
cursor.execute("insert into STUDENT values('Charlie', '10th', 'A', 92)")


# dislay all records
print("All Records:")
data=cursor.execute("select * from STUDENT")
for row in data:
    print(row)


# commit the changes
connection.commit()
connection.close()


