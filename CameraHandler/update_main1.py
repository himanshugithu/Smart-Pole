import cv2
import time
import oneM2Mget 
from Speak import text_to_speech
# from getLUX import calculate_luminance
# from faceDistance import getDistance

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
KNOWN_FACE_WIDTH = 16.5  # Assume the average face width in centimeters (e.g., 16.5 cm)
FOCAL_LENGTH = 500.0  # Assume the focal length of the camera (e.g., 500 pixels)

def count_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces)

def calculate_distance(face_width_pixels):
    return (KNOWN_FACE_WIDTH * FOCAL_LENGTH) / face_width_pixels

def take_photo_and_count_faces():
    # Attempt to open the first camera (0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        # If the first camera fails, try the second camera (1)
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("Error: Failed to open both cameras.")
            return

    prev_num_faces = 0  # Previous number of faces
    speech_played = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        num_faces = count_faces(frame)
        print(f"Previous number of faces: {prev_num_faces}, Current number of faces: {num_faces}")

        if prev_num_faces != num_faces:
            for (x, y, w, h) in face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)):
                face_width_pixels = w
                distance = calculate_distance(face_width_pixels)
                print(f"Distance to face: {distance} cm")
                if distance is not None and distance < 200:   # Check if distance is valid (not None) and less than 40
                    if not speech_played:                    # Check if speech has already been played for this detection
                        try: 
                            #response_data = oneM2Mget.getTemperature()
                            #con_value = response_data
                            data = f"Welcome to Smart City Living Lab. We have deployed over three hundred sensor nodes all over the campus and we also have wi sun backbone network in place. The current value of CO2 is {43}, temperature is {35.98}, and humidity is {78.9}."
                            text_to_speech(data)
                            speech_played = True             # Set the flag to True to indicate that speech has been played
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        speech_played = False

        prev_num_faces = num_faces  # Update previous number of faces

        time.sleep(1)  # Wait for 3 seconds before capturing the next photo

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    take_photo_and_count_faces()
