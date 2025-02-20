import json
import threading
import time
from tkinter import *
from PIL import ImageTk, Image
import datetime
from getdata import fetch_and_process_data

urls = [
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SR/SR-AQ/SR-AQ-KH95-00/Data/la",
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WD/WM-WD-KH95-00/Data/la",
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN02-00/Data/la",
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WF/WM-WF-KB04-70/Data/la",
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-AQ/AQ-SN00-00/Data/la",
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WN/WN-L001-03/Data/la",
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN95-00/Data/la",
]

# Define the index mapping for each URL
index_mapping = {
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SR/SR-AQ/SR-AQ-KH95-00/Data/la": [1, 2, 3],
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WD/WM-WD-KH95-00/Data/la": [4],
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN02-00/Data/la": [1],
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WF/WM-WF-KB04-70/Data/la": [2],
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-AQ/AQ-SN00-00/Data/la": [11],
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WN/WN-L001-03/Data/la": [2, 4],
    "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN95-00/Data/la": [1],
}

def update_json_file():
    while True:
        result = fetch_and_process_data(urls, index_mapping)
        with open('result.json', 'w') as json_file:
            json.dump(result, json_file)
        time.sleep(10)

# Start the background thread
thread = threading.Thread(target=update_json_file)
thread.daemon = True
thread.start()

# Create the root window
root = Tk()
root.title("Sensor Data")
root.configure(background='#0A0A0A')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

frame = Frame(root, bg='#0A0A0A')
frame.pack(pady=10)

# Create labels for time and day
time_label = Label(frame, text="Time: ", font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white')
time_label.pack(side=LEFT, anchor=NW, pady=(10, 5), padx=(30, 50))

day_label = Label(frame, text="Day: ", font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white')
day_label.pack(side=RIGHT, anchor=NW, pady=(10, 5), padx=(50, 30))

# Create a frame to contain the images
frame = Frame(root, bg='#0A0A0A')
frame.pack(pady=10) 

# Load and resize the first image
image1 = Image.open(r"image/smartCity_livingLab.png").resize((120, 80))
photo1 = ImageTk.PhotoImage(image1)

# Load and resize the second image
image2 = Image.open(r"image/iiith_icon1.png").resize((120, 80))
photo2 = ImageTk.PhotoImage(image2)

# Create labels to display the images horizontally inside the frame
label1 = Label(frame, image=photo2, bg='#0A0A0A')
label1.image = photo1
label1.pack(side=LEFT, padx=(0, 20))  # Add padding on the right side of the first image

label2 = Label(frame, image=photo1, bg='#0A0A0A')
label2.image = photo2
label2.pack(side=LEFT, padx=(20, 0))  # Add padding on the left side of the second image

# Create a canvas for drawing the line below the frame
canvas_frame_line = Canvas(root, width=400, height=2, bg='#0A0A0A', highlightthickness=0)
canvas_frame_line.create_line(0, 0, 500, 0, fill="white", width=2)
canvas_frame_line.pack(pady=(5, 0))  # Adjust the padding to position the line below the frame

# Add a label for the text "Smart city dashboard"
label_text = Label(root, text="Smart City Dashboard", font=('Arial', 17, 'bold'), bg='#0A0A0A', fg='white')
label_text.pack(pady=(5, 0))  # Adjust the padding to position the label below the line

# Create a canvas for drawing the line below the text
canvas_text_line = Canvas(root, width=400, height=2, bg='#0A0A0A', highlightthickness=0)
canvas_text_line.create_line(0, 0, 500, 0, fill="white", width=2)
canvas_text_line.pack(pady=(5, 0))  # Adjust the padding to position the line below the text

image_frame = Frame(root, bg='#0A0A0A')
image_frame.pack(pady=10)

# Load and resize the image
image_path = r"image/nodes.png"  # Replace "path_to_your_image.jpg" with the actual path to your image
image = Image.open(image_path)
image = image.resize((400, 250))  # Adjust the size as needed
image = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = Label(image_frame, image=image, bg='#0A0A0A')
image_label.image = image  # Keep a reference to the image to prevent garbage collection
image_label.pack()

# Create a canvas for drawing the line below the text
canvas_text_line = Canvas(root, width=400, height=2, bg='#0A0A0A', highlightthickness=0)
canvas_text_line.create_line(0, 0, 500, 0, fill="white", width=2)
canvas_text_line.pack(pady=(2, 0))  # Adjust the padding to position the line below the text

label_text = Label(root, text="Lab Stats", font=('Arial', 10, 'bold'), bg='#0A0A0A', fg='white')
label_text.pack(pady=(2, 0))
# Create a canvas for drawing the line below the frame
canvas_frame_line = Canvas(root, width=400, height=2, bg='#0A0A0A', highlightthickness=0)
canvas_frame_line.create_line(0, 0, 500, 0, fill="white", width=2)
canvas_frame_line.pack(pady=(2, 0))  # Adjust the padding to position the line below the frame

# Create a frame for the sensor data columns
sensor_frame = Frame(root, bg='#0A0A0A')
sensor_frame.pack(pady=15)  # Increase the distance between the two columns

# Left column for sensor data
left_column = Frame(sensor_frame, bg='#0A0A0A')
left_column.pack(side=LEFT, padx=(10, 40))  # Increase the padding for the left column

# Right column for sensor data
right_column = Frame(sensor_frame, bg='#0A0A0A')
right_column.pack(side=RIGHT, padx=(40, 10))  # Increase the padding for the right column

# Load and resize the temperature icon
temp_icon = Image.open(r"image/temp_icon1.png").resize((30, 30))
temp_icon = ImageTk.PhotoImage(temp_icon)

# Add labels for sensor data
temp_label = Label(left_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=temp_icon)
temp_label.pack(anchor=W, pady=2)

rh_icon = Image.open(r"image/rh_icon.png").resize((30, 30))
rh_icon = ImageTk.PhotoImage(rh_icon)

rh_label = Label(left_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=rh_icon)
rh_label.pack(anchor=W, pady=2)

aqi_icon = Image.open(r"image/aqi_icon.png").resize((30, 30))
aqi_icon = ImageTk.PhotoImage(aqi_icon)

aqi_label = Label(left_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=aqi_icon)
aqi_label.pack(anchor=W, pady=2)

ss_icon = Image.open(r"image/ss_icon.png").resize((30, 30))
ss_icon = ImageTk.PhotoImage(ss_icon)

signal_label = Label(left_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=ss_icon)
signal_label.pack(anchor=W, pady=2)

co2_icon = Image.open(r"image/co2_icon2.png").resize((30, 30))
co2_icon = ImageTk.PhotoImage(co2_icon)

co2_label = Label(right_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=co2_icon)
co2_label.pack(anchor=W, pady=2)

sl_icon = Image.open(r"image/sl_icon2.png").resize((30, 30))
sl_icon = ImageTk.PhotoImage(sl_icon)

energy_label = Label(right_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=sl_icon)
energy_label.pack(anchor=W, pady=2)

wf_icon = Image.open(r"image/wf_icon.png").resize((30, 30))
wf_icon = ImageTk.PhotoImage(wf_icon)

water_flow_label = Label(right_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=wf_icon)
water_flow_label.pack(anchor=W, pady=2)

wq_icon = Image.open(r"image/wq_icon.png").resize((30, 30))
wq_icon = ImageTk.PhotoImage(wq_icon)

tds_label = Label(right_column, font=('Arial', 13, 'bold'), bg='#0A0A0A', fg='white', compound=LEFT, image=wq_icon)
tds_label.pack(anchor=W, pady=2)

# Create a canvas for drawing the line below the text
canvas_text_line = Canvas(root, width=400, height=2, bg='#0A0A0A', highlightthickness=0)
canvas_text_line.create_line(0, 0, 500, 0, fill="white", width=2)
canvas_text_line.pack(pady=(1, 0))  # Adjust the padding to position the line below the text

label_text = Label(root, text="ESG Stats", font=('Arial', 10, 'bold'), bg='#0A0A0A', fg='white')
label_text.pack(pady=(2, 0))
# Create a canvas for drawing the line below the frame
canvas_frame_line = Canvas(root, width=400, height=2, bg='#0A0A0A', highlightthickness=0)
canvas_frame_line.create_line(0, 0, 500, 0, fill="white", width=2)
canvas_frame_line.pack(pady=(1, 0))  # Adjust the padding to position the line below the frame

# Create the main frame with a smaller width and height
esg_frame = Frame(root, bg='#0A0A0A', width=300, height=200)
esg_frame.pack(pady=15)  # Increase the distance between the two columns
# Left column for sensor data
esg_left_column = Frame(esg_frame, bg='#0A0A0A')
esg_left_column.pack(side=LEFT, padx=(10, 10))  # Increase the padding for the left column
# Right column for sensor data
esg_right_column = Frame(esg_frame, bg='#0A0A0A')
esg_right_column.pack(side=RIGHT, padx=(10, 10))
# Middle column for sensor data
esg_mid_column = Frame(esg_frame, bg='#0A0A0A')
esg_mid_column.pack(expand=True, fill=BOTH)  # Expand to fill the remaining space
# Add labels for sensor data
esg_co2_label = Label(esg_left_column, font=('Arial', 20, 'bold'), bg='#0A0A0A', fg='white')
esg_co2_label.pack(anchor=W, pady=2)
esg_carbon_label = Label(esg_right_column, font=('Arial', 20, 'bold'), bg='#0A0A0A', fg='white')
esg_carbon_label.pack(anchor=W, pady=2)
canvas_text_line = Canvas(root, width=400, height=2, bg='#0A0A0A', highlightthickness=0)
canvas_text_line.create_line(0, 0, 500, 0, fill="white", width=2)
canvas_text_line.pack(pady=(1, 0))  # Adjust the padding to position the line below the text

def update_gui():
    with open('result.json', 'r') as json_file:
        result = json.load(json_file)
    time_label.config(text="Time: " + datetime.datetime.now().strftime("%H:%M"))
    day_label.config(text="Day: " + datetime.datetime.now().strftime("%A"))
    temp_label.config(text="" + f" {result['Temperature']} \xb0C")
    rh_label.config(text="" + f" {result['Humidity']} %")
    aqi_label.config(text="" + f" {result['AQI']}")
    energy_label.config(text="" + f"{result['Energy']} Kwh")
    water_flow_label.config(text="" + f" {result['Water Flow']} L/min")
    tds_label.config(text="" + f" {result['Water Quality']:.2f} ppm")
    co2_label.config(text="" + f" {result['CO2']} ppm")
    signal_label.config(text="" + f" {-12} dBm")
    esg_co2_label.config(text=f"{(result['ESG']+(130*2*0.1)*0.9):.2f} Kg")
    esg_carbon_label.config(text=f"{((result['ESG'] + (130 * 2 * 0.1) * 0.9) / 1000):.2f} ton")
    root.attributes('-fullscreen', True)
    root.after(10000, update_gui)  # Schedule the function to run every 10 seconds

# Start updating the GUI
root.attributes('-fullscreen', True)
update_gui()
root.attributes('-fullscreen', True)
root.mainloop()
