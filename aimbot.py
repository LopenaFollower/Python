import cv2
import numpy as np
import pyautogui
import win32api,win32con
import mss
import keyboard
import time

running=False
target1=np.array([145,150,150])
target2=np.array([160,255,255])
sw,sh=pyautogui.size()
area={
	"left":sw//2-160,
	"top":sh//2-120,
	"width":320,
	"height":240
}
def crop(frame,cw,ch):
	h,w,_=frame.shape
	stx=w//2-cw//2
	sty=h//2-ch//2
	return frame[sty:sty+ch,stx:stx+cw],stx,sty

def find_target(frame):
	ca,ox,oy=crop(frame,160,120)
	cont,_=cv2.findContours(cv2.inRange(cv2.cvtColor(ca,cv2.COLOR_BGR2HSV),target1,target2),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if cont:
		cont=[c for c in cont if cv2.contourArea(c)>50]
		if cont:
			cx=ca.shape[1]//2
			x,y,w,h=cv2.boundingRect(min(cont,key=lambda c:abs((cv2.boundingRect(c)[0]+cv2.boundingRect(c)[2]//2)-ca.shape[1]//2)))
			return ox+x+w//2,oy+y+1
	return None

def toggle():
	global running
	running=not running

keyboard.add_hotkey("`",toggle)

with mss.mss()as sct:
	while keyboard.is_pressed("=")==False:
		time.sleep(0.01)
		if running:
			img=np.array(sct.grab(area))
			frame=cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
			t=find_target(frame)
			if t:
				sx=t[0]+area["left"]-sw//2
				sy=t[1]+area["top"]-sh//2
				dx=np.sign(sx)
				dy=np.sign(sy)
				win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,dx*int((dx*sx)**.5),dy*int((dy*sy)**.5),0,0)