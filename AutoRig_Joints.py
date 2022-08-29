#Xavier Rodriguez
#AutoRig Joints

import maya.cmds as mc
import AutoRig_Locators as locator

def createJoints():
    if mc.objExists("Skeleton_Grp"):
        mc.confirmDialog(title = "Skeleton Already Exists", message = "Skeleton Group already exists", button = "OK")
        return
    else:
        jointGrp = mc.group(em = True, name = "Skeleton_Grp") #creating a separate group for the rig

    if mc.objExists("Locator_Mast"):
        pass
    else:
        mc.confirmDialog(title = "Error", message = "Locators must be created before the skeleton can be made.", button = "OK")
        return

    root = mc.ls("Locator_Root") #getting a ref of the root locator
    pelvis = mc.ls("Locator_Pelvis") #getting a ref of the pelvis locator

    Spines = mc.ls("Locator_Spine_*", type = 'locator') #getting a ref of the spine locator(s)
    spine = mc.listRelatives(Spines, p = True, f = True) #filtering the ref for the spine locator(s)

    rootPos = mc.xform(root, q = True, t = True, ws = True) #getting the position of the locator root and setting it for the skeleton root
    rootJoint = mc.joint(radius = 3, p = rootPos, name = "Skeleton_Root") #creating a joint at the location of the locator root

    pelvisPos = mc.xform(pelvis, q = True, t = True, ws = True) #getting the position of the locator pelvis and setting it for the skeleton pelvis   
    pelvisJoint = mc.joint(radius = 3, p = pelvisPos, name = "Skeleton_Pelvis") #creating a joint at the location of the locator pelvis

    for i, s in enumerate(spine): #for loop that checks the position of the spine locators and creates a spine skeleton in the same location
        pos = mc.xform(s, q = True, t = True, ws = True)
        jointSpine = mc.joint(radius = 3, p = pos, name = "Skeleton_Spine_" + str(i))

    spinePos = mc.xform("Skeleton_Spine_" + str((locator.mc.intField(locator.spineCount, query = True, value = True) - 1)), q = True, t = True, ws = True)

    createHeadJoints()
    createArmJoints(spinePos)
    createLegJoints()

    if mc.objExists("Locator_L_Inv_Heel"):
        createInverseFootRollJoint()
        mc.mirrorJoint("Skeleton_L_Inv_Heel", mb = True, myz = True, sr = ["_L", "_R"])
    else:
        pass

    if mc.objExists("*ArmTwist*"):
        createArmTwistJoints()
    else:
        pass

    mc.mirrorJoint("Skeleton_L_Clavicle", mb = True, myz = True, sr = ["_L", "_R"])

    if mc.objExists("*ThighTwist*") and mc.objExists("*AnkleTwist*"):
        createLegTwistJoints()
    else:
        pass

    mc.mirrorJoint("Skeleton_L_Hip", mb = True, myz = True, sr = ["_L", "_R"])

    setJointOrientation()

    locator.deleteLocators()

def createHeadJoints(): 

    #joints parent based off the previously selected object automatically, so by selecting the final spine joint before the neck is created, this ensures the neck is parented to the spine instead of anything else
    spine = mc.select("Skeleton_Spine_" + str((locator.mc.intField(locator.spineCount, query = True, value = True) - 1))) 
    spinePos = mc.xform("Skeleton_Spine_" + str((locator.mc.intField(locator.spineCount, query = True, value = True) - 1)), q = True, t = True, ws = True)

    neckBase = mc.ls("Locator_NeckBase") #"_" between "Neck" and "Base" was removed to ensure joint wouldn't be selected by the neck list used to create the later neck joints
    NeckBase = mc.listRelatives(neckBase, p = True, f = True)
    neckBasePos = mc.xform(neckBase,  q = True, t = True, ws = True)
    neckBaseJoint = mc.joint(r = 3, p = ((neckBasePos[0] - spinePos[0]), (neckBasePos[1] - spinePos[1]), (neckBasePos[2] - spinePos[2])), name = "Skeleton_NeckBase")
    
    mc.setAttr("Skeleton_NeckBase.radius", 3)

    Neck = mc.ls("Locator_Neck_*", type = "locator") #grabbing a list of neck locators for the enumberator
    neck = mc.listRelatives(Neck, p = True, f = True) #this is to prevent moving anything from the neck locators that isn't the locators themselves (such as shapes, etc)

    for i, s in enumerate(neck): #for loop used to create the neck joints 
        neck_Pos = mc.xform(s, q = True, t = True, ws = True) #getting the position of each neck locator
        neck_Joint = mc.joint(radius = 3, p = neck_Pos, name = "Skeleton_Neck_" + str(i)) #creating a joint using the locator pos as ref and renaming it to much the skeletal convention
    
    #mc.select("Skeleton_Neck_*" + str((locator.mc.intField(locator.neckCount, query = True, value = True) - 1)))
    head = mc.ls("Locator_Head")
    head_Pos = mc.xform(head, q = True, t = True, ws = True) #grabbing the position of the head locator
    head_Joint = mc.joint(r = 3, p = ((head_Pos[0] - neck_Pos[0]), (head_Pos[1] - neck_Pos[1]), (head_Pos[2] - neck_Pos[2])), n = "Skeleton_Head") #creates the head joint and locates it by subtracting the location of the head locator with that of the current neck location (head spawned in a weird area otherwise)
    mc.setAttr("Skeleton_Head.radius", 3)

def createArmJoints(SpinePos):
    spine = mc.select("Skeleton_Spine_" + str((locator.mc.intField(locator.spineCount, query = True, value = True) - 1)))

    head = mc.ls("Locator_Head")
    head_Pos = mc.xform(head, q = True, t = True, ws = True) #grabbing the position of the head locator

    #neckPos = mc.xform("Skeleton_Neck_" + str((locator.mc.intField(locator.neckCount, query = True, value = True) - 1)), q = True, t = True, ws = True)
    #print (neckPos)

    leftClavicle = mc.ls("Locator_L_Clavicle")
    leftClavicle_Pos = mc.xform(leftClavicle, q = True, t = True, ws = True)
    leftClavicle_Joint = mc.joint(r = 3, p = ((leftClavicle_Pos[0] - SpinePos[0]), (leftClavicle_Pos[1] - SpinePos[1]), (leftClavicle_Pos[2] - SpinePos[2])), n = "Skeleton_L_Clavicle")
    #mc.setAttr("Skeleton_L_Clavicle.radius", 3)
    mc.setAttr ("Skeleton_L_Clavicle.radius", 3)
    
    leftUpperArm = mc.ls("Locator_L_UpperArm")
    leftUpperArm_Pos = mc.xform(leftUpperArm, q = True, t = True, ws = True)
    leftUpperArm_Joint = mc.joint(radius = 3, p = leftUpperArm_Pos, name = "Skeleton_L_Shoulder")

    leftElbow = mc.ls("Locator_L_Elbow")
    leftElbow_Pos = mc.xform(leftElbow, q = True, t = True, ws = True)
    leftElbow_Joint = mc.joint(radius = 3, p = leftElbow_Pos, name = "Skeleton_L_Elbow")

    leftWrist = mc.ls("Locator_L_Wrist")
    leftWrist_Pos = mc.xform(leftWrist, q = True, t = True, ws = True)
    leftWrist_Joint = mc.joint(radius = 3, p = leftWrist_Pos, name = "Skeleton_L_Wrist")

    createFingerJoints()

    #mirroring joints instead of creating the right arm joint hierarchy from scratch like before to streamline code
    #mc.mirrorJoint(leftClavicle_Joint, mb = True, myz = True, sr = ["_L", "_R"])

# def createArmFKJoints():

#     selectArm = mc.ls("Skeleton_L_Shoulder", "Skeleton_L_Elbow", "Skeleton_L_Wrist")
#     mc.duplicate(selectArm, po = True, rc = True)

#     mc.rename("Skeleton_L_Shoulder1", "Skeleton_L_Shoulder_FK")
#     mc.rename("Skeleton_L_Elbow1", "Skeleton_L_Elbow_FK")
#     mc.rename("Skeleton_L_Wrist1", "Skeleton_L_Wrist_FK")

def createLegJoints():

    pelvis = mc.select("Skeleton_Pelvis")

    leftHip = mc.ls("Locator_L_Hip")
    leftHip_Pos = mc.xform(leftHip, q = True, t = True, ws = True)
    leftHip_Joint = mc.joint(radius = 3, p = leftHip_Pos, name = "Skeleton_L_Hip")
    #mc.parent(leftHip_Joint, "Skeleton_Pelvis")

    leftKnee = mc.ls("Locator_L_Knee")
    leftKnee_Pos = mc.xform(leftKnee, q = True, t = True, ws = True)
    leftKnee_Joint = mc.joint(radius = 3, p = leftKnee_Pos, name = "Skeleton_L_Knee")

    leftFoot = mc.ls("Locator_L_Ankle")
    leftFoot_Pos = mc.xform(leftFoot, q = True, t = True, ws = True)
    leftFoot_Joint = mc.joint(radius = 3, p = leftFoot_Pos, name = "Skeleton_L_Ankle")

    leftFootBase = mc.ls("Locator_L_FootBase")
    leftFootBase_Pos = mc.xform(leftFootBase, q = True, t = True, ws = True)
    leftFootBase_Joint = mc.joint(radius = 3, p = leftFootBase_Pos, name = "Skeleton_L_Foot")   

    createToeJoints()
    
    #mirroring joints instead of creating the right leg joint hierarchy from scratch like before to streamline code
    #mc.mirrorJoint(leftHip_Joint, mb = True, myz = True, sr = ["_L", "_R"])

def createInverseFootRollJoint():
    mc.select(deselect = True)

    l_inverse_heel_joint = mc.joint(r = 6, p = mc.xform(mc.ls("Locator_L_Inv_Heel", type = "transform"), q = True, t = True, ws = True), n = "Skeleton_L_Inv_Heel")
    l_inverse_toe_joint = mc.joint(r = 3, p = mc.xform(mc.ls("Locator_L_Inv_Toe", type = "transform"), q = True, t = True, ws = True), a = True, n = "Skeleton_L_Inv_Toe")
    l_inverse_footBase_joint = mc.joint(r = 3, p = mc.xform(mc.ls("Locator_L_Inv_footBase", type = "transform"), q = True, t = True, ws = True), a = True, n = "Skeleton_L_Inv_footBase")
    l_inverse_ankle_joint = mc.joint(r = 3, p = mc.xform(mc.ls("Locator_L_Inv_Ankle", type = "transform"), q = True, t = True, ws = True), a = True, n = "Skeleton_L_Inv_Ankle")
    mc.parent(l_inverse_heel_joint, "Skeleton_Grp")

    # mc.select(deselect = True)

    # r_inverse_heel_joint = mc.joint(r = 3, p = mc.xform(mc.ls("Locator_R_Inv_Heel", type = "transform"), q = True, t = True, ws = True), n = "Skeleton_R_Inv_Heel")
    # r_inverse_toe_joint = mc.joint(r = 3, p = mc.xform(mc.ls("Locator_R_Inv_Toe", type = "transform"), q = True, t = True, ws = True), a = True, n = "Skeleton_R_Inv_Toe")
    # r_inverse_footBase_joint = mc.joint(r = 3, p = mc.xform(mc.ls("Locator_R_Inv_footBase", type = "transform"), q = True, t = True, ws = True), a = True, n = "Skeleton_R_Inv_footBase")
    # r_inverse_ankle_joint = mc.joint(r = 3, p = mc.xform(mc.ls("Locator_R_Inv_Ankle", type = "transform"), q = True, t = True, ws = True), a = True, n = "Skeleton_R_Inv_Ankle")
    # mc.parent(r_inverse_heel_joint, "Skeleton_R_Toe0")

def createArmTwistJoints():

    #forearm twist
    mc.select(deselect = True)

    if (mc.objExists("Locator_L_ArmTwist_*")):
        l_armTwists = mc.ls("Locator_L_ArmTwist_*", type = "transform")

        for i, j in enumerate(l_armTwists):
            L_armTwistJoint = mc.joint(r = 6, p = mc.xform(j, q = True, t = True, ws = True), a = True, n = "Skeleton_L_ArmTwist_" + str(i))
        mc.parent("Skeleton_L_ArmTwist_0", "Skeleton_L_Elbow")
    else:
        pass

    #upperarm twist
    mc.select(deselect = True)

    if (mc.objExists("Locator_L_UpperArmTwist_*")):
        l_upperArmTwists = mc.ls("Locator_L_UpperArmTwist_*", type = "transform")

        for i, j in enumerate(l_upperArmTwists):
            print(str(j))
            L_upperArmTwistJoint = mc.joint(r = 6, p = mc.xform(j, q = True, t = True, ws = True), a = True, n = "Skeleton_L_UpperArmTwist_" + str(i))
        mc.parent("Skeleton_L_UpperArmTwist_0", "Skeleton_L_Shoulder")
    else:
        pass

def createLegTwistJoints():

    #thigh twist
    mc.select(deselect = True)

    if (mc.objExists("Locator_L_ThighTwist_*")):
        l_thighTwists = mc.ls("Locator_L_ThighTwist_*", type = "transform")

        for i, j in enumerate(l_thighTwists):
            print(str(j))
            L_thighTwistJoint = mc.joint(r = 6, p = mc.xform(j, q = True, t = True, ws = True), a = True, n = "Skeleton_L_ThighTwist_" + str(i))
        mc.parent("Skeleton_L_ThighTwist_0", "Skeleton_L_Hip")
    else:
        pass

    #ankle twist
    mc.select(deselect = True)

    if (mc.objExists("Locator_L_AnkleTwist_*")):
        l_ankleTwists = mc.ls("Locator_L_AnkleTwist_*", type = "transform")

        for i, j in enumerate(l_ankleTwists):
            print(str(j))
            L_ankleTwistJoint = mc.joint(r = 6, p = mc.xform(j, q = True, t = True, ws = True), a = True, n = "Skeleton_L_AnkleTwist_" + str(i))
        mc.parent("Skeleton_L_AnkleTwist_0", "Skeleton_L_Knee")
    else:
        pass

def createFingerJoints():

    amount = mc.ls("Locator_L_Finger_*_0", type = "transform")

    for x in range(0, len(amount)):
        mc.select("Skeleton_L_Wrist")
        allLeftFinger = mc.ls("Locator_L_Finger_" + str(x) + "_*", type = "transform")
        leftFingers = mc.listRelatives(allLeftFinger, p = True, s = False)

        for i, f in enumerate(allLeftFinger):
            fingerPos = mc.xform(f, q = True, t = True, ws = True)
            leftFinger_Joints = mc.joint(radius = 3, p = fingerPos, name = "Skeleton_L_Finger_" + str(x) + "_" + str(i))

def createToeJoints():
    
    amount = mc.ls("Locator_L_Toe_*_0", type = "transform")

    footPos = mc.xform("Skeleton_L_Foot", q = True, t = True, ws = True)

    for x in range(0, len(amount)):
        mc.select("Skeleton_L_Foot")
        allLeftToes = mc.ls("Locator_L_Toe_" + str(x) + "_*", type = "transform")
        leftToes = mc.listRelatives(allLeftToes, p = True, s = False)

        for i, t in enumerate(allLeftToes):
            toePos = mc.xform(t, q = True, t = True, ws = True)
            toeJoint = mc.joint(r = 3, p = ((toePos[0] - footPos[0]), (toePos[1] - footPos[1]), (toePos[2] - footPos[2])), name = "Skeleton_L_Toe" + str(i))

def setJointOrientation():
    mc.select("Skeleton_Root")
    mc.joint(e = True, ch = True, oj = "xyz", secondaryAxisOrient = "xup")
    mc.select("*Clavicle*", "*Shoulder*", "*Elbow*")
    mc.joint(e = True, oj = "yzx", sao = "zup", zso = True)
    mc.select("*Wrist*")
    mc.joint(e = True, oj = "none", zso = True)
    mc.select("*Foot*")
    mc.joint(e = True, oj = "none", zso = True)
    mc.select("Skeleton_*_Finger_*_2")
    mc.joint(e = True, oj = "none", zso = True)    

#deletes all joints in the world using the outliner
def deleteJoints():
    if mc.objExists("Skeleton_Grp"):
        nodes = mc.ls("Skeleton_*")
        mc.delete(nodes)
    else:
        mc.confirmDialog(title = "Error", message = "Skeleton doesn't exist. Please create skeleton to be deleted", button = "OK")
        return

def bindSkin():
    selection = mc.ls(sl = True)
    if (len(selection) == 0):
        mc.confirmDialog(title = "No Selection", m = "Please Select A Mesh To Bind Skin", b = "OK")
    else:
        for i in range(0, len(selection)):
            mc.skinCluster(selection[i], "Skeleton_Root", bm = 0, ps = 1, dr = 1, n = "Mesh" + str(i))

def resetJoints():
    if mc.objExists("Skeleton_Grp"):
        nodes = mc.ls("Skeleton_*")
        mc.delete(nodes)
        createJoints()
    else:
        mc.confirmDialog(title = "Error", message = "Skeleton doesn't exist. Please create skeleton to be deleted", button = "OK")
        return