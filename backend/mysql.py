import pymysql
from prettytable import PrettyTable

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="****",
  password="*********",
  read_timeout=timeout,
  port=15441,
  user="*****",
  write_timeout=timeout,
)
  
try:
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM todos")
  results = cursor.fetchall()
  table = PrettyTable()
  if results:
    table.field_names = results[0].keys()
  for row in results:
    table.add_row(row.values())
  print(table)
finally:
  connection.close()