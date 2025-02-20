import telebot
from gtts import gTTS
import os
import socket
import subprocess
import oneM2Mget
import time
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Read token from .env
print(BOT_TOKEN)
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in the .env file.")
bot = telebot.TeleBot(BOT_TOKEN)

# Function to send the IP and Wi-Fi info at startup
def send_ip_at_startup():
    ip_address = get_ip_address()
    wifi_status = check_wifi_connection()
    startup_message = f"Startup Info:\nIP Address: {ip_address}\nWiFi Status: {wifi_status}"
    bot.send_message(chat_id='1137118390', text=startup_message)

# Function to convert text to speech and play it
def text_to_speech(text, language='en', filename='output.mp3', play=True):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)
    if play:
        os.system(f"mpg321 {filename}")

# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Use /play to play predefined text or /playcustom : your text to play.")

# Define a function to handle the /play command (predefined text)
@bot.message_handler(commands=['play'])
def play_audio(message):
    response_data = oneM2Mget.getTemperature()
    con_value = response_data
    predefined_text = f"Welcome to Smart City Living Lab. The current value of CO2 is {con_value[1]}, temperature is {con_value[2]}, and humidity is {con_value[3]}."
    bot.reply_to(message, "Playing predefined text.")
    text_to_speech(predefined_text)

# Define a function to handle the /playcustom command (custom text)
@bot.message_handler(commands=['playcustom'])
def play_custom_audio(message):
    if ':' in message.text:
        custom_text = message.text.split(":", 1)[1].strip()
        if custom_text:
            bot.reply_to(message, f"Playing custom text: {custom_text}")
            text_to_speech(custom_text)
        else:
            bot.reply_to(message, "No custom text provided after /playcustom.")
    else:
        bot.reply_to(message, "Please provide custom text using /playcustom:your text")

# Function to get the IP address
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "Unable to get IP address: {}".format(str(e))

# Function to check Wi-Fi connection status
def check_wifi_connection():
    try:
        result = subprocess.run(['iwgetid'], stdout=subprocess.PIPE)
        wifi_info = result.stdout.decode('utf-8')
        if wifi_info:
            return "Connected to WiFi network: {}".format(wifi_info.strip())
        else:
            return "Not connected to any WiFi network"
    except Exception as e:
        return "Unable to determine WiFi connection status: {}".format(str(e))

# Define a function to handle the /ip command
@bot.message_handler(commands=['ip'])
def send_ip_info(message):
    ip_address = get_ip_address()
    wifi_status = check_wifi_connection()
    bot.reply_to(message, f"IP Address: {ip_address}\nWiFi Status: {wifi_status}")

# Function to activate virtual environment and run a Python file
def run_python_file(message, python_file):
    try:
        # Activate virtual environment and run the file
        command = f"source /home/pacling/Documents/lamp/myenv/bin/activate && python {python_file}"
        subprocess.run(command, shell=True, check=True)
        bot.reply_to(message, f"Running {python_file} with virtual environment activated.")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Failed to run {python_file}: {str(e)}")

# Functions to stop, start, and restart a service
def manage_service(message, service_name, action):
    try:
        subprocess.run(["sudo", "systemctl", action, service_name], check=True)
        bot.reply_to(message, f"Service '{service_name}' {action}ed successfully.")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Failed to {action} service '{service_name}': {str(e)}")

# Bot commands for managing services and running Python files
@bot.message_handler(commands=['start_service'])
def start_service(message):
    service_name = "camera.service"  # Replace with actual service name
    manage_service(message, service_name, "start")

@bot.message_handler(commands=['stop_service'])
def stop_service(message):
    service_name = "camera.service"  # Replace with actual service name
    manage_service(message, service_name, "stop")

@bot.message_handler(commands=['restart_service'])
def restart_service(message):
    service_name = "camera.service"  # Replace with actual service name
    manage_service(message, service_name, "restart")

@bot.message_handler(commands=['run_python'])
def run_python(message):
    python_file = "/home/pacling/Documents/lamp/main/update_main1.py"  # Replace with actual script path
    run_python_file(message, python_file)

@bot.message_handler(commands=['reboot'])
def reboot_rpi(message):
    bot.reply_to(message, "Rebooting...")
    os.system("sudo reboot")

@bot.message_handler(func=lambda message: True)
def handle_data(message):
    data = message.text
    bot.reply_to(message, f"Received data: {data}")

# Send the IP at startup and start the bot with automatic retry
def start_bot():
    send_ip_at_startup()  # Send IP when the script starts
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print("Error occurred:", str(e))
            time.sleep(5)

# Start the bot
if __name__ == "__main__":
    start_bot()
