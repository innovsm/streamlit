import streamlit as st
import mysql.connector
import cv2
import numpy as np
from factory import *
from plotly import express as exp
import time
data_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
# ==========================   main.pyh ===========================
def job():
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
            final_function_and_save(data_cascade,img)  # emotion detection and saving refined data in database

        except:
            continue 

    # delete all the images after data has been refined
    mycursor = my_db.cursor()
    sql = "TRUNCATE TABLE images"
    mycursor.execute(sql)
    my_db.commit()
    mycursor.close()
    return myresult




# ===================================================================

st.set_page_config(page_title="Result",layout="centered")

data_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")


my_db  = mysql.connector.connect(
              host="sql.freedb.tech",
              user="freedb_images",
              password="gEzze6ZHjU#M4e2",
              database="freedb_image_data"
        )



# ------------------------  main_workflow -----------------------
with st.expander("About", expanded=False):
  st.write(alfa_string())

# adding the link
st.markdown("[click here for camera access](https://alternative-3znj.onrender.com/)", )
st.title("FocusMate")
st.write("the following graph will generate the emotional response of the students during the session")
checkbox = st.checkbox("Get Result")

if checkbox:
  mycursor = my_db.cursor()
  sql = "SELECT * FROM emotions"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  data_emotion = pd.DataFrame(result, columns=[ 'time', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
  
  data_emotion.index = pd.to_datetime(data_emotion['time'])

  data_emotion.drop(['time'], axis = 1 ,inplace = True)
  tab_1, tab_2,tab_3 = st.tabs(["line-chart", "pie-chart","dataframe-generated"])
  with tab_1:
    st.title("Real time access")
    st.write("real time emotional response of student during session")
    st.line_chart(data_emotion)
  with tab_2:
    st.title("Pie Chart")
    data_1 = data_emotion
    alfa = pd.DataFrame(data_1[['angry','disgust', 'fear', 'happy','sad','surprise', 'neutral']].sum())
    alfa['emotion'] = alfa.index
    colors = exp.colors.sequential.RdBu
    fig = exp.pie(alfa, values=0, names='emotion', title='Emotion Distribution', color_discrete_sequence=colors)
    st.plotly_chart(fig)
  with tab_3:
    st.title("Dataframe")
    st.subheader("main dataframe")
    st.write(data_emotion)
else:
   x = True
   while(x):
  
      alfa = job()
      if(len(alfa) == 0):
         x = False
      else:
         time.sleep(20)

      

    