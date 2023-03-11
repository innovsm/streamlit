import tensorflow as tf  
import cv2.cv2 as cv
from deepface import DeepFace
import mysql.connector
import pandas as pd
from datetime import datetime

def final_function(model_face,frame):
    frame_gray  = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces =  model_face.detectMultiScale(frame_gray)
    final_value = []
    for face in faces:
        x,y,w,h = face
        try:
            emotion_data = DeepFace.analyze(frame[y:y+h,x:x+w],actions=['emotion'])
            #print(emotion_data)
            final_value.append(emotion_data[0]['dominant_emotion'])
        except:
            continue
    emotion_list = ['angry', 'disgust','fear', 'happy', 'sad','surprise','neutral']
    emotion_count = []
    for i in emotion_list:
        count = final_value.count(i)
        emotion_count.append(count)
    return emotion_count



# Define function to establish connection to MySQL database

def connect_to_database():
    try:
        # Establish connection to MySQL database
        my_db = mysql.connector.connect(
            host="sql.freedb.tech",
            user="freedb_images",
            password="gEzze6ZHjU#M4e2",
            database="freedb_image_data"
        )
        return my_db
    except:
        print("Error connecting to MySQL database ")
        return None

# Define function to analyze image and save emotion data to MySQL table
def final_function_and_save(model_face, frame):
    # Connect to MySQL database
    my_db = connect_to_database()

    # Return None if database connection failed
    if not my_db:
        return None

    # Create cursor object
    mycursor = my_db.cursor()

    # Analyze image and get emotion counts
    emotion_count = final_function(model_face, frame)

    # Convert emotion count list to a string for SQL insertion
    emotion_str = ','.join(str(x) for x in emotion_count)

    try:
        # Get current date and time
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert emotion data into MySQL table
        sql = "INSERT INTO emotions (time, angry, disgust, fear, happy, sad, surprise, neutral) VALUES ('{}', {})".format(now, emotion_str)
        mycursor.execute(sql)
        my_db.commit()

        # Return emotion count list for further processing if needed
        return emotion_count

    except:

        # Reconnect to MySQL database and retry INSERT statement
        my_db = connect_to_database()

        # Return None if database reconnection failed
        if not my_db:
            return None

        mycursor = my_db.cursor()
        mycursor.execute(sql)
        my_db.commit()

        # Return emotion count list for further processing if needed
        return emotion_count



#--------------------------------------------------

def destroy_table():
    my_db = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_images",
        password="gEzze6ZHjU#M4e2",
        database="freedb_image_data"
        )

    mycursor = my_db.cursor()
    sql = "TRUNCATE TABLE images"
    my_db.commit()
    mycursor.execute(sql)
    mycursor.close()
    return True
    