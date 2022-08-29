#Xavier Rodriguez
#Locator Script

import maya.cmds as mc

#used to lock the controls later on in the script (see "def lockLocators" for ref)
editMode = True

#Defining Tool Functions#

def separators():
    mc.separator(h = 10, w = 150, st = "none")
    mc.separator(h = 10, w = 150, st = "none")
    mc.separator(h = 10, w = 150, st = "none")

#spine, finger, toe, neck, and pose ui code here since the integer code for each is integral to the locator code
def createFields():
    
    #spine count UI
    #set how many spine joints get created for the event "create controls"
    mc.separator(w = 150, st = "none")
    mc.text("Spine Count", l = "Spine Count (max:10)", w = 150) #adds a label to the Spine Count int field
    mc.separator(st = "none", w = 150)  

    separators()

    global spineCount #I think this allows the variable to be referenced by other files

    mc.separator(w = 150, st = "none")
    spineCount = mc.intField(minValue = 1, maxValue = 10, value = 3, w = 150) #allows user to set the amount of spine Locators up to a max value of 10
    mc.separator(w = 150, st = "none")

    separators()

    #finger count UI
    #set how many fingers get created for the event "create controls"
    mc.separator(w = 150, st = "none")
    mc.text("Finger Count", l = "Finger Count (max:10)", w = 150) #adds a label to the Finger Count int field
    mc.separator(w = 150, st = "none")

    separators()

    global fingerCount #I think this allows the variable to be referenced by other files

    mc.separator(w = 150, st = "none")
    fingerCount = mc.intField(minValue = 1, maxValue = 10, value = 5, w = 150,) #allows user to set the amount of finger Locators up to a max value of 10
    mc.separator(w = 150, st = "none")

    separators()

    #toe count UI
    #set how many toe joints get created for the event "create controls"
    mc.separator(w = 150, st = "none")
    mc.text("Toe Count", l = "Toe Count (max:10)", w = 150)
    mc.separator(w = 150, st = "none")

    separators()

    global toeCount

    mc.separator(w = 150, st = "none")
    toeCount = mc.intField(minValue = 1, maxValue = 5, value = 1, w = 150,)
    mc.separator(w = 150, st = "none")

    separators()

    #neck count UI
    #set how many neck joints get created for the event "create controls"
    mc.separator(w = 150, st = "none")
    mc.text("Neck Count", l = "Neck Count (max:10)", w = 150)
    mc.separator(w = 150, st = "none")

    separators()

    global neckCount

    mc.separator(w = 150, st = "none")
    neckCount = mc.intField(minValue = 1, maxValue = 10, value = 2, w = 150)
    mc.separator(w = 150, st = "none")

    separators()

    #Pose UI
    #user can select whether they generate their rig in an a-pose or a t-pose
    mc.text("Pose", l = "Pose", w = 150,)
    global poseChoice
    poseChoice = mc.radioCollection("poseCollection")
    mc.radioButton("A_Pose", l = "A Pose", w = 150,)
    mc.radioButton("T_Pose", l = "T Pose", w = 150,)

def createLocators():
    
    #ensures that user must have a pose selected in order to create locators
    poseSelection = mc.radioCollection("poseCollection", q = True, sl = True) 
    if poseSelection != "A_Pose" and poseSelection != "T_Pose":
        mc.confirmDialog(title = "No Pose Selected", message = "Please Select Pose To Create Locators", button = "OK")
        return

    if mc.objExists("Locator_Mast"): #check to see if a locator rig already exists
        mc.confirmDialog(title = "Master Locator Already Exists", message = "Locator Group already exists", button = "OK")
        return
    else:
        mc.group(em = True, name = "Locator_Mast") #creates Maya group for Locators

        #placing this code in the else statement to ensure users can't create a new locator while one is already in the world
        root = mc.spaceLocator(n = "Locator_Root") #creates root Locator (just realized the root doesn't need a Locator. oops)
        mc.scale(2.0, 2.0, 2.0, root) #Locators were a bit too small in the editor
        mc.parent(root, "Locator_Mast") #parents the Locator hierarchy to the Master group
    
        pelvis = mc.spaceLocator(n = "Locator_Pelvis") #creates the pelvis Locator
        mc.scale(2.0,2.0,2.0, pelvis) 
        mc.move(0,95,0, pelvis)
        mc.parent(pelvis, "Locator_Root") #parents the spine to the root Locator

        #runs the createSpine function which creates the spine hierarchy for the locators
        createSpine() 

def createSpine():
    for i in range(0, mc.intField(spineCount, query = True, value = True)): #sets i value based off of int field selection for variable "spineCount"
        spine = mc.spaceLocator(n = "Locator_Spine_" + str(i)) #generates spine Locators based off of i value and gives them the proper naming conventions
        spineHeight = int(45) #used as a clamp value to determine the height we want the spine to stay in regardless of spine count
        mc.scale(2.0,2.0,2.0, spine)   
        if i == 0:
            mc.parent(spine, "Locator_Pelvis") #parents the first spine Locator to the root
        else:
            mc.parent(spine, "Locator_Spine_" + str(i-1)) #parents each subsequence spine to the previous spine locator to follow standard hierarchy
 
        mc.move(0, 95 + (spineHeight/mc.intField(spineCount, query = True, value = True)) * (i+1), 0, spine) #moves spine locators evenly to prevent overlap. uses spine height to be clamp height to a set value    
        #mc.move(0, 112 + (22 * i), 0, spine) #moves spine locators evenly to prevent overlap 

    createHead() #generates head and neck
    createLegs(1) #generates the left leg
    createLegs(-1) #generates the right leg
    createArms(1) #generates the left arm
    createArms(-1) #generates the right arm

    setColor() #alters the colors of the locators to be easier to see against the background

def createHead():

    spinePos = mc.xform("Locator_Spine_" + str(mc.intField(spineCount, query = True, value = True) - 1), q = True, t = True, ws = True) #grabs the spine position for the neck to have height ref

    #neck base
    neckBase = mc.spaceLocator(n = "Locator_NeckBase") #create the neck base locator itself
    neckBaseScale = mc.scale(2,2,2, neckBase)
    mc.parent(neckBase, "Locator_Spine_" + str(mc.intField(spineCount, query = True, value = True) - 1)) #parents the neck base to spine
    moveNeckBase = mc.move(0.0, 17.0 + spinePos[1], 0.0, neckBase) #moves neck locators evenly to prevent overlap. uses neck height to be clamp height to a set value    

    #remaining neck locators
    for i in range(0, mc.intField(neckCount, query = True, value = True)): #for loop to generate neck locators based off of the neck count
        neckBones = mc.spaceLocator(n = "Locator_Neck_" + str(i)) #creates the locator for the remaining neck bones 
        neckHeight = float(10) #used as a clamp value to determine the height we want the neck to stay in regardless of neck count
        mc.scale(2,2,2, neckBones)

        if i == 0:
            moveNeckJoints = mc.move(0.0, 157 + (neckHeight/mc.intField(neckCount, query = True, value = True) * (i+1)), 0.0, neckBones) #moves neck locators evenly to prevent overlap. uses neck height to be clamp height to a set value            
            mc.parent(neckBones, neckBase) #parents neck to the spine based off the int value users set up in the int field

        else:
            moveNeckJoints = mc.move(0.0, 157 + (neckHeight/mc.intField(neckCount, query = True, value = True) * (i+1)), 0.0, neckBones) #moves neck locators evenly to prevent overlap. uses neck height to be clamp height to a set value
            mc.parent(neckBones, "Locator_Neck_" + str(i - 1)) #parents neck to the spine based off the int value users set up in the int field               

    #head 
    head = mc.spaceLocator(n = "Locator_Head")
    mc.parent(head, "Locator_Neck_" + str(mc.intField(neckCount, query = True, value = True) - 1)) #parents the head to the latest neck locator
    mc.scale(1,1,1, head)
    mc.move(0, 172, 5, head) #moves head locator based off the neck pos established in earlier

#using the same foundation as the arm code, creates and places leg locators in the world and parents them to the pelvis
def createLegs(side): #side parameter is used to determine which leg (left or right) to spawn when using the createLegs function in another part of the code
    if side == 1: #Left Leg
        if mc.objExists("L_Leg_Grp"):
            print ("left leg already exists") #make into a window at a later point
        else:
            Left_Leg = mc.group(em = True, name = "L_Leg_Grp") #creates grouping for the left leg
            mc.parent(Left_Leg, "Locator_Pelvis")
            mc.move(10, 90, 0, Left_Leg)

        #Left Hip
        Left_Hip = mc.spaceLocator(n = "Locator_L_Hip")
        mc.scale(2,2,2, Left_Hip)
        mc.move(15, 90, 0, Left_Hip)
        mc.parent(Left_Hip, Left_Leg)

        #Left Knee
        Left_Knee = mc.spaceLocator(n = "Locator_L_Knee")
        mc.scale(2,2,2, Left_Knee)
        mc.move(15, 50, 0, Left_Knee)
        mc.parent(Left_Knee, Left_Hip)

        #Left Foot
        Left_Foot = mc.spaceLocator(n = "Locator_L_Ankle") #I accidentally named it foot in all the variables so apologies to future me for any issues that causes
        mc.scale(2,2,2, Left_Foot)
        mc.move(15,10,-5, Left_Foot)
        mc.parent(Left_Foot, Left_Knee)

        #Left Foot Base
        Left_Foot_Base = mc.spaceLocator(n = "Locator_L_FootBase")
        mc.scale(2,2,2, Left_Foot_Base)
        mc.move(15,0,10, Left_Foot_Base)
        mc.parent(Left_Foot_Base, Left_Foot)

        pos = mc.xform(Left_Foot_Base, q = True, t = True, ws = True) #used as location ref for creating the toes

        #Left foot toes
        for i in range(0, mc.intField(toeCount, query = True, value = True)): #for loop using toe int field to determine range
            createToes(1, pos, i) #generates Toes and positions them using the foot base as ref

        #realigning toes based on foot base position
        mc.select("L_Foot_Grp", "Locator_L_FootBase") #the whole group is selected since if the individual toes are chosen then they will overlap one another which we don't want
        mc.align(atl = True, x = 'mid') #the toes are then aligned to the foot base through the hand group

        mc.parent("L_Foot_Grp", "Locator_L_FootBase") #parenting for the toes to the foot base is done after each are created to ensure that the hand realignment done in "createToes" works properly. 

    else:
        if mc.objExists("R_Leg_Grp"):
            print ("right leg already exists") #make into a window at a later point
        else:
            Right_Leg = mc.group(em = True, name = "R_Leg_Grp")
            mc.parent(Right_Leg, "Locator_Pelvis")
            mc.move(-10, 90, 0, Right_Leg)

        #Right hip
        Right_Hip = mc.spaceLocator(n = "Locator_R_Hip")
        mc.scale(2,2,2, Right_Hip)
        mc.move(-15, 90, 0, Right_Hip)
        mc.parent(Right_Hip, Right_Leg)

        #Right knee
        Right_Knee = mc.spaceLocator(n = "Locator_R_Knee")
        mc.scale(2,2,2, Right_Knee)
        mc.move(-15, 50, 0, Right_Knee)
        mc.parent(Right_Knee, Right_Hip)

        #Right foot
        Right_Foot = mc.spaceLocator(n = "Locator_R_Ankle") #I accidentally named it foot in all the variables so apologies to future me for any issues that causes
        mc.scale(2,2,2, Right_Foot)
        mc.move(-15,10,-5, Right_Foot)
        mc.parent(Right_Foot, Right_Knee)

        #Right foot base
        Right_Foot_Base = mc.spaceLocator(n = "Locator_R_FootBase")
        mc.scale(2,2,2, Right_Foot_Base)
        mc.move(-15,0,10, Right_Foot_Base)
        mc.parent(Right_Foot_Base, Right_Foot)

        pos = mc.xform(Right_Foot_Base, q = True, t = True, ws = True)

        #Right foot toes
        for i in range(0, mc.intField(toeCount, query = True, value = True)): #for loop using toe int field to determine range
            createToes(-1, pos, i) #generates Toes and positions them using the foot base as ref

        #realigning toes based on foot base position
        mc.select("R_Foot_Grp", "Locator_R_FootBase") #the whole group is selected since if the individual toes are chosen then they will overlap one another which we don't want
        mc.align(atl = True, x = 'mid') #the toes are then aligned to the foot base through the hand group

        mc.parent("R_Foot_Grp", "Locator_R_FootBase") #parenting for the toes to the foot base is done after each are created to ensure that the hand realignment done in "createToes" works properly. 

def createToes(side, footPos, count): #side determines l or r, footpos is used for world position, count is used for number of toes
    for x in range(0,1):
        if side == 1: #left toes
            #group created to realign toes to the center of the foot
            if mc.objExists("L_Foot_Grp"):
                print (5*8*12) #proxy line, just here to fill space
            else:
                Left_Foot_Grp = mc.group(em = True, name = "L_Foot_Grp")
                mc.move(footPos[0], footPos[1], footPos[2], Left_Foot_Grp)

            toeLeft = mc.spaceLocator(n = "Locator_L_Toe_" + str(count) + "_" + str(x))
            mc.scale(1,1,1, toeLeft)
            if x == 0:
                mc.parent(toeLeft, "L_Foot_Grp")
            else:
                mc.parent(toeLeft, "Locator_L_Toe_" + str(count) + "_" + str(x-1))
            mc.move(footPos[0] +(2 * count), footPos[1], footPos[2] + (5+(5*x)), toeLeft)

        else: #right toes
            #group created to realign toes to the center of the foot
            if mc.objExists("R_Foot_Grp"):
                print (5*8*12) #proxy line, just here to fill space
            else:
                Right_Foot_Grp = mc.group(em = True, name = "R_Foot_Grp")
                mc.move(footPos[0], footPos[1], footPos[2], Right_Foot_Grp)

            toeRight = mc.spaceLocator(n = "Locator_R_Toe_" +str(count) + "_" + str(x))
            mc.scale(1,1,1, toeRight)
            if x == 0:
                mc.parent(toeRight, "R_Foot_Grp")
            else:
                mc.parent(toeRight, "Locator_R_Toe_" + str(count) + "_" + str(x-1))
            mc.move(footPos[0] + -(2 * count), footPos[1], footPos[2] + (5+(5*x)), toeRight)

#creates and places arm locators in the world and parents them to the spine
def createArms(side):

    poseSelection = mc.radioCollection("poseCollection", q = True, sl = True) #stores the pose value from user's selection on the pose choice

    if side == 1: #Left Arm
        if mc.objExists("L_Arm_Grp"):
            print (5*8*12) #proxy line, just here to fill space
        else:
            Left_Arm = mc.group(em = True, name = "L_Arm_Grp") #creates grouping for the left arm
            mc.parent(Left_Arm, "Locator_Spine_" + str(mc.intField(spineCount, query = True, value = True) - 1))

            #Left Clavicle 
            LeftClavicle = mc.spaceLocator(n = "Locator_L_Clavicle")
            mc.scale(2,2,2, LeftClavicle)
            mc.parent(LeftClavicle, Left_Arm)
            SpinePos = mc.xform("Locator_Spine_" + str(mc.intField(spineCount, query = True, value = True) - 1), q = True, t = True, ws = True) #grabbing the position of the spine for the left clavicle

            #Left Upper Arm
            UpperLeftArm = mc.spaceLocator(n = "Locator_L_UpperArm")
            mc.scale(2.0, 2.0, 2.0, UpperLeftArm)
            mc.parent(UpperLeftArm, LeftClavicle)

            #Left Elbow
            LeftElbow = mc.spaceLocator(n = "Locator_L_Elbow")
            mc.scale(2.0, 2.0, 2.0, LeftElbow)
            mc.parent(LeftElbow, UpperLeftArm)

            #Left Wrist
            LeftWrist = mc.spaceLocator(n = "Locator_L_Wrist")
            mc.scale(2.0, 2.0, 2.0, LeftWrist)
            mc.parent(LeftWrist, LeftElbow)

            if poseSelection == "A_Pose": #condition to determine the placement of the arm locators in a pose

                #Move Left Clavicle
                mc.move(5 * side, SpinePos[1] + 15, 0, LeftClavicle)

                #Move Left Upper Arm
                mc.move(15 * side, SpinePos[1] + 10, -10, UpperLeftArm)
                #90 + (22* mc.intField(spineCount, query = True, value = True))

                #Move Left Elbow
                mc.move(35 * side, 130, -15, LeftElbow)

                #Move Left Wrist
                mc.move(55 * side, 110, -10, LeftWrist)

            else: #condition to determine the placement of the arm locators in t pose

                #Move Left Clavicle
                mc.move(5 * side, SpinePos[1] + 15, 0, LeftClavicle)

                #Move Left Upper Arm
                mc.move(15 * side, SpinePos[1] + 15, 0, UpperLeftArm)

                #Move Left Elbow
                mc.move(50 * side, SpinePos[1] + 15, 0, LeftElbow)

                #Move Left Wrist
                mc.move(75 * side, SpinePos[1] + 15, 1, LeftWrist)

            createHands(1, LeftWrist)

            #realigning fingers based on wrist position
            mc.select("L_Hand_Grp", "Locator_L_Wrist") #the whole group is selected since if the individual fingers are chosen then they will overlap one another which we don't want
            mc.align(atl = True, z = 'mid') #the fingers are then aligned to the wrist through the hand group

            mc.parent("L_Hand_Grp", "Locator_L_Wrist") #parenting for the fingers to the wrist is done after each are created to ensure that the hand realignment done in "createFingers" works properly. 

    else: #right arm
        if mc.objExists("R_Arm_Grp"):
            print (25*40)
        else: 
            Right_Arm = mc.group(em = True, n = "R_Arm_Grp")
            mc.parent(Right_Arm, "Locator_Spine_" + str(mc.intField(spineCount, query = True, value = True) - 1))

            #Right Clavicle 
            RightClavicle = mc.spaceLocator(n = "Locator_R_Clavicle")
            mc.scale(2,2,2, RightClavicle)
            mc.parent(RightClavicle, Right_Arm)
            SpinePos = mc.xform("Locator_Spine_" + str(mc.intField(spineCount, query = True, value = True) - 1), q = True, t = True, ws = True) #grabbing the position of the spine for the right clavicle

            #Right Upper Arm
            UpperRightArm = mc.spaceLocator(n = "Locator_R_UpperArm")
            mc.scale(2.0, 2.0, 2.0, UpperRightArm)
            mc.parent(UpperRightArm, RightClavicle)

            #Right Elbow
            RightElbow = mc.spaceLocator(n = "Locator_R_Elbow")
            mc.scale(2.0, 2.0, 2.0, RightElbow)
            mc.parent(RightElbow, UpperRightArm)

            #Right Wrist
            RightWrist = mc.spaceLocator(n = "Locator_R_Wrist")
            mc.scale(2.0, 2.0, 2.0, RightWrist)
            mc.parent(RightWrist, RightElbow)

            if poseSelection == "A_Pose": #condition to determine the placement of the arm locators in a pose

                #Move Right Clavicle
                mc.move(5 * side, SpinePos[1] + 15, 0, RightClavicle)

                #Move Right Upper Arm
                mc.move(15 * side, SpinePos[1] + 10, -10, UpperRightArm)

                #Move Right Elbow
                mc.move(35 * side, 130, -15, RightElbow)

                #Move Right Wrist
                mc.move(55 * side, 110, -10, RightWrist)
            
            else: #condition to determine the placement of the arm locators in t pose

                #Move Right Clavicle
                mc.move(5 * side, SpinePos[1] + 15, 0, RightClavicle)

                #Move Right Upper Arm
                mc.move(15 * side, SpinePos[1] + 15, 0, UpperRightArm)

                #Move Right Elbow
                mc.move(50 * side, SpinePos[1] + 15, 0, RightElbow)

                #Move Right Wrist
                mc.move(75 * side, SpinePos[1] + 15, 1, RightWrist)

            createHands(-1, RightWrist)

            #realigning fingers based on wrist position
            mc.select("R_Hand_Grp", "Locator_R_Wrist") #the whole group is selected since if the individual fingers are chosen then they will overlap one another which we don't want
            mc.align(atl = True, z = 'mid') #the fingers are then aligned to the wrist through the hand group

            mc.parent("R_Hand_Grp", "Locator_R_Wrist") #parenting for the fingers to the wrist is done after each are created to ensure that the hand realignment done in "createFingers" works properly. 

def createHands(side, wrist): #side and wrist parameter to determine l or r hand in "create arms"
    if side == 1: #left hand
        if mc.objExists("L_Hand_Grp"):
            print ("Left Hand already exists")
        else:
            Left_Hand = mc.group(em = True, name = "L_Hand_Grp") #creates group for the left hand if one doesn't already exists
            pos = mc.xform(wrist, q = True, t = True, ws = True) #converts wrist position into a variable for the hand
            mc.move(pos[0], pos[1], pos[2], Left_Hand) #moves hand based on the world position of the wrist
            #mc.parent(Left_Hand, "Locator_L_Wrist") #parents the left hand variable to the left hand group

            for i in range(0, mc.intField(fingerCount, query = True, value = True)): #creates finger locators based off of int field established in the ui
                createFingers(1, pos, i)

    else: #right hand
        if mc.objExists("R_Hand_Grp"):
            print ("Right Hand already exists")
        else:
            Right_Hand = mc.group(em = True, name = "R_Hand_Grp")
            pos = mc.xform(wrist, q = True, t = True, ws = True)
            mc.move(pos[0], pos[1], pos[2], Right_Hand)
            #mc.parent(Right_Hand, "Locator_R_Wrist")           

            for i in range(0, mc.intField(fingerCount, query = True, value = True)):
                createFingers(-1, pos, i)

def createFingers(side, handPos, count): #side determines l or r, handpos is used for world position, count is used for number of fingers
    #poseSelection is a duplicated variable from createArms because the radio buttons are established in a definition and thus I can't make a reusable global function
    poseSelection = mc.radioCollection("poseCollection", q = True, sl = True) #stores the pose value from user's selection on the pose choice
    
    for x in range(0,3):
        if side == 1: #left side fingers
            Left_Finger = mc.spaceLocator(n = "Locator_L_Finger_" + str(count) + "_" + str(x)) #creates left finger locators
            mc.scale(2,2,2, Left_Finger) #sets left finger locator scale
            if x == 0: #parents first finger joint to the wrist, else parents it to the previous finger joint
                mc.parent(Left_Finger, "L_Hand_Grp")
            else:
                mc.parent(Left_Finger, "Locator_L_Finger_" + str(count) + "_" + str(x - 1))

            if poseSelection == "A_Pose": #condition to check whether finger location is set for the a pose or the t pose
                mc.move(handPos[0] + (5 + (5 * x)) * side, handPos[1] - (5 + (5 * x)), handPos[2] + -(3 * count), Left_Finger) #moves finger locators based off of hand location (A Pose)
            elif poseSelection == "T_Pose":
                mc.move(handPos[0] + (5 + (5 * x)) * side, handPos[1], handPos[2] + -(3 * count), Left_Finger) #moves finger locators based off of hand location (T Pose)
            else:
                print ("Select Pose To Generate Locators")

        else: #right side fingers
            Right_Finger = mc.spaceLocator(n = "Locator_R_Finger_" + str(count) + "_" + str(x)) #creates right finger locators
            mc.scale(2,2,2, Right_Finger)
            if x == 0: #parents first finger joint to the wrist, else parents it to the previous finger joint
                mc.parent(Right_Finger, "R_Hand_Grp")
            else:
                mc.parent(Right_Finger, "Locator_R_Finger_" + str(count) + "_" + str(x-1))

            if poseSelection == "A_Pose": #condition to check whether finger location is set for the a pose or the t pose
                mc.move(handPos[0] + (5 + (5 * x)) * side, handPos[1] - (5 + (5 * x)), handPos[2] + -(3 * count), Right_Finger)
            elif poseSelection == "T_Pose":
                mc.move(handPos[0] + (5 + (5 * x)) * side, handPos[1], handPos[2] + -(3 * count), Right_Finger)
            else:
                print("Pose must be selected to create locators")

def mirrorLocators():
    allLeftLocators = mc.ls("Locator_L_*") #grabs a list of all the items in the outliner with "Locator_L" in their name
    leftLocators = mc.listRelatives(allLeftLocators, p = True, f = True) #filters the list to only include parents and the full path name of the objects

    allRightLocators = mc.ls("Locator_R_*") #grabs a list of all the items in the outliner with "Locator_R" in their name
    rightLocators = mc.listRelatives(allRightLocators, p = True, f = True) #filters the list to only include parents and the full path name of the objects

    for i,l in enumerate(leftLocators): #for loop that checks the left locators position and mirrors that translation to the right locators
        pos = mc.xform(l, q = True, t = True, ws = True)
        mc.move(-pos[0], pos[1], pos[2], rightLocators[i])

def setColor():
    mc.setAttr("Locator_Mast.overrideEnabled", 1) #sets override enabled in the attribute editor so that the color of the locators can be changed
    mc.setAttr("Locator_Mast.overrideColor", 18) #changes the color of the locators so they stand out more in the project

def lockLocators(lock):
    global editMode

    #prevents Locators from moving once created

    axis = ['x', 'y', 'z']
    attr = ['t', 'r', 's']

    nodes = mc.listRelatives("Locator_*", allParents = True)

    for axe in axis:
        for att in attr:
            for node in nodes:
                mc.setAttr(node + '.' + att + axe, lock = lock)

    if editMode == False:
        editMode = True
    else:
        editMode = False

#deletes all locators in the world using the outliner
def deleteLocators():
    if mc.objExists("Locator_Mast"):
        nodes = mc.ls("*Locator*") #places every object with the word "Locator_" in the outliner onto a list. 
        mc.delete(nodes) #deletes previously established list
    else:
        mc.confirmDialog(title = "Error", message = "Locators don't exist. Please create locators to be deleted", button = "OK")
        return