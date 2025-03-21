#1242 demo on basic .Net startup with Drawer (+threading, +timers)
import random
import threading
from time import *
import clr
import pythonnet

clr.AddReference ('GDIDrawer') # drawer already uses drawing, but we could add reference too
clr.AddReference ('System.Drawing') # somewhat redundant, but shows additional reference
#clr.AddReference ('System.LINQ') # somewhat redundant, but shows additional reference
#clr.AddReference ('System.Windows.Forms') # somewhat redundant, but shows additional reference
from System.Drawing import Color, Point # make common types available
from GDIDrawer import * #make everything for drawer available (drawer, randcolor, ...)
from System.Windows.Forms import ColorDialog

# demo for introductory .NET bits in python

# globals
# this is used to have any threads/timers exit
ThreadRun = True

# pick a random coordinate
def get_random_coordinate (width, height):
    return random.randrange (0, width), random.randrange(0, height)
# def get_random_coordinate (width, height):


# left-click handler running in the drawer thread
def canvas_left_click (pos, sender):
    global ThreadRun

    # show where user clicked
    canvas.AddCenteredEllipse (pos, 5, 10, RandColor.GetColor())
    canvas.Render()

    # have thread/timer die next pass
    ThreadRun = False
# def canvas_left_click (pos, sender):


# function body for self-prop timer
def timer_callback():
    w, h = get_random_coordinate(800, 600)
    canvas.AddCenteredRectangle(w, h, 50, 50, RandColor.GetColor())
    canvas.Render()

    # only prop another timer if we are still running
    if ThreadRun:
        tim = threading.Timer (1.2, timer_callback)
        tim.start()
# def timer_callback():


# function as thread body
def ThreadDraw (**kwargs):

    # fall out if we have been asked to leave
    while ThreadRun:
        w, h = get_random_coordinate(800, 600)
        kwargs['can'].AddCenteredEllipse (w, h, 50, 50, RandColor.GetColor())
        kwargs['can'].Render()

        # all daemon threads should have some form of throttle if they run in a loop!
        sleep(kwargs['delay'])
# def ThreadDraw (**kwargs):


if __name__ == "__main__":
    #print (pythonnet.get_runtime_info())

    # create a drawer - note, no new, and no help from popups
    canvas = CDrawer (800, 600, False)

    # not useful, but shows that .NET forms items can be used
    dlg = ColorDialog()
    dlg.Color = Color.Red
    dlg.FullOpen = True
    dlg.ShowDialog()
    canvas.BBColour = dlg.Color

    # subscribe to a drawer event
    canvas.MouseLeftClickScaled += canvas_left_click

    # create a thread to draw shapes (ellipse in this case)
    # note useful capacity to parameterize the thread!
    thrDraw = threading.Thread (target=ThreadDraw, daemon=True, kwargs = {'can':canvas, 'delay':0.2})

    # start the thread
    thrDraw.start()

    # start self-propagating timer
    timer_callback()

    # wait for thread to exit
    thrDraw.join()

    # we are actually always to do this, in C# too
    canvas.Close()