# Install Flask on your system by writing
#!pip install Flask
#Import all the required libraries
#Importing Flask
#render_template--> To render any html file, template
import flask
from flask import Flask, Response, request, render_template, jsonify
# Required to run the YOLOv8 model
import cv2
import math
import time
# YOLO_Video is the python file which contains the code for our object detection model
#Video Detection is the Function which performs Object Detection on Input Video
from VIDEO import video_detection
app = Flask(__name__)

app.config['SECRET_KEY'] = 'HYPERLOOP'
#Generate_frames function takes path of input video file and  gives us the output with bounding boxes
# around detected objects

# Define global variables
detect_time = time.localtime()
objects_detected = 0
dangerous_detected = 0
confidence = 0
list_confidence = []
list_objects = []
list_time = []

#Now we will display the output video with detection
def generate_frames(path_x = ''):
    global detect_time
    global objects_detected
    global dangerous_detected
    global confidence
    global list_confidence
    global list_objects
    global list_time
    # yolo_output variable stores the output for each detection
    # the output with bounding box around detected objects

    yolo_output = video_detection(path_x)
    for detection_, num_classes, num_danger, list_classes, list_conf in yolo_output:
        objects_detected = num_classes
        dangerous_detected = num_danger
        num_elements = len(list_classes)
        confidence = 0
        list_confidence = []
        list_objects = []
        list_time = []
        if num_classes != 0:
            detect_time = time.localtime()

        actual_time = detection_time()
        for i in range(num_elements):
            list_objects.append(list_classes[i])
            list_confidence.append(list_conf[i])
            list_time.append(actual_time)
            print(list_time[i])
            if list_conf[i] > confidence:
                confidence = list_conf[i]

        ref,buffer=cv2.imencode('.jpg',detection_)
        # Any Flask application requires the encoded image to be converted into bytes
        #We will display the individual frames using Yield keyword,
        #we will loop over all individual frames and display them as video
        #When we want the individual frames to be replaced by the subsequent frames the Content-Type, or Mini-Type
        #will be used
        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

def detection_time():
    global detect_time
    hour = detect_time.tm_hour
    minute = detect_time.tm_min
    second = detect_time.tm_sec

    if hour < 10:
        if minute < 10:
            if second < 10:
                time_string = f"0{hour}:0{minute}:0{second}"
            else:
                time_string = f"0{hour}:0{minute}:{second}"
        else:
            if second < 10:
                time_string = f"0{hour}:{minute}:0{second}"
            else:
                time_string = f"0{hour}:{minute}:{second}"
    else:
        if minute < 10:
            if second < 10:
                time_string = f"{hour}:0{minute}:0{second}"
            else:
                time_string = f"{hour}:0{minute}:{second}"
        else:
            if second < 10:
                time_string = f"{hour}:{minute}:0{second}"
            else:
                time_string = f"{hour}:{minute}:{second}"

    return time_string

@app.route('/video')
def video():
    return Response(generate_frames(path_x='static/files/Videos/bike.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(generate_frames(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam')
def webcam():
    return Response(generate_frames(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    global real_time
    return render_template('indextry1.html', image_url='/webcam', array=list_objects)


@app.route('/video_feed')
def video_feed():
    return Response(video_detection(path_x='static/files/Videos/bike.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/num_objects')
def num_objects():
    global objects_detected
    number = str(objects_detected)
    return number

@app.route('/num_danger_objects')
def num_danger_objects():
    global dangerous_detected
    number = str(dangerous_detected)
    return number

@app.route('/get_confidence')
def get_confidence():
    global confidence
    number = str(confidence)
    return number

@app.route('/get_object_names')
def get_object_names():
    global list_objects
    return jsonify(list_objects)

@app.route('/get_object_conf')
def get_object_conf():
    global list_confidence
    return jsonify(list_confidence)

@app.route('/get_time')
def get_time():
    global list_time
    return jsonify(list_time)

if __name__ == "__main__":
    app.run(debug=True)
