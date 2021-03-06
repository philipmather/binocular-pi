#python
"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import cv2,imutils
import threading,queue,time
import numpy as np
import traceback
#import os,argparse
import pickle
from gpiozero import CPUTemperature

def run():
  try:
    left_camera_source = 0
    right_camera_source = 2
    pixel_width = 640 #1280 #320 #640
    pixel_height = 480 #720 #240 #480
#    angle_width = 78
#    angle_height = 64 # 63
    frame_rate = 30
#   camera_separation = 5 + 15/16

    # left camera 1
    ct1 = Camera_Thread()
    ct1.name = "Left"
    ct1.camera_source = left_camera_source
    ct1.camera_width = pixel_width
    ct1.camera_height = pixel_height
    ct1.camera_frame_rate = frame_rate
    leftFrame = None

    # right camera 2
    ct2 = Camera_Thread()
    ct2.name = "Right"
    ct2.camera_source = right_camera_source
    ct2.camera_width = pixel_width
    ct2.camera_height = pixel_height
    ct2.camera_frame_rate = frame_rate
    rightFrame = None

    # camera coding
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"YUYV")
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"YUYV")
    ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"XVID")
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"XVID")
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"BGR3")
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"BGR3")
    #ct1.camera_fourcc = cv2.VideoWriter_fourcc(*"YU12")
    #ct2.camera_fourcc = cv2.VideoWriter_fourcc(*"YU12")

    # start cameras
    ct1.start()
    ct2.start()

    # ------------------------------
    # stabilize 
    # ------------------------------

    # pause to stabilize
    time.sleep(0.01)
    main_loop_count = 0
    main_loop_rate = 0
    t1 = time.time()

    X,Y,Z,D = 0,0,0,0
    blank = np.zeros(shape=(pixel_height,pixel_width,3)).astype('uint8')
    disparity = "Disparity"

    cv2.imshow(ct1.name,blank)
    cv2.imshow(ct2.name,blank)
    cv2.imshow(disparity,blank)
    cv2.moveWindow(ct1.name,0,500)
    cv2.moveWindow(disparity,0+pixel_width,500)
    cv2.moveWindow(ct2.name,0+(pixel_width*2),500)

    rec = Recognizer_Thread()
    rec.start()

    # https://github.com/opencv/opencv/blob/3.4/samples/python/stereo_match.py
    # disparity range is tuned for 'aloe' image pair
#    window_size = 3 #3
#    min_disp = 16 #16
#    num_disp = 112-min_disp #112

#    stereo = cv2.StereoSGBM_create(
#      minDisparity = min_disp,
#      numDisparities = num_disp,
#      blockSize = 16,
#      P1 = 8*3*window_size**2,
#      P2 = 32*3*window_size**2,
#      disp12MaxDiff = 1,
#      uniquenessRatio = 10,
#      speckleWindowSize = 100,
#      speckleRange = 32
#    )

    block_size = 3
    min_disp = 0
    num_disp = 80 - min_disp #96

    stereo = cv2.StereoSGBM_create(minDisparity   = min_disp, 
                                   numDisparities = num_disp,
                                   blockSize      = block_size,
                                   P1 = 8  * 3 * block_size**2,
                                   P2 = 32 * 3 * block_size**2,
                                   disp12MaxDiff = 1, #0 seemed marignally worse?
                                   preFilterCap = 0,
                                   uniquenessRatio = 10,
                                   speckleRange = 0,  #1-2 seemed very speckly
                                   speckleWindowSize = 25, # above 25 seems okay
                                   mode = 4) # mode zero or 2 seem viable, 4 most accurate?

    cpu = CPUTemperature()

    while True:
      # get frames
      leftFrame = ct1.next()
      rightFrame = ct2.next()
#      targets = rec.next(leftFrame,rightFrame)

      # display coordinate data
      fps1 = int(ct1.current_frame_rate)
      fps2 = int(ct2.current_frame_rate)

      # display frame
      cv2.imshow("Left",leftFrame)
      cv2.imshow("Right",rightFrame)

      #disp = stereo.compute( cv2.pyrDown(leftFrame), cv2.pyrDown(rightFrame)).astype(np.float32) / 16.0
      disp = stereo.compute(leftFrame, rightFrame).astype(np.float32) / 16.0
      cv2.imshow(disparity, (disp - min_disp)/num_disp)

      # detect keys
      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        break

      if main_loop_count >= 10:
        # update loop rate
        main_loop_rate = round(main_loop_count/(time.time()-t1),2)
        main_loop_count = 0
        t1 = time.time()

        #print('generating 3d point cloud...',)
        #h, w = imgL.shape[:2]
        #f = 0.8*w                          # guess for focal length
        #Q = np.float32([[1, 0, 0, -0.5*w],
        #                 [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
        #                 [0, 0, 0,     -f], # so that y-axis looks up
        #                 [0, 0, 1,      0]])
        #points = cv.reprojectImageTo3D(disp, Q)
        #colors = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
        #mask = disp > disp.min()
        #out_points = points[mask]
        #out_colors = colors[mask]
        #out_fn = 'out.ply'
        #write_ply(out_fn, out_points, out_colors)
        #print('%s saved' % out_fn)

#        t = vcgencmd.measure_temp()
        text = 'T: {} FPS: {}/{} LPS {}:'.format(cpu.temperature,fps1,fps2,main_loop_rate)
        print(text)
        lineloc = 0
        lineheight = 30
#        for t in text.split('\n'):
#          lineloc += lineheight
#          cv2.putText(leftFrame,
#                      t,
#                      (10,lineloc), # location
#                      cv2.FONT_HERSHEY_PLAIN, # font
#                      1.5, # size
#                      (0,255,0), # color
#                      1, # line width
#                      cv2.LINE_AA,
#                      False)
#      elif key != 255:
#        print('KEY PRESS:',[chr(key)])

      main_loop_count += 1

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
  camera_init = 0.01

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
      time.sleep(0.01)

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
#    self.loop_start_time = time.time()

    # frame rate
    fc = 0
    t1 = time.time()

    # loop
    while True:

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
#    self.loop_start_time = 0
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


# ---
# Face recgnizer
# ---

class Recognizer_Thread:

  buffer = None
  leftFrame = np.zeros(shape=(300,300,3)).astype('uint8')
  rightFrame = np.zeros(shape=(300,300,3)).astype('uint8')

  # load our serialized face detector from disk
#  print("[INFO] loading face detector...")
  protoPath = "face_detection_model/deploy.prototxt"
  modelPath = "face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
  detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

  # load our serialized face embedding model from disk
#  print("[INFO] loading face recognizer...")
  embedder = cv2.dnn.readNetFromTorch("embedding_model/openface_nn4.small2.v1.t7")

  # load the actual face recognition model along with the label encoder
  recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())
  le = pickle.loads(open("output/le.pickle", "rb").read())

  def start(self):
    self.buffer = queue.Queue(1)
    self.thread = threading.Thread(target=self.loop)
    print('Starting recognizer')
    self.thread.start()

  def loop(self):
    while True:
      t0 = time.time()
      frame = self.leftFrame

      # height, width, number of channels in image
#      print('Original dims: ', frame.shape)

      # resize the frame to have a width of 600 pixels (while maintaining the aspect ratio), and then grab the image dimensions
      #frame = imutils.resize(frame, width=600)
      (h, w) = frame.shape[:2]

      # construct a blob from the image, blobbing is fast
      imageBlob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)
      #print('Time to blob ', time.time()-t0)

      # apply OpenCV's deep learning-based face detector to localize faces in the input image, detecting is slow ~0.36s
      self.detector.setInput(imageBlob)
      detections = self.detector.forward()
#     print('Time to detect ', time.time()-t0)

      targets = []
      # loop over the detections
      for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > 0.5:
          # compute the (x, y)-coordinates of the bounding box for the face
          box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
          (startX, startY, endX, endY) = box.astype("int")

          # extract the face ROI
          face = frame[startY:endY, startX:endX]
          (fH, fW) = face.shape[:2]

          boxArea = (endX - startX) * (endY - startY)
          area = h*w
          p = 100 * boxArea / area

          # todo: fix param 2 and 3 as these should be middle of target not just +10
          #               %, targetX , targetY , boxX , boxY ,boxWidth, boxHieght
          targets.append((p,startX+10,startY+10,startX,startY,fW,fH))
          # ensure the face width and height are sufficiently large
          if fW < 20 or fH < 20:
            continue

	  # construct a blob for the face ROI, then pass the blob through our
          # face embedding model to obtain the 128-d quantification of the face
          faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
          self.embedder.setInput(faceBlob)
          vec = self.embedder.forward()

          # perform classification to recognize the face
          preds = self.recognizer.predict_proba(vec)[0]
          j = np.argmax(preds)
          proba = preds[j]
          name = self.le.classes_[j]

          # draw the bounding box of the face along with the associated probability
          text = "Detected {}, {:.2f}% certain in {:.2f}".format(name, proba * 100,time.time()-t0)
          print(text)
          y = startY - 10 if startY - 10 > 10 else startY + 10
#          cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
#          cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

      # open a spot in the buffer
      if self.buffer.full():
        self.buffer.get()

      targets = [(x,y,bx,by,bw,bh) for (size,x,y,bx,by,bw,bh) in targets]
      self.buffer.put(targets,False)

#    print('never getting here')

  def next(self,lFrame,rFrame):
    self.leftFrame = lFrame
    self.rightFrame = rFrame

    # get from buffer (fail if empty)
    try:
      targets = self.buffer.get(False)
    except queue.Empty:
      targets = []
#      print('Queue Empty!')
      pass

    # done
    return targets

  def stop():
    self.buffer = None

if __name__ == '__main__':
  run()
