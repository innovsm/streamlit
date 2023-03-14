import streamlit as st
import mysql.connector
import cv2
import numpy as np
from factory import *
from plotly import express as exp

st.set_page_config(page_title="Result",layout="centered")

data_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

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


# ------------------------  main_workflow -----------------------
with st.expander("About", expanded=False):
  st.write("""
  At Saffron.ai, we are dedicated to improving student 
  engagement and learning outcomes through the use of cutting-edge technology. Our facial expression
    recognition system provides real-time data on student attentiveness during class, allowing teachers to 
    adjust their teaching approach and create more personalized and effective learning experiences for their
      students. By integrating this data with other sources such as student feedback and curriculum data, we 
      provide a comprehensive understanding of student progress and needs.
Our goal is to help educators leverage the power of technology to create more engaging and effective learning environments, leading to improved outcomes for students and a more equitable and inclusive education system. We understand the importance of creating a supportive and positive learning environment, and our system has the potential to reduce stress levels among students while improving their academic performance and long-term success.

We are committed to implementing our system responsibly,
 addressing potential ethical concerns surrounding the use of facial recognition technology, such as 
 privacy and bias issues. We believe that by using technology in a responsible and ethical manner, we can 
 contribute to a more equitable and inclusive education system.
Join us in our mission to revolutionize education and empower students to reach their full potential.""")

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

  