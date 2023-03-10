import streamlit as st
import mysql.connector
import cv2
import numpy as np


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
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)   # getting the gray-scale image
    # appying the fucntion here

    st.image(img)
  except:
    continue 
  

  