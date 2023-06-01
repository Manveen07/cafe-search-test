from dotenv import load_dotenv
load_dotenv()
import os
import pymysql

connection = pymysql.connect(
  host= os.getenv("HOST"),
  user=os.getenv("USERNAME"),
  passwd= os.getenv("PASSWORD"),
  database= os.getenv("DATABASE"),
ssl={'ssl': {'ca': os.environ.get('MYSQL_ATTR_SSL_CA')}}
)
def to_dict(query):
  cursor = connection.cursor()
  cursor.execute(query)
  rows = cursor.fetchall()
  cursor.close()
  result = []
  columns = [column[0] for column in cursor.description]  # Get the column names
  for row in rows:
    row_dict = dict(zip(columns, row))
    result.append(row_dict)
  return result

def setup_partitioning():
  cursor = connection.cursor()

  # Enable partitioning on the cafes table
  cursor.execute('ALTER TABLE cafes PARTITION BY RANGE(id) (PARTITION p0 VALUES LESS THAN (100), PARTITION p1 VALUES LESS THAN (200))')

  # Create local indexes on the cafes table
  cursor.execute('CREATE INDEX idx_name ON cafes (name)')

  # Commit the changes
  connection.commit()
  cursor.close()

def load_cafes_from_db():
  query='SELECT * FROM cafes'
  return to_dict(query)
def load_cafe_from_db(id):
  query=f"select * from cafes where id = {id}"
  return to_dict(query)

def add_cafe_to_db(id, data):
  query = f"INSERT INTO cafes (id, name, map_url, img_url, location, has_sockets, has_toilet, can_take_calls, seats, coffee_price) " \
            f"VALUES ({id}, '{data['name']}', '{data['map_url']}', '{data['img_url']}', '{data['location']}', {data['has_sockets']}, " \
            f"{data['has_toilet']}, {data['can_take_calls']}, {data['seats']}, {data['coffee_price']})"
  cursor = connection.cursor()
  cursor.execute(query)

def add_review_for_cafe_to_db(id, data):
  query = f"INSERT INTO review (id, name, email, review, rating) VALUES ({id}, '{data['full_name']}', '{data['email']}', '{data['review']}', {data['rating']})"
  cursor = connection.cursor()
  cursor.execute(query)


cursor=connection.cursor()
# cursor.execute("SHOW INDEX FROM cafes")
# rows=cursor.fetchall()
# print(rows)
# cursor.execute('ALTER TABLE cafes DROP INDEX name')
# cursor.execute("SHOW INDEX FROM cafes")
# rows=cursor.fetchall()
# print(rows)




# setup_partitioning()
data={'email': 'shardyms@gmail.com', 'full_name': 'manveen singh', 'review': 'good food', 'rating': '9'}
add_review_for_cafe_to_db(id=2,data=data)