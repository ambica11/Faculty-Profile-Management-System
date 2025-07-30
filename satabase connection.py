import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootcode",
  database="project"
)

mycursor = mydb.cursor()

sql = "INSERT INTO sample (name, class) VALUES (%s, %s)"
val = ("John", "Highway 21")

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
