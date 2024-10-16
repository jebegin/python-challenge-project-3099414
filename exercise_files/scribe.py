import os
import time
from termcolor import colored
import math

# This is the Canvas class. It defines some height and width, and a 
# matrix of characters to keep track of where the TerminalScribes are moving
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the 
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):
        if round(point[0]) < 0 or round(point[0]) >= self._x:
            return 'vertical'
        elif round(point[1]) < 0 or round(point[1]) >= self._y:
            return 'horizontal'
        else:
            return False

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    # Clear the terminal (used to create animation)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

    def getCanvasWidth(self):
        return self._x

class TerminalScribe:
    def __init__(self, canvas, trail = '.', mark = '*', 
    framerate = 0.05, pos = [0, 0], 
    direction = [0, 1], color = 'red'):
        self.canvas = canvas
        self.trail = trail
        self.mark = mark
        self.framerate = framerate
        self.pos = pos
        self.direction = direction
        self.color = color

        self.degrees = 0

    def setPosition(self, pos):
        self.pos = pos

    def setDegrees(self, degrees):
        self.degrees = degrees
        radians = (degrees/180) * math.pi
        self.direction = [math.sin(radians), -math.cos(radians)]

    def forward(self, distance):
        for i in range(distance):
            pos = [self.pos[0] + self.direction[0], 
                self.pos[1] + self.direction[1]]
            hitsWall = self.canvas.hitsWall(pos)
            if hitsWall == 'horizontal':
                self.degrees = 180 - self.degrees
                self.setDegrees(self.degrees)
            elif hitsWall == 'vertical':
                self.degrees = 360 - self.degrees
                self.setDegrees(self.degrees)
            else:
                self.draw(pos)

    def draw(self, pos):
        # Set the old position to the "trail" symbol
        self.canvas.setPos(self.pos, self.trail)
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.setPos(self.pos, colored(self.mark, self.color))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)        


class DirectionScribe(TerminalScribe):
    def up(self):
        self.direction = [0, -1]
        self.forward(1)

    def down(self):
        self.direction = [0, 1]
        self.forward(1)

    def right(self):
        self.direction = [1, 0]
        self.forward(1)

    def left(self):
        self.direction = [-1, 0]
        self.forward(1)


class ShapesScribe(DirectionScribe):
    def drawLineUp(self, size):
        for i in range(size):
            self.up()

    def drawLineDown(self, size):
        for i in range(size):
            self.down()

    def drawLineRight(self, size):
        for i in range(size):
            self.right()

    def drawLineLeft(self, size):
        for i in range(size):
            self.left()

    def drawSquare(self, size):
        self.drawLineRight(size)
        self.drawLineDown(size)
        self.drawLineLeft(size)
        self.drawLineUp(size)


class FuncPlotter(TerminalScribe):
    def plotter(self, func):
        for x in range(canvas.getCanvasWidth()):
            pos = [x, func(x)]
            self.draw(pos)


# Create a new Canvas instance that is 30 units wide by 30 units tall 
canvas = Canvas(40, 40)
'''Available text colors:
        black, red, green, yellow, blue, magenta, cyan, white,
        light_grey, dark_grey, light_red, light_green, light_yellow, light_blue,
        light_magenta, light_cyan.'''

''' Challenge 6
directionScribe = DirectionScribe(canvas, color='green')
directionScribe.setDegrees(135)
directionScribe.forward(0)
directionScribe.down()
directionScribe.down()
directionScribe.down()

squareScribe = ShapesScribe(canvas, color='black', pos = [5, 5])
squareScribe.drawSquare(8)

lineScribe = ShapesScribe(canvas, color = 'white', pos = [6, 7])
lineScribe.drawLineRight(12)
lineScribe.drawLineDown(15)
lineScribe.drawLineRight(7)
lineScribe.drawLineUp(22)

def sine(x):
    return 5*math.sin(x/4) + 15
plotSin = FuncPlotter(canvas, pos = [0, 15], trail = '@')
plotSin.plotter(sine)
'''

''' Challenge 5
import time, math
def timeDescender(x):
    f, w = math.modf(time.time())
    return (int(f * 100)) % 30

scribe = TerminalScribe(canvas)
scribe.plotter(timeDescender)
'''

''' Challenge 4
scribe = TerminalScribe(canvas)
scribe.setDegrees(130)
scribe.forward(200)
'''

''' Challenge 3
scribes = [
    {'degrees': 45, 
     'position': [15, 15], 
     'instructions': [
         {'function': 'forward', 'duration': 5}
      ]
    },
    {'degrees': 135, 
     'position': [5, 10], 
     'instructions': [
         {'function': 'forward', 'duration': 10},
         {'function': 'right', 'duration': 11},
         {'function': 'up', 'duration': 15}
      ]
    }
]

for scribeData in scribes:
    scribeData['scribe'] = TerminalScribe(canvas)
    scribeData['scribe'].setDegrees(scribeData['degrees'])
    scribeData['scribe'].setPosition(scribeData['position'])

for scribeData in scribes:
    for instruction in scribeData['instructions']:
        for i in range(instruction['duration']):
          if instruction['function'] == 'forward':
              scribeData['scribe'].forward()
          if instruction['function'] == 'up':
              scribeData['scribe'].up()
          if instruction['function'] == 'down':
              scribeData['scribe'].down()
          if instruction['function'] == 'left':
              scribeData['scribe'].left()
          if instruction['function'] == 'right':
              scribeData['scribe'].right()
'''

''' Challenge 2
# Create a new scribe and give it the Canvas object
scribe = TerminalScribe(canvas)

# scribe.drawSquare(11)

scribe.setDegrees(135)
for i in range(30):
    scribe.forward()
'''
