from cmath import sqrt
import maya.cmds as mc
from math import pow, sqrt, cos, acos, radians

class SecondaryLocators():

    def __init__(self):
        self.CreateSecLocatorWindow()

    def CreateSecLocatorWindow(self):

        mc.window("Secondary Locators")
        mc.rowColumnLayout(nc = 1)

        #footroll doesn't work with ik setup, will have to go back and check it out at a later date
        # mc.separator(h = 10)
        # mc.button(l = "Create Reverse Footroll", w = 200, c = self.CreateReverseFootroll)

        mc.separator(h = 10)

        self.forearmTwist = mc.intSliderGrp(l = "Forearm Twist Amount", min = 2, max = 10, value = 2, step = 1, field = True)
        mc.button(l = "Create Forearm Twist", w = 200, c = self.ForearmTwist)

        mc.separator(h = 10)

        self.upperarmTwist = mc.intSliderGrp(l = "Upperarm Twist Amount", min = 2, max = 10, value = 2, step = 1, field = True)
        mc.button(l = "Create Upperarm Twist", w = 200, c = self.UpperarmTwist)

        mc.separator(h = 10)

        self.thighTwist = mc.intSliderGrp(l = "Thigh Twist Amount", min = 2, max = 10, value = 2, step = 1, field = True)
        mc.button(l = "Create Thigh Twist", w = 200, c = self.ThighTwist)

        mc.separator(h = 10)

        self.ankleTwist = mc.intSliderGrp(l = "Ankle Twist Amount", min = 2, max = 10, value = 2, step = 1, field = True)
        mc.button(l = "Create Ankle Twist", w = 200, c = self.AnkleTwist)

        mc.separator(h = 10)

        self.CheckGroup(self)
        mc.showWindow()

    def ForearmTwist(self, void):
        amount = mc.intSliderGrp(self.forearmTwist, q = True, v = True)
        self.createForearmTwist(self, amount)

    def UpperarmTwist(self, void):
        amount = mc.intSliderGrp(self.upperarmTwist, q = True, v = True)
        self.createUpperarmTwist(self, amount)

    def ThighTwist(self, void):
        amount = mc.intSliderGrp(self.thighTwist, q = True, v = True)
        self.createThighTwist(self, amount)

    def AnkleTwist(self, void):
        amount = mc.intSliderGrp(self.ankleTwist, q = True, v = True)
        self.createAnkleTwist(self, amount)

    def CheckGroup(self, void):
        if mc.objExists("Secondary_Locators"):
            print ("group exists")
        else:
            mc.group(em = True, n = "Secondary_Locators")

        self.setColors(self)

    def CreateReverseFootroll(self, void):

        #left heel
        mc.select(deselect = True)
        l_reverse_heel = mc.spaceLocator(n = "Locator_L_Inv_Heel")
        mc.scale(.5,.5,.5, l_reverse_heel)

        l_heelPos = mc.xform(mc.ls("Locator_L_Ankle"), q = True, t = True, ws = True)
        mc.move(l_heelPos[0], l_heelPos[1] - 10, l_heelPos[2], l_reverse_heel)
        mc.parent(l_reverse_heel, "Secondary_Locators")

        #right heel
        r_reverse_heel = mc.spaceLocator(n = "Locator_R_Inv_Heel")
        mc.scale(.5,.5,.5, r_reverse_heel)      

        r_heelPos = mc.xform(mc.ls("Locator_R_Ankle"), q = True, t = True, ws = True)
        mc.move(r_heelPos[0], r_heelPos[1] - 9, r_heelPos[2], r_reverse_heel) 
        mc.parent(r_reverse_heel, "Secondary_Locators") 

        #left toes
        l_toePos = mc.xform(mc.ls("Locator_L_Toe_0_0"), q = True, t = True, ws = True)
        l_reverse_toes = mc.spaceLocator(n = "Locator_L_Inv_Toe")
        mc.scale(.5,.5,.5, l_reverse_toes)
        mc.move(15, 0, 15, l_reverse_toes)
        mc.parent(l_reverse_toes, l_reverse_heel)

        mc.select(l_reverse_toes, l_reverse_heel)
        mc.align(atl = True, x = "mid")

        #right toes
        r_reverse_toes = mc.spaceLocator(n = "Locator_R_Inv_Toe")
        mc.scale(.5,.5,.5, r_reverse_toes)
        mc.move(-15, 0, 15, r_reverse_toes)
        mc.parent(r_reverse_toes, r_reverse_heel)

        #left foot base
        l_footBasePos = mc.xform(mc.ls("Locator_L_FootBase"), q = True, t = True, ws = True)
        l_reverse_footBase = mc.spaceLocator(n = "Locator_L_Inv_footBase")
        mc.scale(.5,.5,.5, l_reverse_footBase)
        mc.move(l_footBasePos[0], l_footBasePos[1], l_footBasePos[2], l_reverse_footBase)
        mc.parent(l_reverse_footBase, l_reverse_toes)

        #right foot base
        r_footBasePos = mc.xform(mc.ls("Locator_R_FootBase"), q = True, t = True, ws = True)
        r_reverse_footBase = mc.spaceLocator(n = "Locator_R_Inv_footBase")
        mc.scale(.5,.5,.5, r_reverse_footBase)
        mc.move(r_footBasePos[0], r_footBasePos[1], r_footBasePos[2])
        mc.parent(r_reverse_footBase, r_reverse_toes)

        #left ankles 
        l_anklePos = mc.xform(mc.ls("Locator_L_Ankle"), q = True, t = True, ws = True)
        l_reverse_ankle = mc.spaceLocator(n = "Locator_L_Inv_Ankle")
        mc.scale(.5,.5,.5, l_reverse_heel)
        mc.move(l_anklePos[0], l_anklePos[1], l_anklePos[2], l_reverse_ankle)
        mc.parent(l_reverse_ankle, l_reverse_footBase)

        #right ankles
        r_anklePos = mc.xform(mc.ls("Locator_R_Ankle"), q = True, t = True, ws = True)
        r_reverse_ankle = mc.spaceLocator(n = "Locator_R_Inv_Ankle")
        mc.scale(.5,.5,.5, r_reverse_ankle)
        mc.move(r_anklePos[0], r_anklePos[1], r_anklePos[2], r_reverse_ankle)
        mc.parent(r_reverse_ankle, r_reverse_footBase)

    def createThighTwist(self, void, amount):
        mc.select(deselect = True)

        #Left Thigh Twist
        l_hipPos = mc.xform(mc.ls("Locator_L_Hip"), q = True, t = True, ws = True)
        l_kneePos = mc.xform(mc.ls("Locator_L_Knee"), q = True, t = True, ws = True)

        l_vectorX = l_kneePos[0] - l_hipPos[0]
        l_vectorY = l_kneePos[1] - l_hipPos[1]
        l_vectorZ = l_kneePos[2] - l_hipPos[2]

        for i in range(amount - 1):
            l_thighLocator = mc.spaceLocator(n = "Locator_L_ThighTwist_" + str(i))
            mc.move(l_hipPos[0] + (l_vectorX / amount) + ((l_vectorX / amount) * i), l_hipPos[1] + (l_vectorY / amount) + ((l_vectorY / amount) * i), l_hipPos[2] + (l_vectorZ / amount) + ((l_vectorZ / amount) * i), l_thighLocator)
            mc.scale(.5,.5,.5, l_thighLocator)
            mc.parent(l_thighLocator, "Secondary_Locators")

        #Right Thigh Twist
        r_hipPos = mc.xform(mc.ls("Locator_R_Hip"), q = True, t = True, ws = True)
        r_kneePos = mc.xform(mc.ls("Locator_R_Knee"), q = True, t = True, ws = True)

        r_vectorX = r_kneePos[0] - r_hipPos[0]
        r_vectorY = r_kneePos[1] - r_hipPos[1]
        r_vectorZ = r_kneePos[2] - r_hipPos[2]

        for i in range(amount - 1):
            r_thighLocator = mc.spaceLocator(n = "Locator_R_ThighTwist_" + str(i))
            mc.move(r_hipPos[0] + (r_vectorX / amount) + ((r_vectorX / amount) * i), r_hipPos[1] + (r_vectorY / amount) + ((r_vectorY / amount) * i), r_hipPos[2] + (r_vectorZ / amount) + ((r_vectorZ / amount) * i), r_thighLocator)
            mc.scale(.5,.5,.5, r_thighLocator)
            mc.parent(r_thighLocator, "Secondary_Locators")    

    def createAnkleTwist(self, void, amount):
        mc.select(deselect = True)

        #Left Ankle Twist
        l_kneePos = mc.xform(mc.ls("Locator_L_Knee"), q = True, t = True, ws = True)
        l_anklePos = mc.xform(mc.ls("Locator_L_Ankle"), q = True, t = True, ws = True)

        l_vectorX = l_anklePos[0] - l_kneePos[0]
        l_vectorY = l_anklePos[1] - l_kneePos[1]
        l_vectorZ = l_anklePos[2] - l_kneePos[2]

        for i in range(amount - 1):
            l_ankleLocator = mc.spaceLocator(n = "Locator_L_AnkleTwist_" + str(i))
            mc.move(l_kneePos[0] + (l_vectorX / amount) + ((l_vectorX / amount) * i), l_kneePos[1] + (l_vectorY / amount) + ((l_vectorY / amount) * i), l_kneePos[2] + (l_vectorZ / amount) + ((l_vectorZ / amount) * i), l_ankleLocator)
            mc.scale(.5,.5,.5, l_ankleLocator)
            mc.parent(l_ankleLocator, "Secondary_Locators")

        #Right Thigh Twist
        r_kneePos = mc.xform(mc.ls("Locator_R_Knee"), q = True, t = True, ws = True)
        r_anklePos = mc.xform(mc.ls("Locator_R_Ankle"), q = True, t = True, ws = True)

        r_vectorX = r_anklePos[0] - r_kneePos[0]
        r_vectorY = r_anklePos[1] - r_kneePos[1]
        r_vectorZ = r_anklePos[2] - r_kneePos[2]

        for i in range(amount - 1):
            r_ankleLocator = mc.spaceLocator(n = "Locator_R_AnkleTwist_" + str(i))
            mc.move(r_kneePos[0] + (r_vectorX / amount) + ((r_vectorX / amount) * i), r_kneePos[1] + (r_vectorY / amount) + ((r_vectorY / amount) * i), r_kneePos[2] + (r_vectorZ / amount) + ((r_vectorZ / amount) * i), r_ankleLocator)
            mc.scale(.5,.5,.5, r_ankleLocator)
            mc.parent(r_ankleLocator, "Secondary_Locators")

    def createUpperarmTwist(self, void, amount):
        mc.select(deselect = True)

        #Left Upperarm Twist
        l_upperArmPos = mc.xform(mc.ls("Locator_L_UpperArm"), q = True, t = True, ws = True)
        l_elbowPos = mc.xform(mc.ls("Locator_L_Elbow"), q = True, t = True, ws = True)

        l_vectorX = l_elbowPos[0] - l_upperArmPos[0]
        l_vectorY = l_elbowPos[1] - l_upperArmPos[1]
        l_vectorZ = l_elbowPos[2] - l_upperArmPos[2]

        for i in range(amount - 1):
            l_upperTwistLocator = mc.spaceLocator(n = "Locator_L_UpperArmTwist_" + str(i))
            mc.move(l_upperArmPos[0] + (l_vectorX / amount) + ((l_vectorX / amount) * i), l_upperArmPos[1] + (l_vectorY / amount) + ((l_vectorY / amount) * i), l_upperArmPos[2] + (l_vectorZ / amount) + ((l_vectorZ / amount) * i), l_upperTwistLocator)
            mc.scale(.5,.5,.5, l_upperTwistLocator)
            mc.parent(l_upperTwistLocator, "Secondary_Locators")
        
        #Right Upperarm Twist
        r_upperArmPos = mc.xform(mc.ls("Locator_R_UpperArm"), q = True, t = True, ws = True)
        r_elbowPos = mc.xform(mc.ls("Locator_R_Elbow"), q = True, t = True, ws = True)

        r_vectorX = r_elbowPos[0] - r_upperArmPos[0]
        r_vectorY = r_elbowPos[1] - r_upperArmPos[1]
        r_vectorZ = r_elbowPos[2] - r_upperArmPos[2]

        for i in range(amount - 1):
            r_upperTwistLocator = mc.spaceLocator(n = "Locator_R_UpperArmTwist_" + str(i))
            mc.move(r_upperArmPos[0] + (r_vectorX / amount) + ((r_vectorX / amount) * i), r_upperArmPos[1] + (r_vectorY / amount) + ((r_vectorY / amount) * i), r_upperArmPos[2] + (r_vectorZ / amount) + ((r_vectorZ / amount) * i), r_upperTwistLocator)
            mc.scale(.5,.5,.5, r_upperTwistLocator)
            mc.parent(r_upperTwistLocator, "Secondary_Locators")

    def createForearmTwist(self, void, amount):
        mc.select(deselect = True)

        #Left Forearm Twist
        if(mc.objExists("Locator_L_Elbow")):
            l_elbowPos = mc.xform(mc.ls("Locator_L_Elbow"), q = True, t = True, ws = True)
        else:
            l_elbowPos = mc.xform(mc.ls("Locator_L_Elbow"), q = True, t = True, ws = True)

        l_wristPos = mc.xform(mc.ls("Locator_L_Wrist"), q = True, t = True, ws = True)

        l_vectorX = l_wristPos[0] - l_elbowPos[0]
        l_vectorY = l_wristPos[1] - l_elbowPos[1]
        l_vectorZ = l_wristPos[2] - l_elbowPos[2]

        for i in range(amount - 1):
            l_twistLocator = mc.spaceLocator(n = "Locator_L_ArmTwist_" + str(i))
            mc.move(l_elbowPos[0] + (l_vectorX / amount) + ((l_vectorX / amount) * i), l_elbowPos[1] + (l_vectorY / amount) + ((l_vectorY / amount) * i), l_elbowPos[2] + (l_vectorZ / amount) + ((l_vectorZ / amount) * i), l_twistLocator)
            mc.scale(.5,.5,.5, l_twistLocator)
            mc.parent(l_twistLocator, "Secondary_Locators")

        #Right Forearm Twist
        if(mc.objExists("Locator_R_Elbow")):
            r_elbowPos = mc.xform(mc.ls("Locator_R_Elbow"), q = True, t = True, ws = True)
        else:
            l_elbowPos = mc.xform(mc.ls("Locator_R_Elbow"), q = True, t = True, ws = True) 

        r_wristPos = mc.xform(mc.ls("Locator_R_Wrist"), q = True, t = True, ws = True)

        r_vectorX = r_wristPos[0] - r_elbowPos[0]           
        r_vectorY = r_wristPos[1] - r_elbowPos[1]   
        r_vectorZ = r_wristPos[2] - r_elbowPos[2]   

        for i in range(amount - 1):
            r_twistLocator = mc.spaceLocator(n = "Locator_R_ArmTwist_" + str(i))
            mc.move(r_elbowPos[0] + (r_vectorX / amount) + ((r_vectorX / amount) * i), r_elbowPos[1] + (r_vectorY / amount) + ((r_vectorY / amount) * i), r_elbowPos[2] + (r_vectorZ / amount) + ((r_vectorZ / amount) * i), r_twistLocator)
            mc.scale(.5,.5,.5, r_twistLocator)
            mc.parent(r_twistLocator, "Secondary_Locators")

    def setColors(self, void):
        mc.setAttr("Secondary_Locators.overrideEnabled", 1) #sets override enabled in the attribute editor so that the color of the locators can be changed
        mc.setAttr("Secondary_Locators.overrideColor", 18) #changes the color of the locators so they stand out more in the project

    def deleteSecondary(self, void):
        mc.delete(mc.ls("Secondary_Locators"))





