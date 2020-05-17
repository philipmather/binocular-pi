#python
"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import cv2#,imutils
import threading,queue,time
import numpy as np
import traceback
#import os,argparse
#import pickle

def run():
  try:
    left_camera_source = 0
    right_camera_source = 2
    pixel_width = 640 #1280 #320 #640
    pixel_height = 480 #720 #240 #480
#    angle_width = 78
#    angle_height = 64 # 63
    frame_rate = 20
#   camera_separation = 5 + 15/16

    # left camera 1
    ct1 = Camera_Thread()
    ct1.name = "Left"
    ct1.camera_source = left_camera_source
    ct1.camera_width = pixel_width
    ct1.camera_height = pixel_height
    ct1.camera_frame_rate = frame_rate

    # right camera 2
    ct2 = Camera_Thread()
    ct2.name = "Right"
    ct2.camera_source = right_camera_source
    ct2.camera_width = pixel_width
    ct2.camera_height = pixel_height
    ct2.camera_frame_rate = frame_rate

    # camera coding
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"YUYV")
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"YUYV")
    ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"XVID")
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"XVID")
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

    # start cameras
    ct1.start()
    ct2.start()

    # ------------------------------
    # stabilize 
    # ------------------------------

    # pause to stabilize
    time.sleep(0.25)

    X,Y,Z,D = 0,0,0,0
    blank = np.zeros(shape=(pixel_height,pixel_width,3)).astype('uint8')

    cv2.imshow(ct1.name,blank)
    cv2.imshow(ct2.name,blank)
    cv2.moveWindow(ct1.name,0,500)
    cv2.moveWindow(ct2.name,0+pixel_width,500)

    while True:
      # get frames
      frame1 = ct1.next()
      frame2 = ct2.next()

      # display coordinate data
      fps1 = int(ct1.current_frame_rate)
      fps2 = int(ct2.current_frame_rate)

      text = 'X: {:3.1f} Y: {:3.1f} Z: {:3.1f} D: {:3.1f} FPS: {}/{}'.format(X,Y,Z,D,fps1,fps2)
#      print(text)
#      lineloc = 0
#      lineheight = 30
#      for t in text.split('\n'):
#        lineloc += lineheight
#        cv2.putText(frame1,
#                    t,
#                    (10,lineloc), # location
#                    cv2.FONT_HERSHEY_PLAIN, # font
#                    #cv2.FONT_HERSHEY_SIMPLEX, # font
#                    1.5, # size
#                    (0,255,0), # color
#                    1, # line width
#                    cv2.LINE_AA, #
#                    False) #

      # display frame
#      print('Displaying frames')
      cv2.imshow("Left",frame1)
      cv2.imshow("Right",frame2)

      # detect keys
      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        break
#      elif key != 255:
#        print('KEY PRESS:',[chr(key)])

  except:
    print("Failed during main execution")
    print(traceback.format_exc())

  # close camera1
  try:
    ct1.stop()
  except:
    print("Failed to stop ct1")
    pass

  # close camera2
  try:
    ct2.stop()
    print("Failed to stop ct2")
  except:
    pass

  # kill frames
  cv2.destroyAllWindows()

  print('DONE')

# ------------------------------
# Camera Tread
# ------------------------------

class Camera_Thread:

  # ------------------------------
  # System Variables
  # ------------------------------

  # camera
  camera = None
  camera_init = 0.1

  # buffer
  buffer = None

  # control states
  frame_grab_run = False
  frame_grab_on = False

  # counts and amounts
  current_frame_rate = 0
  loop_start_time = 0

  # ------------------------------
  # Functions
  # ------------------------------
  def start(self):
    # buffer
    self.buffer = queue.Queue(1)

    # camera setup
    self.camera = cv2.VideoCapture(self.camera_source)
    self.camera.set(3,self.camera_width)
    self.camera.set(4,self.camera_height)
    self.camera.set(5,self.camera_frame_rate)
    self.camera.set(6,self.camera_fourcc)
    time.sleep(self.camera_init)

    # camera image vars
    self.camera_width  = int(self.camera.get(3))
    self.camera_height = int(self.camera.get(4))
    self.camera_frame_rate = int(self.camera.get(5))
    self.camera_mode = int(self.camera.get(6))
    self.camera_area = self.camera_width*self.camera_height

    # black frame (filler)
    self.black_frame = np.zeros((self.camera_height,self.camera_width,3),np.uint8)

    # set run state
    self.frame_grab_run = True

    # start thread
    self.thread = threading.Thread(target=self.loop)
#    print('Starting camera source:',self.camera_source)
    self.thread.start()

  def stop(self):
    # set loop kill state
    self.frame_grab_run = False
      
    # let loop stop
    while self.frame_grab_on:
      time.sleep(0.1)

    # stop camera if not already stopped
    if self.camera:
      try:
        self.camera.release()
      except:
        pass
    self.camera = None

    # drop buffer
    self.buffer = None

  def loop(self):
    # load start frame
    self.buffer.put(self.black_frame,False)

    # status
    self.frame_grab_on = True
    self.loop_start_time = time.time()

    # frame rate
    fc = 0
    t1 = time.time()

    # loop
    while 1:

      # external shut down
      if not self.frame_grab_run:
        break

      grabbed,frame = self.camera.read()
      if not grabbed:
        break

      # open a spot in the buffer
      if self.buffer.full():
        self.buffer.get()

      self.buffer.put(frame,False)
      fc += 1

      # update frame read rate
      if fc >= 10:
        self.current_frame_rate = round(fc/(time.time()-t1),2)
        fc = 0
        t1 = time.time()

    # shut down
    self.loop_start_time = 0
    self.frame_grab_on = False
    self.stop()

  def next(self):
    # get from buffer (fail if empty)
    try:
      frame = self.buffer.get(timeout=1)
    except queue.Empty:
      frame = self.black_frame
      print('Queue Empty!')
      #print(traceback.format_exc())
      pass

    # done
    return frame

if __name__ == '__main__':
  run()
