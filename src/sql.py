#-*- coding:utf-8 -*-
import sqlite3 as sql
import os.path
from morphs import *



#confirm existence
def isfile(directory):
  if not os.path.isfile(directory):
    print(directory, '위치에 파일이 없습니다.')
    raise Exception

def create_table(directory, table):
  isfile(directory)
  try:
    conn = sql.connect(directory)
    cur = conn.cursor()
    cur.execute(f'''CREATE TABLE {table}(
                n integer primary key autoincrement,
                x text,
                y text,
                left text,
                right text,
                UNIQUE (x,y));''')
    conn.close()
    print(f'{table}이 생성되었습니다.')
  except Exception as e:
      return e

def insert_data(directory, x, y, left, right):
  'insert data to directory'

  isfile(directory)
  if not len(x)==len(y):
    print("x, y배열의 길이가 같아야 합니다.")
    raise Exception
  
  conn = sql.connect(directory)
  cur = conn.cursor()
  cur.execute('begin;')
  for i in range(len(x)):
    for j in range(len(x[i])):
      try:
        cur.execute(f'INSERT INTO Words(x, y, left, right) values("{x[i][j]}", "{y[i][j]}", "{left[i+j]}", "{right[i+j]}");')
      except Exception as e:
          pass
  cur.execute('commit;')
  conn.close()
  print('commit 완료.')
 

def set_data(text):
  tags = 'NVMJESX'
  morphs = Morphs()
  left = []
  right = []
  
  document = konlpy.utils.read_txt(text)
  morphs.pos(document)

  print('inserting data to db')
  for i in range(len(morphs.tags)):
      if len(morphs.tags[i]) < 4:
          continue
      for j in range(len(morphs.tags[i])):
          if j==0:
              left.append('')
              right.append(tags.find(morphs.tags[i][j+1]))
          elif j==(len(morphs.tags[i])-1):
              left.append(tags.find(morphs.tags[i][j-1]))
              right.append('')
          else:
              left.append(tags.find(morphs.tags[i][j-1]))
              right.append(tags.find(morphs.tags[i][j+1]))
              
  insert_data('dictionary', morphs.morphs, morphs.tags, left, right)


def get_data(directory, word):
    isfile(directory)
    try:
      conn = sql.connect(directory)
      cur = conn.cursor()
      cur.execute(f'SELECT n, y, left, right FROM Words WHERE x="{word}"')
      return cur.fetchone()
    except Exception as e:
      return e

def drop_data(directory, table):
  isfile(directory)
  try:
    conn = sql.connect(directory)
    cur = conn.cursor()
    cur.execute(f'DROP TABLE {table};')
    print(f'{table} Dropped')
  except Exception as e:
    return e

def show_data(directory, table):
  isfile(directory)
  try:
    conn = sql.connect(directory)
    cur = conn.cursor()
    cur.execute(f'SELECT * from {table};')
    return cur.fetchall()
  except Exception as e:
    return e
