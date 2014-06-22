
# Copyright - Abhishek Trigunayat

import Myro
from Myro import *
from Graphics import *
import math

width, height = 700, 700
currentX = 310
currentY = 270
sim = Simulation("Parking Structure", width, height, Color("white"))

#function to set up the world for model based agent
def modelWorldSetUp():
    print("Enter the sequence of three colors you \nwant to paint the walls with \nin anticlockwise direction starting \nwith the north wall");
    count = 0
    inputColor = []
    while (count < 3):
        inputColor.append(raw_input("Enter the color "));
        count = count + 1
    sim.addWall((250,150),(500,160), Color(inputColor[0]))
    sim.addWall((250,160),(260,360), Color(inputColor[1]))
    sim.addWall((260,350),(500,360), Color(inputColor[2]))
    print("The list of colors entered by you is : ",inputColor)

#function to set up the world for goal based agent
def goalWorldSetUp():
    print("Enter the sequence of colors \nyou want to paint the walls with")
    count = 0
    inputColor = []
    while (count < 3):
        inputColor.append(raw_input("Enter the color : "));
        count = count + 1

    sim.addWall((50,50),(55,150), Color(inputColor[0]))
    sim.addWall((50,200),(55,300), Color(inputColor[1]))
    sim.addWall((50,350),(55,450), Color(inputColor[2]))

class Agent(object):
    def act(self, pic):
        return False

# Agent 1: Model-based
#
# Explanation:
# In this scenario, the user is asked to enter the sequence of three colors he/she wants to paint
# the walls of the room with. The agent will then scan each wall with a camera sensor and
# decides towards which direction it has to exit the room depending on the color of the walls.
# The room will have three walls, each with a different color, and one exit towards east.
# In order to decide where to exit from it will follow the below rule:
# If the north wall is blue then it will exit the room from east and then move
# towards north.
# If the west wall is blue then it will exit the room from east and then move straight
# If the south wall is blue then it will exit the room from east and then move
# towards south.

# Assumptions:
# The user cannot paint two or more walls of the room with the blue color.
# Colors only out of the following can be used as input: red, green, blue, black, yellow

class ModelBasedAgent(Agent):
    def act(self):
        flag = 0
        count = 0
        perceptSequence = []
        print("Robot is detecting the colors of the wall");

        #Setting the percept sequence fom sensor input
        while(count<3):
            robot.turnBy(90,"deg")
            pic = takePicture()
            show(pic)
            pixel = getPixel(pic, getWidth(pic)/2, getHeight(pic)/2)
            if(getRed(pixel) !=0 and getBlue(pixel) == 0 and getGreen(pixel) == 0):
                colorName = "red"
            elif (getBlue(pixel) !=0 and getRed(pixel) == 0 and getGreen(pixel) == 0):
                colorName = "blue"
            elif (getGreen(pixel) !=0 and getRed(pixel) == 0 and getBlue(pixel) == 0):
                colorName = "green"
            elif(getRed(pixel) == 0 and getGreen(pixel) == 0 and getBlue(pixel) == 0):
                colorName = "black"
            elif (getBlue(pixel) == 0 and getRed(pixel) != 0 and getGreen(pixel) != 0):
                colorName = "yellow"
            perceptSequence.append(colorName)
            count = count +1
        robot.turnBy(90,"deg")
        action = []

        #Taking action depending on percept sequence
        if(perceptSequence[0] == "blue"):
            action.append(90)
            print("The robot will exit the room towards south!!")
        elif(perceptSequence[1] == "blue"):
            action.append(0)
            print("The robot will exit the room straight!!")
        elif(perceptSequence[2] == "blue"):
            action.append(270);
            print("The robot will exit the room towards north!!")
        else:
            print("Blue colored wall is not present, the robot will do nothing")
            flag = 1
        if(flag != 1):
            robot.forward(1,7)
            for index in action:
                robot.turnBy(index,"deg")
            robot.forward(1,2)

# Agent 2: Goal-based
#
# Explanation:
# In this scenario, the user is asked to enter three colors to paint three different walls with
# and a goal color. The robot will then scan each wall and look for the goal color.
# If the goal color is found on any wall then the robot will stop and announce it,
# else it would continue checking.

# Assumption:
# Colors only out of these can be used as input: red, green, blue, black, yellow

class GoalBasedAgent(Agent):
    def act(self):

        #Accepting the goal color from user
        print("Enter the color of the goal wall ")
        goalColor = raw_input();
        robot.turnBy(270,"deg")
        robot.forward(2,1.8)
        robot.turnBy(270,"deg")
        robot.forward(1,5)
        print("Scanning for goal color ")
        colorName = 0
        count = 0
        found = 0

        #Checking for goal color
        while(count < 2):
            pic = takePicture()
            show(pic)
            pixel = getPixel(pic, getWidth(pic)/2, getHeight(pic)/2)
            if(getRed(pixel) == 0 and getGreen(pixel) == 0 and getBlue(pixel) == 0):
                colorName = "black"
            elif (getBlue(pixel) == 0 and getRed(pixel) != 0 and getGreen(pixel) != 0):
                colorName = "yellow"
            elif (getGreen(pixel) != 0 and getRed(pixel) == 0 and getBlue(pixel) == 0):
                colorName = "green"
            elif(getRed(pixel) != 0 and getBlue(pixel) == 0 and getGreen(pixel) == 0):
                colorName = "red"
            elif (getBlue(pixel) != 0 and getRed(pixel) == 0 and getGreen(pixel) == 0):
                colorName = "blue"
            if(colorName == goalColor):
                print("Goal color found!!")
                found = 1
                count = 5
            else :
                robot.turnBy(270,"deg")
                robot.forward(1.2,3)
                robot.turnBy(90,"deg")
                count = count + 1
        if(found != 1):
            print("Goal color not found!!")



# Agent 3: Utility-based
# In this scenario the user is asked to enter two conflicting goals in form of co-ordinates.
# The robot will then use a utility function to decide which is a better goal and then
# navigate towards it. The utility function will use the distance from the robot to the goal
# as a criteria for choosing a better goal.

# Assumption
# The robot is able to know its currect location co-ordinates
# Each input goal co-ordinate should be less than 700 which is the max limit of the simulation boundaries

class UtilityBasedAgent(Agent):
    def utilityFunction(self,goalOne,goalTwo):
        distanceToOne = 0
        distanceToTwo = 0
        distanceToOne = math.sqrt(math.pow((goalOne[0] - currentX),2)+math.pow((goalOne[1] - currentY),2))
        distanceToTwo = math.sqrt(math.pow((goalTwo[0] - currentX),2)+math.pow((goalTwo[1] - currentY),2))
        print("Distance to one is : ",distanceToOne)
        print("Distance to two is : ",distanceToTwo)
        if(distanceToOne > distanceToTwo):
            return "Two"
        elif(distanceToOne < distanceToTwo):
            return "One"

    def act(self):
        goalOne = []
        goalTwo = []
        goal = []

        #Accepting two goals from the user
        print("Enter Goal 1 coordinates (will be denoted in red)")
        goalOne.append(int(raw_input("Enter X coordinate")))
        goalOne.append(int(raw_input("Enter Y coordinate")))
        print("Enter Goal 2 coordinates (will be denoted in green)")
        goalTwo.append(int(raw_input("Enter X coordinate")))
        goalTwo.append(int(raw_input("Enter Y coordinate")))
        sim.addWall((goalOne[0],goalOne[1]),(goalOne[0]+5,goalOne[1]+5), Color("red"))
        sim.addWall((goalTwo[0],goalTwo[1]),(goalTwo[0]+5,goalTwo[1]+5), Color("green"))

        #Getting the nearest goal for the robot using a utility function
        result = self.utilityFunction(goalOne,goalTwo)
        if(result == "One"):
            goal = goalOne
        elif(result == "Two"):
            goal = goalTwo
        print("The nearest goal is : ",result),

        #Navigating to the nearest goal
        targetX = goal[0]
        targetY = goal[1]
        toMoveX = 0
        toMoveY = 0
        if (targetX > currentX and targetY > currentY):
            toMoveX = targetX - currentX
            toMoveY = targetY - currentY
            rotateForX = 270
            rotateForY = 90
        elif (targetX < currentX and targetY > currentY):
            toMoveX = currentX - targetX
            toMoveY = targetY - currentY
            rotateForX = 90
            rotateForY = 90
        elif (targetX > currentX and targetY < currentY):
            toMoveX = targetX - currentX
            toMoveY = currentY - targetY
            rotateForX = 90
            rotateForY = 270
        elif (targetX < currentX and targetY < currentY):
            toMoveX = currentX - targetX
            toMoveY = currentY - targetY
            rotateForX = 270
            rotateForY = 270

        print("X distance to move : ", toMoveX)
        print("Y distance to move : ", toMoveY)

        robot.turnBy(rotateForY,"deg")
        count = 0
        while(count != toMoveY):
            robot.forward(0.1,0.2)
            count = count + 1

        robot.turnBy(rotateForX,"deg")
        count = 0
        while(count != toMoveX):
            robot.forward(0.1,0.2)
            count = count + 1



print("Enter the type of agent you want to Simulate : \n1.Model \n2.Goal \n3.Utility")
sim.setup()
robot = makeRobot("SimScribbler", sim)
userChoice = int(raw_input())
if(userChoice == 1):
    modelWorldSetUp()
    agent = ModelBasedAgent()
    pic = takePicture()
    show(pic)
elif(userChoice == 2):
    goalWorldSetUp()
    agent = GoalBasedAgent()
    pic = takePicture()
    show(pic)
elif(userChoice == 3):
    agent = UtilityBasedAgent()

agent.act()

