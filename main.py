import streamlit as st
import mysql.connector
import cv2.cv2 as cv
import numpy as np
from factory import *


    

data_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt2.xml")

my_db  = mysql.connector.connect(
          host="sql.freedb.tech",
          user="freedb_images",
          password="gEzze6ZHjU#M4e2",
          database="freedb_image_data"
    )
mycursor = my_db.cursor()

mycursor.execute("SELECT * FROM images")

myresult = mycursor.fetchall()
final_list = []
for x in myresult:
  final_list.append(x)


for i in range(len(final_list)):
  
  image_data = final_list[i][2]
  nparr = np.frombuffer(image_data, np.uint8)
  try:
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)   # getting the gray-scale image
    # appying the fucntion here
    final_function_and_save(data_cascade,img)  # emotion detection and saving refined data in database
  
  except:
    continue 


# delete all the images after data has been refined


mycursor = my_db.cursor()
sql = "TRUNCATE TABLE images"
mycursor.execute(sql)
my_db.commit()
mycursor.close()



checkbox = st.checkbox("show dataframe")

if checkbox:
  mycursor = my_db.cursor()
  sql = "SELECT * FROM emotions"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  df = pd.DataFrame(result, columns=[ 'time', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
  st.write(df)
  