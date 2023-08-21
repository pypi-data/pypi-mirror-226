"""
©Copyright Shadow Studio
Python package omiga (beta)

Use:
-----
·This library is used to make 2D games and includes physics engines, rendering, and other features
·You can make games by class Stage,Function,Canvas,Music,Sprite,Physics and Interaction

Our Links:
----------
·shadowoffice.mysxl.cn
·xiaoying-command-line.mysxl.cn

Thanks:
--------
·All members in Shadow Studio
·Python Program Language
·Github
·shequ.codemao.cn
·kitten4.codemao.cn

That's all
"""

from tkinter import *
import turtle
from PIL import Image
import sys
import time
import math
import webbrowser
import os
import winsound
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
import wave
import contextlib
import functools
import random

number=1
physics_list=[]
airtemperature=25
wind_velocity=0
wind_angle=None

class Stage:
    """
    The Window class is used to create a window and assume basic game window settings
    """
    def __init__(self,width=800,height=600,caption="omiga"):
        self.objects=[]
        self.p=turtle.Pen()
        self.p.hideturtle()
        self.positioned=False
        self.title=caption
        self.boot=True
        self.mp=(0,0)
        """
        Create a window here
        """
        self.WIDTH=width
        self.HEIGHT=height
        self.CAPTION=caption
        self.w=width
        self.h=height
        self.ms=turtle.Screen()
        self.ms._root.resizable(False,False)
        self.ms.setup(width,height)
        self.ms.title(caption)
        self.ms.tracer(0)
        self.ms.bgcolor("black")
        self.ms._canvas.config(bd=0,highlightthickness=0)
        self.ms._root.bind("<Motion>",self.on_mouse_motion)
        self.ms._root.protocol("WM_DELETE_WINDOW",self.passed)
    def passed(self):
        pass
    def init(self):
        """
        When creating a window, the initial information is retained and this function is used to reply to the initial state of the window
        
        Example:
            win=omiga.Window(**args)
            win.set_mode(400,300)
        >   win.init()
        """
        self.ms._root.resizable(False,False)
        self.ms.setup(self.WIDTH,self.HEIGHT)
        self.ms.title(self.CAPTION)
        self.ms.bgcolor("black")
        self.ms._canvas.config(bd=0,highlightthickness=0)
    def quit(self):
        """
        Quit the window

        Example:
            stage=Stage()
        >   stage.quit()
        """
        self.ms._root.destroy()
        sys.exit()
    def set_mode(self,width,height):
        """
        After creating the window, if you want to modify the window size again, you can use this function to modify it

        Example:
            win=omiga.Window(**args)
        >   win.set_mode(400,300)
            win.run()
        """
        self.ms.setup(width,height)
        self.w,self.h=width,height
    def set_caption(self,caption):
        """
        After creating a window, if you want to modify the window title again, you can use this function to modify it

        Example:
            win=omiga.Window(**args)
        >   win.set_caption("Hello World")
        """
        self.ms.title(caption)
        self.title=caption
    def set_width(self,width):
        """
        Set width for the window

        Example:
            win=omiga.Window(**args)
        >   win.set_width(400)
        """
        self.w=width
        self.ms.setup(self.w,self.h)
    def set_height(self,height):
        """
        Set height for the window

        Example:
            win=omiga.Window(**args)
        >   win.set_height(300)
        """
        self.h=height
        self.ms.setup(self.w,self.h)
    def set_icon(self,ico):
        """
        Set the icon into bitmap

        Example:
            win=omiga.Window(**args)
        >   win.set_icon("photo.ico")
        """
        self.ms._root.iconbitmap(ico)
    def set_background(self,color):
        """
        Set background color for the window

        Example:
            win=omiga.Window(**args)
        >   win.set_background("red")
        """
        self.ms.bgcolor(color)
    def set_backpicture(self,picture):
        """
        Put a picture on the lowest window floor

        Example:
            win=omiga.Window(**args)
        >   win.set_backpicture("back.png")
        """
        self.ms.bgpic(picture)
    def update(self):
        """
        Update the window

        Example:
            win=omiga.Window(**args)
            while True:
        >       win.update()
                win.set_width(win.get_width()+1)
            win.run()
        """
        self.ms.update()
    def clear(self):
        """
        Clear everything on the window

        Example:
            win=omiga.Window(**args)
            pen=omiga.Pen(win) #Needs to bind the window
            pen.advance(100)
        >   win.clear()
        """
        for item in self.objects:
            try:
                item.clear()
            except:
                sys.exit()
    def toplevel(self):
        """
        Place the window on the highest layer

        Example:
            win=omiga.Window(**args)
        >   win.toplevel()
        """
        self.ms._root.attributes("-topmost",True)
    def relevel(self):
        """
        Place the window on the simple layer

        Example:
            win=omiga.Window(**args)
            win.toplevel()
        >   win.relevel()
        """
        self.ms._root.attributes("-topmost",False)
    def show_axis(self,maincolor="white",othercolor="gray"):
        """
        Draw the coordinate system on the window

        Example:
            win=omiga.Window(**args)
        >   win.show_position()
        """
        self.positioned=True
        self.ms.tracer(0)
        self.p.up()
        self.p.hideturtle()
        #Other
        self.p.pencolor(othercolor)
        for i in range(-20,21):
            if i!=0:
                self.p.up()
                self.p.goto(0,self.ms._root.winfo_screenheight()/2/10*i)
                self.p.down()
                self.p.forward(self.ms._root.winfo_screenwidth()/2)
                self.p.backward(self.ms._root.winfo_screenwidth())
                self.p.forward(self.ms._root.winfo_screenwidth()/2)
                self.p.pencolor(maincolor)
                self.p.write(f" {int(self.ms._root.winfo_screenheight()/2/10*i)}",align="left")
        self.p.penup()
        self.p.goto(0,0)
        self.p.left(90)
        for i in range(-20,21):
            if i!=0:
                self.p.up()
                self.p.goto(self.ms._root.winfo_screenwidth()/2/10*i,0)
                self.p.down()
                self.p.setheading(90)
                self.p.forward(self.ms._root.winfo_screenheight()/2)
                self.p.backward(self.ms._root.winfo_screenheight())
                self.p.forward(self.ms._root.winfo_screenheight()/2)
                self.p.pencolor(maincolor)
                self.p.write(f" {int(self.ms._root.winfo_screenwidth()/2/10*i)}",align="left")
        self.p.up()
        self.p.goto(0,0)
        self.p.up()
        #Main
        self.p.pencolor(maincolor)
        self.p.pensize(1.5)
        self.p.setheading(0)
        self.p.goto(0,0)
        self.p.down()
        self.p.forward(self.ms._root.winfo_screenwidth()/2)
        self.p.backward(self.ms._root.winfo_screenwidth())
        self.p.goto(0,0)
        self.p.left(90)
        self.p.forward(self.ms._root.winfo_screenheight()/2)
        self.p.backward(self.ms._root.winfo_screenheight())
        self.p.goto(0,0)
        self.p.up()
        self.ms.update()
    def hide_axis(self):
        """
        Hide window coordinate system

        Example:
            win=omiga.Window(**args)
            win.show_position(maincolor="black")
        >   win.hide_position()
        """
        self.p.clear()
        self.positioned=False
    def set_freemode(self):
        """
        Allow windows to be manually resized

        Example:
            win=omiga.Window(**args)
        >   win.set_freemode()
        """
        self.ms._root.resizable(True,True)
    def set_disfreemode(self):
        """
        Prevent windows from being manually resized

        Example:
            win=omiga.Window(**args)
            win.set_freemode()
            if <condition>:
        >       win.set_disfreemode()
        """
        self.ms._root.resizable(False,False)
    def set_solidframe(self,solargu=2):
        """
        Make the window more three-dimensional

        Example:
            win=omiga.Window(**args)
        >   win.set_solidframe(solargu=10)
        """
        self.ms._canvas.config(bd=solargu,highlightthickness=1)
    def set_planaframe(self):
        """
        Make the window more flat

        Example:
            win=omiga.Window(**args)
        >   win.set_planaframe()
        """
        self.ms._canvas.config(bd=0,highlightthickness=0)
    def schedule(self,func,time):
        """
        Used to schedule a library function

        Example:
            win=omiga.Window(**args)
            
            def say_hello():
                print("Hello World")
        >       win.schedule(say_hello,1)
            say_hello()
        """
        self.ms.ontimer(func,time*1000)
    def framerate(self,r):
        """
        Set the update rendering frequency within the window

        Example:
            win=omiga.Window(**args)
            while True:
                print("Hello World")
        >       win.framerate(60) #rate 60 times every seconds
        """
        time.sleep(1/r)
    def get_mouse_position(self):
        if self.mp[0]>self.ms._root.winfo_width()/2:
            x=int(self.mp[0]-self.ms._root.winfo_width()/2)
        if self.mp[0]<self.ms._root.winfo_width()/2:
            x=int(-self.ms._root.winfo_width()/2+self.mp[0])
        if self.mp[0]==self.ms._root.winfo_width()/2:
            x=0
        if self.mp[1]>self.ms._root.winfo_height()/2:
            y=-int(self.mp[1]-self.ms._root.winfo_height()/2)
        if self.mp[1]<self.ms._root.winfo_height()/2:
            y=-int(-self.ms._root.winfo_height()/2+self.mp[1])
        if self.mp[1]==self.ms._root.winfo_height()/2:
            y=0
        return (x,y)
    def wait(self,sec):
        """
        Suspend a thread for a period of time

        Example:
            win=omiga.Window(**args)
        >   win.wait(5) #wait for 5 seconds
        """
        time.sleep(sec)
    def run(self):
        """
        At runtime, you need to use this line of code to fix the window and enter the main loop

        Example:
            win=omiga.Window(**args)
        >   win.run()
        """
        try:
            turtle.done()
        except:
            sys.exit()
    def on_mouse_motion(self,event):
        self.ms._root.update()
        self.mp=(event.x,event.y)
        if self.positioned==True:
            if event.x>self.ms._root.winfo_width()/2:
                x=int(event.x-self.ms._root.winfo_width()/2)
            if event.x<self.ms._root.winfo_width()/2:
                x=int(-self.ms._root.winfo_width()/2+event.x)
            if event.x==self.ms._root.winfo_width()/2:
                x=0
            if event.y>self.ms._root.winfo_height()/2:
                y=-int(event.y-self.ms._root.winfo_height()/2)
            if event.y<self.ms._root.winfo_height()/2:
                y=-int(-self.ms._root.winfo_height()/2+event.y)
            if event.y==self.ms._root.winfo_height()/2:
                y=0
            self.ms.title(f"{self.title} ({x},{y})")
        else:
            self.ms.title(self.title)

class Function:
    """
    Used to create and store a Function object
    """
    def __init__(self,anfo="y=x",domain=[-100,100]):
        """
        Create a function here
        """
        self.lanfo=anfo
        self.ldomain=domain
    def get_domain(self):
        """
        Get the Domain of a function of the function

        Example:
            fx=omiga.Function(anfo="y=x+4",domain=[0,100])
        >   print(fx.domain())
        """
        return self.ldomain
    def get_right_term(self):
        """
        Get the right term of the function

        Example:
            fx=omiga.Function(anfo="y=x+4",domain=[0,100])
        >   print(fx.right_term())
        """
        return self.lanfo.split("=")[1]
    def get_left_term(self):
        """
        Get the left term of the function

        Example:
            fx=omiga.Function(anfo="y=x+4",domain=[0,100])
        >   print(fx.left_term())
        """
        return self.lanfo.split("=")[0]
    def get_range(self):
        """
        Get the range of the function

        Example:
            fx=omiga.Function(anfo="y=x+4",domain=[0,100])
        >   print(fx.range())
        """
        value_list=[]
        for item in range(self.ldomain[0],self.ldomain[1]+1):
            try:
                a=eval(self.get_right_term().replace("x",str(item)))
                value_list.append(a)
            except:
                pass
        maxval=max(value_list)
        minval=min(value_list)
        return [minval,maxval]
    def get_value(self,x):
        """
        Get the value of the function

        Example:
            fx=omiga.Function(anfo="y=x+4",domain=[0,100])
        >   print(fx.value(4)) #return 8
        """
        return eval(self.get_right_term().replace("x",str(x)))
    def set_anfo(self,anfo):
        """
        Set the analytical expression of the function

        Example:
            fx=omiga.Function(anfo="y=x+4",domain=[0,100])
        >   fx.set_anfo(anfo="y=x+5")
        """
        self.lanfo=anfo
    def set_domain(self,domain):
        """
        Set the Domain of a function of the function

        Example:
            fx=omiga.Function(anfo="y=x+4",domain=[0,100])
        >   fx.set_domain(domain=[0,200])
        """
        self.ldomain=domain

class Canvas:
    """
    The Canvas class is used to draw basic graphics on a window
    """
    def __init__(self,window):
        """
        Bind a window class here
        """
        self.t=turtle.Pen()
        self.t.hideturtle()
        self.t.up()
        window.objects.append(self.t)
        self.ms=turtle.Screen()
        self.ms.tracer(0)
    def clear(self):
        """
        Empty canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.clear()
        """
        self.t.clear()
    def draw_point(self,position,color="white",size=1):
        """
        Draw a point on the canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_point((0,0),color="red",size=5)
        """
        try:
            self.t.pencolor(color)
        except:
            pass
        self.t.pensize(size)
        self.t.goto(position[0],position[1])
        self.t.down()
        self.t.dot(size,color)
        self.t.up()
    def draw_line(self,position1,position2,color="white",size=1):
        """
        Draw a line on the canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_point((-100,-100),(100,100),color="red",size=5)
        """
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.goto(position1[0],position1[1])
        self.t.down()
        self.t.goto(position2[0],position2[1])
        self.t.up()
    def draw_triangle(self,position1,position2,position3,color="white",size=1,fill=None):
        """
        Draw a triangle on the canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_triangle((-100,-100),(100,100),(100,50),color="red",size=5,fill="red")
        """
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.goto(position1[0],position1[1])
        self.t.down()
        if fill!=None:
            self.t.fillcolor(fill)
            self.t.begin_fill()
        self.t.goto(position2[0],position2[1])
        self.t.goto(position3[0],position3[1])
        self.t.goto(position1[0],position1[1])
        if fill!=None:
            self.t.end_fill()
        self.t.up()
    def draw_quadrilateral(self,position1,position2,position3,position4,color="white",size=1,fill=None):
        """
        Draw a quadrilateral on the canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_quadrilateal((-100,-100),(100,100),(100,50),(200,25),color="red",size=5,fill="red")
        """
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.goto(position1[0],position1[1])
        self.t.down()
        if fill!=None:
            self.t.fillcolor(fill)
            self.t.begin_fill()
        self.t.goto(position2[0],position2[1])
        self.t.goto(position3[0],position3[1])
        self.t.goto(position4[0],position4[1])
        self.t.goto(position1[0],position1[1])
        if fill!=None:
            self.t.end_fill()
        self.t.up()
    def draw_square(self,position,sidelength,color="white",size=1,fill=None):
        """
        Draw a square on the canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_square((0,0),sidelength=5,color="red",size=3,fill="blue")
        """
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.goto(position[0],position[1])
        self.t.setheading(0)
        self.t.forward(sidelength/2)
        self.t.left(90)
        self.t.down()
        if fill!=None:
            self.t.fillcolor(fill)
            self.t.begin_fill()
        self.t.forward(sidelength/2)
        self.t.left(90)
        self.t.forward(sidelength)
        self.t.left(90)
        self.t.forward(sidelength)
        self.t.left(90)
        self.t.forward(sidelength)
        self.t.left(90)
        self.t.forward(sidelength/2)
        if fill!=None:
            self.t.end_fill()
        self.t.up()
    def draw_rect(self,position,width,height,color="white",size=1,fill=None):
        """
        Draw a rect on the canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_rect((0,0),width=50,height=20,color="red",size=3,fill="blue")
        """
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.goto(position[0],position[1])
        self.t.setheading(0)
        self.t.forward(width/2)
        self.t.left(90)
        self.t.down()
        if fill!=None:
            self.t.fillcolor(fill)
            self.t.begin_fill()
        self.t.forward(height/2)
        self.t.left(90)
        self.t.forward(width)
        self.t.left(90)
        self.t.forward(height)
        self.t.left(90)
        self.t.forward(width)
        self.t.left(90)
        self.t.forward(height/2)
        if fill!=None:
            self.t.end_fill()
        self.t.up()
    def draw_polygon(self,positions,color="white",size=1,fill=None):
        """
        Draw a polygon on the canvas

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_polygon(positions=[(-100,-100),(100,100),(100,50)],color="red",size=5,fill="red")
        """
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.goto(positions[0][0],positions[0][1])
        self.t.down()
        if fill!=None:
            self.t.fillcolor(fill)
            self.t.begin_fill()
        for position in positions[1:]:
            self.t.goto(position[0],position[1])
        self.t.goto(positions[0][0],positions[0][1])
        if fill!=None:
            self.t.end_fill()
        self.t.up()
    def draw_arc(self,position,radius,ia,ra=0,color="white",size=1):
        """
        Draw a arc on the window
        Tip:the ia is the arc's angle and the ra is the arc's spin angle(0-360)

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_arc((0,0),radius=100,ia=50,ra=90,color="red",size=1)
        """
        self.t.goto(position[0],position[1])
        self.t.setheading(ra)
        self.t.forward(radius)
        self.t.right(90)
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.down()
        self.t.circle(-radius,ia)
        self.t.up()
        self.t.left(90)
        self.t.backward(radius)
        self.t.setheading(ra)
    def draw_sector(self,position,radius,ia,ra=0,color="white",size=1,fill=None):
        """
        Draw a sector on the window
        Tip:the ia is the arc's angle and the ra is the arc's spin angle(0-360)

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_sector((0,0),radius=100,ia=50,ra=90,color="red",size=1,fill="red")
        """
        self.t.goto(position[0],position[1])
        self.t.setheading(ra)
        if fill!=None:
            self.t.fillcolor(fill)
            self.t.begin_fill()
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.down()
        self.t.forward(radius)
        self.t.right(90)        
        self.t.circle(-radius,ia)
        self.t.left(90)
        self.t.backward(radius)
        self.t.up()
        if fill!=None:
            self.t.end_fill()
        self.t.up()
        self.t.setheading(ra)
    def draw_circle(self,position,radius,color="white",size=1,fill=None):
        """
        Draw a circle on the window

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_circle((0,0),radius=100,color="red",size=1,fill="red")
        """
        self.t.goto(position[0],position[1])
        self.t.setheading(0)
        if fill!=None:
            self.t.fillcolor(fill)
            self.t.begin_fill()
        self.t.pencolor(color)
        self.t.pensize(size)
        self.t.forward(radius)
        self.t.down()
        self.t.right(90)        
        self.t.circle(-radius)
        self.t.left(90)
        self.t.up()
        self.t.backward(radius)
        self.t.up()
        if fill!=None:
            self.t.end_fill()
        self.t.up()
        self.t.setheading(0)
    def draw_function(self,func,color="white",size=1):
        """
        Convert an analytical expression into an image and draw it on the window

        Example:
            l1=omiga.Function("y=x+3",domain=[-20,20])
            canvas=omiga.Canvas(win)
        >   canvas.draw_function(func=l1,color="red",size=2)
        """
        xt=func.get_right_term()
        dots=[]
        for item in range(func.get_domain()[0],func.get_domain()[1]+1):
            try:
                dots.append([item,eval(xt.replace("x",str(item)))])
            except:
                dots.append(["none"])
        self.t.penup()
        try:
            self.t.goto(dots[0][0],dots[0][1])
        except:
            pass
        self.t.pendown()
        self.t.pencolor(color)
        self.t.pensize(size)
        for item in dots:
            if item!=["none"]:
                try:
                    self.t.goto(item[0],item[1])
                except:
                    pass
                self.t.down()
            else:
                self.t.up()
        try:
            self.t.penup()
        except:
            pass
    def draw_brokenline(self,positions,color="white",size=1):
        """
        Draw a brokenline on the window

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_brokenline([(-50,100),(0,0),(50,120)],color="red",size=1)
        """
        self.t.up()
        self.t.goto(positions[0][0],positions[0][1])
        self.t.down()
        self.t.pencolor(color)
        self.t.pensize(size)
        for item in positions:
            self.t.goto(item[0],item[1])
        self.t.up()
    def draw_link(self,position,link,text="link",large=10,background="black",color="blue"):
        """
        Draw a link on the window

        Example:
            canvas=omiga.Canvas(win)
        >   canvas.draw_link((0,0),link="www.python.org",color="blue")
        """
        px=position[0]
        py=position[1]
        self.ms._root.attributes("-transparentcolor","#000001")
        self.ms._root.update()
        rx=self.ms._root.winfo_width()/2+px
        ry=self.ms._root.winfo_height()/2-py
        def lopen():
            webbrowser.open(link)
        Button(self.ms._root,text=text,font=("shadow studio font",large,"underline"),foreground=color,bd=0,background=background,activebackground=background,activeforeground="purple",command=lopen).place(x=rx,y=ry,anchor=CENTER)

class Music:
    """
    Music class is used to play music
    """
    def __init__(self,file=None):
        """
        Set a music here
        """
        self.music=file
    def load_music(self,file):
        """
        Set a music for the class

        Example:
            m=omiga.Music()
        >   m.load_music(file="example.wav") #can't a mp3 or others
        """
        self.music=file
    def play(self):
        """
        Play a sound in the program process

        Example:
            m=omiga.Music(file="example.wav")
        >   m.play()
        """
        winsound.PlaySound(self.music,0)
    def loop_play(self):
        """
        Play a music for loop

        Example:
            m=omiga.Music(file="example.wav")
        >   m.loop_play()
        """
        winsound.PlaySound(self.music,winsound.SND_FILENAME|winsound.SND_LOOP)
    def stop(self):
        """
        Stop every music playing in the program process

        Example:
            m=omiga.Music(file="example.wav")
            m.loop_play()
            time.sleep(5) #import time
        >   m.stop()
        """
        winsound.PlaySound(None,winsound.SND_FILENAME)
    def beep(self,frequency,time):
        """
        Play a beep

        Example:
            m=omiga.Music()
        >   m.beep(frequency=37,time=1)
        """
        winsound.Beep(frequency,time*1000)
    def get_volume(self):
        """
        Get the volume of the computer

        Example:
            m=omiga.Music()
        >   print(m.get_volume())
        """
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume.GetMasterVolumeLevel()
    def get_volume_range(self):
        """
        Get the volume range of the computer

        Example:
            m=omiga.Music()
        >   print(m.get_volume_range())
        """
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume.GetVolumeRange()
    def set_volume(self,level):
        """
        Set volume for the window

        Example:
            m=omiga.Music()
        >   m.set_volume(100)
        """
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        grange=volume.GetVolumeRange()
        print(grange[0]+(grange[1]-grange[0])/100*level)
        volume.SetMasterVolumeLevel(grange[0]+(grange[1]-grange[0])/100*level, None)
    def get_length(self):
        """
        Get the length of the music

        Example:
            m=omiga.Music("example.wav")
        >   print(m.get_length())
        """
        with contextlib.closing(wave.open(self.music,'r')) as f:
            frames=f.getnframes()
            rate=f.getframerate()
            duration=int(frames/float(rate))
            return duration

class Sprite:
    """
    Sprite class is used to create a sprite and edit the sprite
    """
    def __init__(self,img=None):
        global number
        """
        Create a sprite here
        """
        self.sculpt=[]
        self.attributes={"collision":True}
        if img!=None:
            self.sculpt.append(img)
        self.tsprite_number=(7-len(str(number)))*"0"+str(number)
        self.create_time=time.time()
        number+=1
        self.sprite=turtle.Pen()
        self.sprite.penup()
        self.sprite.pencolor("white")
        self.sprite.fillcolor("black")
        self.sprite.shape("circle")
        self.sculpt_number=0
        self.ms=turtle.Screen()
        self.ms.tracer(0)
        self.speed=0
        self.addspeed=0
        self.cradius=0
    def sprite_id(self):
        """
        Return the sprite's number

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.sprite_number())
        """
        msg={self.tsprite_number:(self.create_time,self.sculpt)}
        return msg
    def create_sculpt(self,img):
        """
        Create a new sculpt for the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.create_sculpt(img="picture1.gif")
        """
        self.sculpt.append(img)
    def create_sculpt_by_list(self,imgs):
        """
        Create a new sculpt for the sprite by list

        Example:
            s=omiga.Sprite()
        >   s.create_sculpt_by_list(imgs=["picture.gif","picture1.gif"])
        """
        for item in imgs:
            self.sculpt.append(item)
    def delete_sculpt(self,index):
        """
        Remove a sculpt from list "self.sculpt"

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.delete_sculpt(index=0)
        """
        self.sculpt.pop(index)
    def get_sculpt(self):
        """
        Get the sculpt list of the class sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.get_sculpt())
        """
        return self.sculpt
    def sculpt_length(self):
        """
        Get the length of the sculpt list

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.sculpt_length())
        """
        return len(self.sculpt)
    def set_attributes(self,key,value):
        """
        Set attributes for the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.set_attributes(key="name",value="sprite")
        """
        self.attributes.update({key:value})
    def get_attributes(self,key):
        """
        Find the attributes in the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.get_attributes(key="name")
        """
        return self.attributes[key]
    def get_resolution(self):
        """
        Get the height of the sprite image
        
        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.get_height())
        """
        dict={}
        for item in self.sculpt:
            dict.update({str(item):(Image.open(item).width,Image.open(item).height)})
        return dict
    def get_ram(self):
        """
        Get the ram of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.ram())
        """
        dict={}
        for item in self.sculpt:
            dict.update({str(item):int(Image.open(item).width)*int(Image.open(item).height)})
        return dict
    def load_sculpt(self):
        """
        Load the sculpt from the sculpt list

        Example:
            s=omiga.Sprite(img="picture1.gif")
            s.create_sculpt_by_list(["picture2.gif","picture3.gif"])
        >   s.load_sculpt()
            s.set_sculpt(2)
        """
        for item in self.sculpt:
            self.ms.addshape(item)
    def set_sculpt(self,index):
        """
        Set the sprite's sculpt

        Example:
            s=omiga.Sprite(img="picture1.gif")
            s.create_sculpt_by_list(["picture2.gif","picture3.gif"])
            s.load_sculpt()
        >   s.set_sculpt(2)
        """
        self.sprite.shape(self.sculpt[index])
        self.sculpt_number=index
    def next_sculpt(self):
        """
        Set the sprite the next sculpt

        Example:
            s=omiga.Sprite(img="picture1.gif")
            s.create_sculpt_by_list(["picture2.gif","picture3.gif"])
            s.load_sculpt()
            while True:
        >       s.next_sculpt()
        """
        if self.sculpt_number<len(self.sculpt)-1:
            self.sculpt_number+=1
            self.sprite.shape(self.sculpt[self.sculpt_number])
        else:
            self.sculpt_number=0
            self.sprite.shape(self.sculpt[0])
    def last_sculpt(self):
        """
        Set the sprite the last sculpt

        Example:
            s=omiga.Sprite(img="picture1.gif")
            s.create_sculpt_by_list(["picture2.gif","picture3.gif"])
            s.load_sculpt()
            while True:
        >       s.last_sculpt()
        """
        if self.sculpt_number>0:
            self.sculpt_number-=1
            self.sprite.shape(self.sculpt[self.sculpt_number])
        else:
            self.sculpt_number=len(self.sculpt)-1
            self.sprite.shape(self.sculpt[self.sculpt_number])
    def top(self):
        """
        Return the top of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.top())
        """
        return self.sprite.ycor()+(Image.open(self.sculpt[self.sculpt_number]).height)/2
    def bottom(self):
        """
        Return the bottom of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.bottom())
        """
        return self.sprite.ycor()-(Image.open(self.sculpt[self.sculpt_number]).height)/2
    def left(self):
        """
        Return the left of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.left())
        """
        return self.sprite.xcor()-(Image.open(self.sculpt[self.sculpt_number]).width)/2
    def right(self):
        """
        Return the right of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   print(s.right())
        """
        return self.sprite.xcor()+(Image.open(self.sculpt[self.sculpt_number]).width)/2
    def translate(self,direction,length):
        """
        Let the sprite translate a length

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.translate(45,100)
        """
        self.sprite.setheading(direction)
        self.sprite.forward(length)
    def advance(self,length):
        """
        Let the sprite move a length

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.move(100) 
        """
        self.sprite.forward(length)
    def position(self,x,y):
        """
        Let the sprite move to the position (x,y)

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.position(100,100)
        """
        self.sprite.goto(x,y)
    def update(self):
        """
        Update the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.update()
        """
        self.sprite.forward(self.speed)
        self.speed+=self.addspeed
        self.ms.update()
    def turn_left(self,angle):
        """
        Let the sprite turn left an angle

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.turn_left(45)
        """
        self.sprite.left(angle)
    def turn_right(self,angle):
        """
        Let the sprite turn right an angle

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.turn_right(45)
        """
        self.sprite.right(angle)
    def set_speed(self,speed):
        """
        Set the sprite's speed

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.set_speed(1)
        """
        self.speed=speed
    def set_addspeed(self,addspeed):
        """
        Set the sprite's addspeed

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.set_addspeed(1)
        """
        self.addspeed=addspeed
    def set_angle(self,angle):
        """
        Set angle for the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.set_angle(135)
        """
        self.sprite.setheading(angle)
    def distance(self,sprite):
        """
        Return the distance between the sprite and the other sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
            s1=omiga.Sprite(img="picture1.gif")
            s1.position(100,100)
        >   print(s.distance(s1))
        """
        return math.sqrt(pow(self.sprite.xcor()-sprite.sprite.xcor(),2)+pow(self.sprite.ycor()-sprite.sprite.ycor(),2))
    def set_collision_radius(self,radius):
        """
        Set the collision radius of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.set_collision_radius(radius=30)
        """
        self.cradius=radius
    def is_collision(self,sprite):
        """
        Check the sprite if collision to the other sprite

        Example:
            s1=omiga.Sprite(img="picture.gif")
            s2=omiga.Sprite(img="picture1.gif")
        >   if (s1.is_collision(s2)==True):
                print("Collision!")
        """
        boolean=None
        if self.distance(sprite)<=(self.cradius+sprite.cradius):
            boolean=True
        else:
            boolean=False
        return boolean
    def hide(self):
        """
        Let the sprite hide on the window

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.hide()
        """
        self.sprite.hideturtle()
    def show(self):
        """
        Let the sprite show on the window

        Example:
            s=omiga.Sprite(img="picture.gif")
        >   s.show()
        """
        self.sprite.showturtle()
    def x(self):
        """
        Return the xcor of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
            print(s.x())
        """
        return self.sprite.xcor()
    def y(self):
        """
        Return the ycor of the sprite

        Example:
            s=omiga.Sprite(img="picture.gif")
            print(s.y())
        """
        return self.sprite.ycor()
    
class Physics:
    """
    Physics class is used to simulates physics in life in a window
    """
    def __init__(self,sprite):
        """
        Create a physics model here
        """
        global physics_list
        self.sprite=sprite
        physics_list.append(self.sprite)
        self.gravity_addspeed=0.5
        self.speed=2
        self.friction=2
        self.elastic=0.5
        self.velocitys=[]
        self.temperature=0
        self.p=turtle.Pen()
        self.p.penup()
        self.ms=turtle.Screen()
        self.ms.addshape("light.gif")
        self.ms.tracer(0)
        self.p.shape("light.gif")
        self.p.hideturtle()
        self.foas=False
        self.axis=None
    def step(self):
        """
        Update the physics model

        Example:
            p=omiga.Physics(sprite=s)
        >   p.update()
        """
        global physics_list,airtemperature,wind_angle,wind_velocity
        self.sprite.sprite.sety(self.sprite.y()-self.speed)
        self.speed+=self.gravity_addspeed
        for item in physics_list:
            if self.sprite.is_collision(item) and self.sprite!=item and item.get_attributes("collision")==True:
                self.speed=-abs(self.speed)
                self.speed+=self.friction
                self.times=0
                for item in self.velocitys:
                    item[0]=item[0]+180
                if self.speed>0:
                    self.speed=0
        for item in self.velocitys:
            self.sprite.sprite.setheading(item[0])
            self.sprite.advance(item[1])
            item[1]-=self.friction
            if item[1]<=0:
                self.velocitys.remove(item)
        self.p.goto(self.sprite.x(),self.sprite.y())
        try:
            if self.gravity_addspeed!=0:
                self.sprite.set_angle(wind_angle)
                self.sprite.advance(wind_velocity)
        except:
            pass
    def static(self):
        """
        Set the physics static

        Example:
            p=omiga.Physics(sprite=s)
        >   p.static()
        """
        self.gravity_addspeed=0
        self.speed=0
        self.elastic=0
        self.friction=0
    def dynamic(self):
        """
        Set the physics dynamic

        Example:
            p=omiga.Physics(sprite=s)
        >   p.dynamic()
        """
        self.gravity_addspeed=0.5
        self.speed=2
        self.friction=2
        self.elastic=0.5
    def set_friction(self,friction):
        """
        Set the friction in the air

        Example:
            p=omiga.Physics(sprite=s)
        >   p.set_friction(2)
        """
        self.friction=friction
    def set_velocity(self,angle,velocity):
        """
        Set a velocity for the sprite

        Example:
            p=omiga.Physics(sprite=s)
        >   p.set_velocity(angle=45,velocity=20)
        """
        if self.foas==False:
            self.velocitys.append([angle,velocity])
        else:
            if self.axis=="x":
                self.velocitys.append([0,velocity*math.cos(angle)])
            elif self.axis=="y":
                self.velocitys.append([0,velocity*math.sin(angle)])
    def join_collision(self,boolean):
        """
        Set the physics if join collision with other physics

        Example:
            p=omiga.Physics(sprite=s)
        >   p.join_collision(True)
        """
        self.sprite.set_attributes("collision",boolean)
    def fixed_on_axis(self,boolean,axis=None):
        """
        Let the physics must be on the axis

        Example:
            p=omiga.Physics(sprite=s)
        >   p.fixed_on_axis(True,"x")
        """
        self.foas=boolean
        self.axis=axis

class Interaction:
    """
    Interaction is used to bind the game and the keyboard,mouse
    """
    def __init__(self):
        """
        Create interaction here
        """
        self.ms=turtle.Screen()
        self.ms.listen()
        self.time=0
        self.A="a"
    def on_key_press(self,key,func):
        """
        When press a key then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_key_press(inter.A,move)
        """
        self.ms.onkeypress(func,key)
    def on_key_click(self,key,func):
        """
        When click a key then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_key_click(inter.A,move)
        """
        self.ms.onkey(func,key)
    def on_key_release(self,key,func):
        """
        When release a key then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_key_release(inter.A,move)
        """
        self.ms.onkeyrelease(func,key)
    def on_exit_press(self,func):
        """
        When press the exit button then trigger a function

        Example:
            inter=Interaction()
        >   inter.on_exit_press(Stage.quit)
        """
        self.ms._root.protocol("WM_DELETE_WINDOW",func)
    def on_mouse_press(self,btn,func):
        """
        When press a button then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_mouse_press(inter.LEFT,move)
        """
        self.ms._canvas.bind(f"<Button-{btn}>",func)
    def on_mouse_double_press(self,btn,func):
        """
        When press a button twice then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_mouse_double_press(inter.LEFT,move)
        """
        self.ms._canvas.bind(f"<Double-Button-{btn}>",func)
    def on_mouse_drag(self,btn,func):
        """
        When drag a button then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_mouse_drag(inter.LEFT,move)
        """
        self.ms._canvas.bind(f"<B{btn}-Motion>",func)
    def on_mouse_motion(self,func):
        """
        When mouse motion then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_mouse_motion(move)
        """
        self.ms._canvas.bind("<Motion>",func)
    def on_mouse_leave_stage(self,func):
        """
        When mouse leave the stage then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_mouse_leave_stage(move)
        """
        self.ms._root.bind("<Leave>",func)
    def on_mouse_enter_stage(self,func):
        """
        When mouse enter the stage then trigger a function

        Example:
            sprite=Sprite()
            def move():
                sprite.advance(1)
            inter=Interaction()
        >   inter.on_mouse_enter_stage(move)
        """
        self.ms._root.bind("<Enter>",func)