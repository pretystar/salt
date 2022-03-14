#pip install mysql-connector-python
#-- 创建用户
#CREATE USER 'username'@'%' IDENTIFIED BY 'password';

#-- 授权使用数据库
#GRANT ALL ON *.* TO 'username'@'%';
import mysql.connector

mydb = mysql.connector.connect(  host="mysql-db",  user="root", db='salt', password="root")

print(mydb)

mycursor = mydb.cursor()
mycursor.execute("use salt;")
mycursor.execute("SHOW SCHEMAS;");
mycursor.execute("SELECT * FROM jids")
mycursor.execute("SELECT * FROM salt_returns")
#mycursor.execute("SHOW DATABASES;")


myresult = mycursor.fetchall()

for x in myresult:
  print(x)