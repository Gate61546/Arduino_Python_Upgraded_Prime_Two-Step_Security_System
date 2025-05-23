import serial
import time
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import face_cascade
import os

ser = serial.Serial('COM3',9600,timeout=1)
time.sleep(2)



def main_function():
    print("correct password")


    
text=[]

while True:
    line = ser.readline().decode("utf-8")
    if line =="":
        pass
    else:
        try:
            text.append(int(line))
            print(text)
        except:
            if (line[0])== 'A':
                if text == []:
                    pass
                else:
                    text.pop()
                    print(text)

            if (line[0])== 'B':
                if text == []:
                    pass
                else:
                    if text==[3,1,2]:
                        print("correct passsword")
                    else:
                        print("incorrect password")

            elif (line[0]) == 'C':

                video = cv2.VideoCapture(0) 
                
  # Loading pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Loading Keras face recognition model
    model = load_model('keras_model.h5')

    # Loading image
    img = cv2.imread('One.jpg')

    # Converting image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecting faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Iterating over the detected faces
    for (x, y, w, h) in faces:
    # Extract the face ROI (Region of Interest)
        face_roi = gray[y:y+h, x:x+w]

    # Resizing face ROI to the input size of the model
    resized_face = cv2.resize(face_roi, (model.input_shape[1], model.input_shape[2]))

    # Normalizing pixel values
    normalized_face = resized_face / 255.0

    # Expanding dimensions of the image to match the model's input shape
    reshaped_face = np.expand_dims(normalized_face, axis=0)
    reshaped_face = np.expand_dims(reshaped_face, axis=-1)

    # Making prediction using the Keras model
    prediction = model.predict(reshaped_face)

    # Getting the predicted class
    predicted_class = np.argmax(prediction)

    # Drawing a rectangle around the face and display the predicted class
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(img, str(predicted_class), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the output image
    cv2.imshow('Face Recognition', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
