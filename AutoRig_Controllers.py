import maya.cmds as mc
import AutoRig_Locators as locator
import AutoRig_IK as ik
import AutoRig_Constraints as constraint

def createControllers():
    
    mc.confirmDialog(title = "Warning", message = "Please go to IK/FK Switch and set a kinematic before moving the controls", button = "OK")

    if mc.objExists("Controller_Grp"):
        mc.confirmDialog(title = "Error", message = "Controllers group already exist. Please delete current controllers to use this function", button = "OK")
        return    
    else:
        controllerGrp = mc.group(em = True, name = "Controller_Grp")
        
    #controls to test the waters
    #Arrow Control
    # arrowControl = mc.curve(p = [(1,0,0), (1,0,2), (2,0,2), (0,0,4), (-2,0,2), (-1,0,2), (-1,0,0), (-1,0,-2), (-2,0,-2), (0,0,-4), (2,0,-2), (1,0,-2), (1,0,0)], d = 1, n = "Control_arrow")
    # mc.scale(6,6,6, arrowControl)
    # mc.rotate(90,0,90, arrowControl)
    # rootPos = mc.xform("Skeleton_Root", q = True, t = True, ws = True)
    # mc.move(rootPos[0] + 50, rootPos[1] + 20, rootPos[2], arrowControl)
    # mc.parent(arrowControl, "Controller_Grp")
    # mc.select(arrowControl)
    # mc.addAttr(ln = "IK_FK_Switch", at = "long", min = 0, max = 1, dv = 1, k = True)

    #Root control
    rootControl = mc.circle(nr = (0,1,0), c = (0,0,0), r = 55, d = 1, s = 8, name = "Control_Root")
    selection = mc.select("Control_Root.cv[1]", "Control_Root.cv[3]", "Control_Root.cv[5]", "Control_Root.cv[7]")
    mc.scale(0.7,0.7,0.7, selection)
    mc.parent("Control_Root", "Controller_Grp")

    #generating controls for each section of the body
    pelvisControl()
    spineControl()
    shoulderControl()
    armControls()
    legControls()
    toeControlsIK()
    toeControlsFK()
    headControl()
    fingerControlsIK()
    fingerControlsFK()

    setColor()

    ik.IKHandles()
    constraint.createConstraints()



def pelvisControl():
    #pelvis control
    pelvisControl = mc.circle(nr = (0,1,0), c = (0,0,0), r = 25, d = 1, s = 16, name = "Control_Pelvis") #creates circle nurb used as the control for the pelvis
    pelvisPos = mc.xform("Skeleton_Pelvis", q = True, t = True, ws = True) #grabs the placement of the pelvis joint
    mc.move(pelvisPos[0], pelvisPos[1], pelvisPos[2], pelvisControl) #moves the controller to the locator of the pelvis
    mc.parent(pelvisControl, "Control_Root") #parents the pelvis to the controller group
    mc.makeIdentity(pelvisControl, a = True, t = 1, r = 1, s = 1) #freezes transformation on the pelvis

def spineControl():
    #spine control
    Spines = mc.ls("Skeleton_Spine_*") #getting a ref of the spine joint(s)

    for i, s in enumerate(Spines): #for loop used to create controls for the spine
        spinePos = mc.xform(s, q = True, t = True, ws = True) #getting the spine placement for the spine
        spineControl = mc.circle(nr = (0,1,0), c = (0,0,0), r = 22, d = 1, s = 16, name = "Control_Spine_" + str(i)) #creating the nurb used as the control for each spine
        mc.move(spinePos[0], spinePos[1], spinePos[2], spineControl) #moves the controllers to the location of each spine
        if i == 0: #for the first spine
            mc.parent(spineControl, "Control_Pelvis") #parents the first spine controller to the pelvis
        else:
            mc.parent(spineControl, "Control_Spine_" + str(i-1)) #parents the following spine controllers to each previous spine

    spineControls = mc.ls("Control_Spine_*") #gathers a list of each control spine in the world
    mc.makeIdentity(spineControls, a = True, t = 1, r = 1, s = 1) #freezes transformation on each spine control      

def shoulderControl():
    #this control is used to determine the shoulder rotation on the whole
    #shoulder controls 
    shoulderControl = mc.circle(nr = (0,1,0), c = (0,0,0), r = 20, d = 1, s = 16, name = "Control_Shoulder")
    shoulderPos = mc.xform("Skeleton_NeckBase", q = True, t = True, ws = True)
    mc.move(shoulderPos[0], shoulderPos[1], shoulderPos[2], shoulderControl)
    mc.scale(1,1,0.7, shoulderControl)
    mc.rotate(20,0,0, shoulderControl)

    spineControl = mc.ls("Control_Spine_" + str(locator.mc.intField(locator.spineCount, query = True, value = True) - 1))

    mc.makeIdentity(shoulderControl, a = True, t = 1, r = 1, s = 1)
    mc.parent(shoulderControl, spineControl)

def armControls():
    #shoulder control (used for the individual shoulder controls)
    #left shoulder
    l_shoulderControl_fk = mc.circle(nr= (0,1,0), c = (0,0,0), r = 6, d = 1, s = 16, n = "Control_L_Shoulder_FK")
    l_shoulderPos = mc.xform("Skeleton_L_Shoulder", q = True, t = True, ws = True)
    mc.move(l_shoulderPos[0], l_shoulderPos[1], l_shoulderPos[2], l_shoulderControl_fk)

    mc.parentConstraint("Skeleton_L_Shoulder", l_shoulderControl_fk, n = "Control_L_Shoulder_Constraint") #constraint is created to match the rotation of the shoulder control with the shoulder joint
    mc.delete("Control_L_Shoulder_Constraint") #after the rotation is set, the constraint is no longer needed

    mc.makeIdentity(l_shoulderControl_fk, a = True, t = 1, r = 1, s = 1) #freezes transformation for the shoulder control
    mc.parent(l_shoulderControl_fk, "Control_Shoulder")

    #right shoulder fk
    r_shoulderControl_fk = mc.circle(nr= (0,1,0), c = (0,0,0), r = 6, d = 1, s = 16, n = "Control_R_Shoulder_FK")
    r_shoulderPos = mc.xform("Skeleton_R_Shoulder", q = True, t = True, ws = True)
    mc.move(r_shoulderPos[0], r_shoulderPos[1], r_shoulderPos[2], r_shoulderControl_fk)

    mc.parentConstraint("Skeleton_R_Shoulder", r_shoulderControl_fk, n = "Control_R_Shoulder_Constraint") #constraint is created to match the rotation of the shoulder control with the shoulder joint
    mc.delete("Control_R_Shoulder_Constraint") #after the rotation is set, the constraint is no longer needed

    mc.makeIdentity(r_shoulderControl_fk, a = True, t = 1, r = 1, s = 1) #freezes transformation for the shoulder control
    mc.parent(r_shoulderControl_fk, "Control_Shoulder")

    #left elbow fk
    l_elbowControl_fk = mc.circle(nr= (0,1,0), c = (0,0,0), r = 6, d = 1, s = 16, n = "Control_L_Elbow_FK")
    l_elbowPos = mc.xform("Skeleton_L_Elbow", q = True, t = True, ws = True)
    mc.move(l_elbowPos[0], l_elbowPos[1], l_elbowPos[2], l_elbowControl_fk)

    mc.parentConstraint("Skeleton_L_Elbow", l_elbowControl_fk, n = "Control_L_Elbow_Constraint") #constraint is created to match the rotation of the shoulder control with the shoulder joint
    mc.delete("Control_L_Elbow_Constraint") #after the rotation is set, the constraint is no longer needed

    mc.makeIdentity(l_elbowControl_fk, a = True, t = 1, r = 1, s = 1) #freezes transformation for the shoulder control
    mc.parent(l_elbowControl_fk, l_shoulderControl_fk)

    #right elbow fk
    r_elbowControl_fk = mc.circle(nr= (0,1,0), c = (0,0,0), r = 6, d = 1, s = 16, n = "Control_R_Elbow_FK")
    r_elbowPos = mc.xform("Skeleton_R_Elbow", q = True, t = True, ws = True)
    mc.move(r_elbowPos[0], r_elbowPos[1], r_elbowPos[2], r_elbowControl_fk)

    mc.parentConstraint("Skeleton_R_Elbow", r_elbowControl_fk, n = "Control_R_Elbow_Constraint") #constraint is created to match the rotation of the shoulder control with the shoulder joint
    mc.delete("Control_R_Elbow_Constraint") #after the rotation is set, the constraint is no longer needed

    mc.makeIdentity(r_elbowControl_fk, a = True, t = 1, r = 1, s = 1) #freezes transformation for the shoulder control
    mc.parent(r_elbowControl_fk, r_shoulderControl_fk)

    #left elbow ik
    l_elbowControl_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_L_Elbow_IK")
    mc.scale(12, 12, 12, l_elbowControl_ik)

    l_elbowIK_Pos = mc.xform("Skeleton_L_Elbow", q = True, t = True, ws = True)
    l_elbowIK_Rot = mc.xform("Skeleton_L_Elbow", q = True, ro = True, ws = True)
    mc.move(l_elbowIK_Pos[0], l_elbowIK_Pos[1], l_elbowIK_Pos[2], l_elbowControl_ik)

    mc.parentConstraint("Skeleton_L_Elbow", l_elbowControl_ik, n = "Control_ElbowIK_Constraint")
    mc.delete("Control_ElbowIK_Constraint")
    mc.rotate(l_elbowIK_Rot[0], 180, l_elbowIK_Rot[2], l_elbowControl_ik)

    mc.makeIdentity(l_elbowControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_elbowControl_ik, "Control_Shoulder")

    #right elbow ik
    r_elbowControl_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_R_Elbow_IK")
    mc.scale(12, 12, 12, r_elbowControl_ik)

    r_elbowIK_Pos = mc.xform("Skeleton_R_Elbow", q = True, t = True, ws = True)
    r_elbowIK_Rot = mc.xform("Skeleton_R_Elbow", q = True, ro = True, ws = True)
    mc.move(r_elbowIK_Pos[0], r_elbowIK_Pos[1], r_elbowIK_Pos[2], r_elbowControl_ik)

    mc.parentConstraint("Skeleton_R_Elbow", r_elbowControl_ik, n = "Control_ElbowIK_Constraint")
    mc.delete("Control_ElbowIK_Constraint")
    mc.rotate(r_elbowIK_Rot[0], 180, r_elbowIK_Rot[2], r_elbowControl_ik)    

    mc.makeIdentity(r_elbowControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_elbowControl_ik, "Control_Shoulder")

    #left wrist control fk
    l_wristControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 6, d = 1, s = 16, n = "Control_L_Wrist_FK")
    l_wristPos = mc.xform("Skeleton_L_Wrist", q = True, t = True, ws = True)
    mc.move(l_wristPos[0], l_wristPos[1], l_wristPos[2], l_wristControl_fk)

    mc.parentConstraint("Skeleton_L_Wrist", l_wristControl_fk, n = "Control_L_Wrist_Constraint")
    mc.delete("Control_L_Wrist_Constraint")

    mc.makeIdentity(l_wristControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_wristControl_fk, l_elbowControl_fk)

    #right wrist control fk
    r_wristControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 6, d = 1, s = 16, n = "Control_R_Wrist_FK")
    r_wristPos = mc.xform("Skeleton_R_Wrist", q = True, t = True, ws = True)
    mc.move(r_wristPos[0], r_wristPos[1], r_wristPos[2], r_wristControl_fk)

    mc.parentConstraint("Skeleton_R_Wrist", r_wristControl_fk, n = "Control_R_Wrist_Constraint")
    mc.delete("Control_R_Wrist_Constraint")

    mc.makeIdentity(r_wristControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_wristControl_fk, r_elbowControl_fk)

    #left wrist control ik
    l_wristControl_ik = mc.circle(nr = (0,1,0), c = (0,0,0), r = 10, d = 1, s = 8, n = "Control_L_Wrist_IK")
    selection = mc.select("Control_L_Wrist_IK.cv[1]", "Control_L_Wrist_IK.cv[3]", "Control_L_Wrist_IK.cv[5]", "Control_L_Wrist_IK.cv[7]")
    mc.scale(0.3,0.3,0.3, selection)

    l_wristPos = mc.xform("Skeleton_L_Wrist", q = True, t = True, ws = True)
    mc.move(l_wristPos[0], l_wristPos[1], l_wristPos[2], l_wristControl_ik)

    mc.parentConstraint("Skeleton_L_Wrist", l_wristControl_ik, n = "Control_L_Wrist_Constraint")
    mc.delete("Control_L_Wrist_Constraint")

    mc.makeIdentity(l_wristControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_wristControl_ik, "Control_Shoulder")

    #right wrist control ik
    r_wristControl_ik = mc.circle(nr = (0,1,0), c = (0,0,0), r = 10, d = 1, s = 8, n = "Control_R_Wrist_IK")
    selection = mc.select("Control_R_Wrist_IK.cv[1]", "Control_R_Wrist_IK.cv[3]", "Control_R_Wrist_IK.cv[5]", "Control_R_Wrist_IK.cv[7]")
    mc.scale(0.3,0.3,0.3, selection)

    r_wristPos = mc.xform("Skeleton_R_Wrist", q = True, t = True, ws = True)
    mc.move(r_wristPos[0], r_wristPos[1], r_wristPos[2], r_wristControl_ik)

    mc.parentConstraint("Skeleton_R_Wrist", r_wristControl_ik, n = "Control_R_Wrist_Constraint")
    mc.delete("Control_R_Wrist_Constraint")

    mc.makeIdentity(r_wristControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_wristControl_ik, "Control_Shoulder")

def fingerControlsIK():

    #left fingers
    l_fingeramount_ik = mc.ls("Skeleton_L_Finger_*_0", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_fingeramount_ik)):
        for j in range(0,3):
            l_fingerPos = mc.xform("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j), q = True, t = True, ws = True)
            l_fingerRot = mc.xform("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j), q = True, ro = True, ws = True)

            l_finger_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_" + "L" + "_Finger_" + str(i) + "_" + str(j) + "_IK")
            mc.scale(8,8,8, l_finger_ik)
            mc.move(l_fingerPos[0], l_fingerPos[1], l_fingerPos[2], l_finger_ik)

            mc.parentConstraint("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j), l_finger_ik, n = "Control_Finger_Constraint")
            mc.delete("Control_Finger_Constraint")
            mc.rotate(-90, 0, -45, l_finger_ik)

            mc.makeIdentity(l_finger_ik, a = True, t = 1, r = 1, s = 1)

            if j == 0:
                mc.parent(l_finger_ik, "Control_L_Wrist_IK")

            if j > 0: 
                mc.parent(l_finger_ik, "Control_" + "L" + "_Finger_" + str(i) + "_" + str(j-1) + "_IK")

    #right fingers
    r_fingeramount_ik = mc.ls("Skeleton_R_Finger_*_0", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_fingeramount_ik)):
        for j in range(0,3):
            r_fingerPos = mc.xform("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j), q = True, t = True, ws = True)
            r_fingerRot = mc.xform("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j), q = True, ro = True, ws = True)

            r_finger_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_" + "R" + "_Finger_" + str(i) + "_" + str(j) + "_IK")
            mc.scale(8,8,8, r_finger_ik)
            mc.move(r_fingerPos[0], r_fingerPos[1], r_fingerPos[2], r_finger_ik)

            mc.parentConstraint("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j), r_finger_ik, n = "Control_Finger_Constraint")
            mc.delete("Control_Finger_Constraint")
            mc.rotate(-90, 0, 45, r_finger_ik)

            mc.makeIdentity(r_finger_ik, a = True, t = 1, r = 1, s = 1)

            if j == 0:
                mc.parent(r_finger_ik, "Control_R_Wrist_IK")

            if j > 0: 
                mc.parent(r_finger_ik, "Control_" + "R" + "_Finger_" + str(i) + "_" + str(j-1) + "_IK")

def fingerControlsFK():

    #left fingers
    l_fingeramount_fk = mc.ls("Skeleton_L_Finger_*_0", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_fingeramount_fk)):
        for j in range(0,3):
            l_fingerPos = mc.xform("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j), q = True, t = True, ws = True)
            l_fingerRot = mc.xform("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j), q = True, ro = True, ws = True)

            l_finger_fk = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_" + "L" + "_Finger_" + str(i) + "_" + str(j) + "_FK")
            mc.scale(8,8,8, l_finger_fk)
            mc.move(l_fingerPos[0], l_fingerPos[1], l_fingerPos[2], l_finger_fk)

            mc.parentConstraint("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j), l_finger_fk, n = "Control_Finger_Constraint")
            mc.delete("Control_Finger_Constraint")
            mc.rotate(-90, 0, -45, l_finger_fk)

            mc.makeIdentity(l_finger_fk, a = True, t = 1, r = 1, s = 1)

            if j == 0:
                mc.parent(l_finger_fk, "Control_L_Wrist_FK")

            if j > 0: 
                mc.parent(l_finger_fk, "Control_" + "L" + "_Finger_" + str(i) + "_" + str(j-1) + "_FK")

    #right fingers
    r_fingeramount_fk = mc.ls("Skeleton_R_Finger_*_0", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_fingeramount_fk)):
        for j in range(0,3):
            r_fingerPos = mc.xform("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j), q = True, t = True, ws = True)
            r_fingerRot = mc.xform("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j), q = True, ro = True, ws = True)

            r_finger_fk = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_" + "R" + "_Finger_" + str(i) + "_" + str(j) + "_FK")
            mc.scale(8,8,8, r_finger_fk)
            mc.move(r_fingerPos[0], r_fingerPos[1], r_fingerPos[2], r_finger_fk)

            mc.parentConstraint("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j), r_finger_fk, n = "Control_Finger_Constraint")
            mc.delete("Control_Finger_Constraint")
            mc.rotate(-90, 0, 45, r_finger_fk)

            mc.makeIdentity(r_finger_fk, a = True, t = 1, r = 1, s = 1)

            if j == 0:
                mc.parent(r_finger_fk, "Control_R_Wrist_FK")

            if j > 0: 
                mc.parent(r_finger_fk, "Control_" + "R" + "_Finger_" + str(i) + "_" + str(j-1) + "_FK")

def legControls():

    #left hip control fk
    l_hipControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 10, d = 1, s = 16, n = "Control_L_Hip_FK")
    l_hipPos = mc.xform("Skeleton_L_Hip", q = True, t = True, ws = True)
    mc.move(l_hipPos[0], l_hipPos[1], l_hipPos[2], l_hipControl_fk)

    mc.makeIdentity(l_hipControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_hipControl_fk, "Control_Pelvis")

    #right hip control fk
    r_hipControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 10, d = 1, s = 16, n = "Control_R_Hip_FK")
    r_hipPos = mc.xform("Skeleton_R_Hip", q = True, t = True, ws = True)
    mc.move(r_hipPos[0], r_hipPos[1], r_hipPos[2], r_hipControl_fk)

    mc.makeIdentity(r_hipControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_hipControl_fk, "Control_Pelvis")

    #left knee control fk
    l_kneeControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 8, d = 1, s = 16, n = "Control_L_Knee_FK")
    l_kneeFKPos = mc.xform("Skeleton_L_Knee", q = True, t = True, ws = True)
    mc.move(l_kneeFKPos[0], l_kneeFKPos[1], l_kneeFKPos[2], l_kneeControl_fk)

    mc.makeIdentity(l_kneeControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_kneeControl_fk, l_hipControl_fk)

    #right knee control fk
    r_kneeControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 8, d = 1, s = 16, n = "Control_R_Knee_FK")
    r_kneeFKPos = mc.xform("Skeleton_R_Knee", q = True, t = True, ws = True)
    mc.move(r_kneeFKPos[0], r_kneeFKPos[1], r_kneeFKPos[2], r_kneeControl_fk)

    mc.makeIdentity(r_kneeControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_kneeControl_fk, r_hipControl_fk)

    #left knee control ik
    l_kneeControl_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_L_Knee_IK")
    mc.scale(12, 12, 12, l_kneeControl_ik)

    l_kneeIK_Pos = mc.xform("Skeleton_L_Knee", q = True, t = True, ws = True)
    l_kneeIK_Rot = mc.xform("Skeleton_L_Knee", q = True, ro = True, ws = True)
    mc.move(l_kneeIK_Pos[0], l_kneeIK_Pos[1], l_kneeIK_Pos[2], l_kneeControl_ik)

    mc.parentConstraint("Skeleton_L_Knee", l_kneeControl_ik, n = "Control_KneeIK_Constraint")
    mc.delete("Control_KneeIK_Constraint")

    mc.makeIdentity(l_kneeControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_kneeControl_ik, "Control_Root")

    #right knee control ik
    r_kneeControl_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_R_Knee_IK")
    mc.scale(12, 12, 12, r_kneeControl_ik)

    r_kneeIK_Pos = mc.xform("Skeleton_R_Knee", q = True, t = True, ws = True)
    r_kneeIK_Rot = mc.xform("Skeleton_R_Knee", q = True, ro = True, ws = True)
    mc.move(r_kneeIK_Pos[0], r_kneeIK_Pos[1], r_kneeIK_Pos[2], r_kneeControl_ik)

    mc.parentConstraint("Skeleton_R_Knee", r_kneeControl_ik, n = "Control_KneeIK_Constraint")
    mc.delete("Control_KneeIK_Constraint")

    mc.makeIdentity(r_kneeControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_kneeControl_ik, "Control_Root")

    #left ankle control fk
    l_ankleControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 8, d = 1, s = 16, n = "Control_L_Ankle_FK")
    l_anklePos = mc.xform("Skeleton_L_Ankle", q = True, t = True, ws = True)
    mc.move(l_anklePos[0], l_anklePos[1], l_anklePos[2], l_ankleControl_fk)

    mc.makeIdentity(l_ankleControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_ankleControl_fk, l_kneeControl_fk)

    #right ankle control fk
    r_ankleControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 8, d = 1, s = 16, n = "Control_R_Ankle_FK")
    r_anklePos = mc.xform("Skeleton_R_Ankle", q = True, t = True, ws = True)
    mc.move(r_anklePos[0], r_anklePos[1], r_anklePos[2], r_ankleControl_fk)

    mc.makeIdentity(r_ankleControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_ankleControl_fk, r_kneeControl_fk)

    #left ankle control ik
    l_ankleControl_ik = mc.circle(nr = (0,1,0), c = (0,0,0), r = 10, d = 1, s = 8, n = "Control_L_Ankle_IK")
    selection = mc.select("Control_L_Ankle_IK.cv[1]", "Control_L_Ankle_IK.cv[3]", "Control_L_Ankle_IK.cv[5]", "Control_L_Ankle_IK.cv[7]")
    mc.scale(0.3,0.3,0.3, selection)
    l_anklePos = mc.xform("Skeleton_L_Ankle", q = True, t = True, ws = True)
    mc.move(l_anklePos[0], l_anklePos[1], l_anklePos[2], l_ankleControl_ik)

    mc.makeIdentity(l_ankleControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_ankleControl_ik, "Control_Root")

    #right ankle control ik
    r_ankleControl_ik = mc.circle(nr = (0,1,0), c = (0,0,0), r = 10, d = 1, s = 8, n = "Control_R_Ankle_IK")
    selection = mc.select("Control_R_Ankle_IK.cv[1]", "Control_R_Ankle_IK.cv[3]", "Control_R_Ankle_IK.cv[5]", "Control_R_Ankle_IK.cv[7]")
    mc.scale(0.3,0.3,0.3, selection)
    r_anklePos = mc.xform("Skeleton_R_Ankle", q = True, t = True, ws = True)
    mc.move(r_anklePos[0], r_anklePos[1], r_anklePos[2], r_ankleControl_ik)

    mc.makeIdentity(r_ankleControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_ankleControl_ik, "Control_Root")

    #left foot control
    # #l_arrow = mc.curve(p = [(1,0,0), (1,0,2), (2,0,2), (0,0,4), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], d = 1, n = "Control_L_Foot")
    # mc.addAttr(sn = "KT", ln = "Knee_Twist", at = "double", dv = 0, min = -100, max = 100, keyable = True)
    # mc.addAttr(sn = "KF", ln = "Knee_Fix", at = "double", dv = 0, min = 0, max = 100, keyable = True)
    # mc.addAttr(sn = "FR", ln = "Foot_Roll", at = "double", dv = 0, min = 0, max = 100, keyable = True)    
    # mc.addAttr(sn = "FBR", ln = "FootBase_Roll", at = "double", dv = 0, min = 0, max = 100, keyable = True)  

    # mc.scale(6,8,8, l_arrow)
    # l_feetPos = mc.xform("Skeleton_L_Ankle", q = True, t = True, ws = True)
    # mc.move(l_feetPos[0], -2, l_feetPos[2], l_arrow)
    # mc.makeIdentity(l_arrow, a = True, t = 1, r = 1, s = 1)    
    # mc.parent(l_arrow, "Controller_Grp")

    #right foot control
    # r_arrow = mc.curve(p = [(1,0,0), (1,0,2), (2,0,2), (0,0,4), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], d = 1, n = "Control_R_Foot")
    # mc.addAttr(sn = "KT", ln = "Knee_Twist", at = "double", dv = 0, min = -100, max = 100, keyable = True)
    # mc.addAttr(sn = "KF", ln = "Knee_Fix", at = "double", dv = 0, min = 0, max = 100, keyable = True)
    # mc.addAttr(sn = "FR", ln = "Foot_Roll", at = "double", dv = 0, min = 0, max = 100, keyable = True)    
    # mc.addAttr(sn = "FBR", ln = "FootBase_Roll", at = "double", dv = 0, min = 0, max = 100, keyable = True)  

    # mc.scale(6,8,8, r_arrow)
    # r_feetPos = mc.xform("Skeleton_R_Ankle", q = True, t = True, ws = True)
    # mc.move(r_feetPos[0], -2, r_feetPos[2], r_arrow)
    # mc.makeIdentity(r_arrow, a = True, t = 1, r = 1, s = 1)    
    # mc.parent(r_arrow, "Controller_Grp")

    #left foot base control ik
    l_footControl_ik = mc.circle(nr = (0,1,0), c = (0,0,0), r = 12, d = 1, s = 8, n = "Control_L_FootBase_IK")
    selection = mc.select("Control_L_FootBase_IK.cv[1]", "Control_L_FootBase_IK.cv[3]", "Control_L_FootBase_IK.cv[5]", "Control_L_FootBase_IK.cv[7]")
    mc.scale(0.5,0.5,0.5, selection)
    l_footPos_ik = mc.xform("Skeleton_L_Foot", q = True, t = True, ws = True)
    mc.move(l_footPos_ik[0], l_footPos_ik[1], l_footPos_ik[2], l_footControl_ik)    
    mc.rotate(90, 0, 0, l_footControl_ik)
    mc.scale(1,1,0.7, l_footControl_ik)

    mc.makeIdentity(l_footControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_footControl_ik, l_ankleControl_ik)

    #right foot base control ik
    r_footControl_ik = mc.circle(nr = (0,1,0), c = (0,0,0), r = 12, d = 1, s = 8, n = "Control_R_FootBase_IK")
    selection = mc.select("Control_R_FootBase_IK.cv[1]", "Control_R_FootBase_IK.cv[3]", "Control_R_FootBase_IK.cv[5]", "Control_R_FootBase_IK.cv[7]")
    mc.scale(0.5,0.5,0.5, selection)
    r_footPos_ik = mc.xform("Skeleton_R_Foot", q = True, t = True, ws = True)
    mc.move(r_footPos_ik[0], r_footPos_ik[1], r_footPos_ik[2], r_footControl_ik)    
    mc.rotate(90, 0, 0, r_footControl_ik)
    mc.scale(1,1,0.7, r_footControl_ik)

    mc.makeIdentity(r_footControl_ik, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_footControl_ik, r_ankleControl_ik)

    #left foot base control FK
    l_footControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 8, d = 1, s = 16, n = "Control_L_FootBase_FK")
    l_footPos = mc.xform("Skeleton_L_Foot", q = True, t = True, ws = True)
    mc.move(l_footPos[0], l_footPos[1], l_footPos[2], l_footControl_fk)    
    mc.rotate(90, 0, 0, l_footControl_fk)
    mc.scale(1,1,0.7, l_footControl_fk)

    mc.makeIdentity(l_footControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(l_footControl_fk, l_ankleControl_fk)

    #right foot base control FK
    r_footControl_fk = mc.circle(nr = (0,1,0), c = (0,0,0), r = 8, d = 1, s = 16, n = "Control_R_FootBase_FK")
    r_footPos = mc.xform("Skeleton_R_Foot", q = True, t = True, ws = True)
    mc.move(r_footPos[0], r_footPos[1], r_footPos[2], r_footControl_fk)    
    mc.rotate(90, 0, 0, r_footControl_fk)
    mc.scale(1,1,0.7, r_footControl_fk)

    mc.makeIdentity(r_footControl_fk, a = True, t = 1, r = 1, s = 1)
    mc.parent(r_footControl_fk, r_ankleControl_fk)

def toeControlsIK():
    #left toes
    l_toeamount = mc.ls("Skeleton_L_Toe*") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_toeamount)):
            l_toePos = mc.xform("Skeleton_L_Toe" + str(i), q = True, t = True, ws = True)
            l_toeRot = mc.xform("Skeleton_L_Toe" + str(i), q = True, ro = True, ws = True)

            l_toe_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_L_Toe_" + str(i) + "_IK")
            mc.scale(4,4,4, l_toe_ik)
            mc.move(l_toePos[0], l_toePos[1], l_toePos[2], l_toe_ik)

            mc.parentConstraint("Skeleton_L_Toe" + str(i), l_toe_ik, n = "Control_Toe_Constraint")
            mc.delete("Control_Toe_Constraint")
            mc.rotate(-90, l_toeRot[1], l_toeRot[2], l_toe_ik)

            mc.parent(l_toe_ik, "Control_L_FootBase_IK") 
            mc.makeIdentity(l_toe_ik, a = True, t = 1, r = 1, s = 1)

    #right toes
    r_toeamount = mc.ls("Skeleton_R_Toe*") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_toeamount)):
            r_toePos = mc.xform("Skeleton_R_Toe" + str(i), q = True, t = True, ws = True)
            r_toeRot = mc.xform("Skeleton_R_Toe" + str(i), q = True, ro = True, ws = True)

            r_toe_ik = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_R_Toe_" + str(i) + "_IK")
            mc.scale(4,4,4, r_toe_ik)
            mc.move(r_toePos[0], r_toePos[1], r_toePos[2], r_toe_ik)

            mc.parentConstraint("Skeleton_R_Toe" + str(i), r_toe_ik, n = "Control_Toe_Constraint")
            mc.delete("Control_Toe_Constraint")
            mc.rotate(-90, r_toeRot[1], r_toeRot[2], r_toe_ik)

            mc.parent(r_toe_ik, "Control_R_FootBase_IK")
            mc.makeIdentity(r_toe_ik, a = True, t = 1, r = 1, s = 1)

def toeControlsFK():
    #left toes
    l_toeamount = mc.ls("Skeleton_L_Toe*") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_toeamount)):
            l_toePos = mc.xform("Skeleton_L_Toe" + str(i), q = True, t = True, ws = True)
            l_toeRot = mc.xform("Skeleton_L_Toe" + str(i), q = True, ro = True, ws = True)

            l_toe_fk = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_L_Toe_" + str(i) + "_FK")
            mc.scale(4,4,4, l_toe_fk)
            mc.move(l_toePos[0], l_toePos[1], l_toePos[2], l_toe_fk)

            mc.parentConstraint("Skeleton_L_Toe" + str(i), l_toe_fk, n = "Control_Toe_Constraint")
            mc.delete("Control_Toe_Constraint")
            mc.rotate(-90, l_toeRot[1], l_toeRot[2], l_toe_fk)

            mc.parent(l_toe_fk, "Control_L_FootBase_FK") 
            mc.makeIdentity(l_toe_fk, a = True, t = 1, r = 1, s = 1)

    #right toes
    r_toeamount = mc.ls("Skeleton_R_Toe*") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_toeamount)):
            r_toePos = mc.xform("Skeleton_R_Toe" + str(i), q = True, t = True, ws = True)
            r_toeRot = mc.xform("Skeleton_R_Toe" + str(i), q = True, ro = True, ws = True)

            r_toe_fk = mc.curve(p = [(0,0,0), (0,0,0.5), (0.2, 0, 0.7), (0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], d = 1, n = "Control_R_Toe_" + str(i) + "_FK")
            mc.scale(4,4,4, r_toe_fk)
            mc.move(r_toePos[0], r_toePos[1], r_toePos[2], r_toe_fk)

            mc.parentConstraint("Skeleton_R_Toe" + str(i), r_toe_fk, n = "Control_Toe_Constraint")
            mc.delete("Control_Toe_Constraint")
            mc.rotate(-90, r_toeRot[1], r_toeRot[2], r_toe_fk)

            mc.parent(r_toe_fk, "Control_R_FootBase_FK")
            mc.makeIdentity(r_toe_fk, a = True, t = 1, r = 1, s = 1)

def headControl():

    #neck base contro
    neckBaseControl = mc.circle(nr = (0,1,0), c = (0,0,0), r = 5, d = 1, s = 16, name = "Control_NeckBase")
    neckPos = mc.xform("Skeleton_NeckBase", q = True, t = True, ws = True)
    mc.move(neckPos[0], neckPos[1], neckPos[2], neckBaseControl) 
    mc.parent(neckBaseControl, "Control_Spine_" + str((locator.mc.intField(locator.spineCount, query = True, value = True) - 1)))

    #neck control
    neck = mc.ls("Skeleton_Neck_*")

    for i,n in enumerate(neck):
        neckPos = mc.xform(n, q = True, t = True, ws = True)
        neckControl = mc.circle(nr = (0,1,0), c = (0,0,0), r = 5, d = 1, s = 16, name = "Control_Neck_" + str(i))
        mc.move(neckPos[0], neckPos[1], neckPos[2], neckControl) #moves the controllers to the location of each neck joint
        if i == 0: #for the first neck
            mc.parent(neckControl, neckBaseControl) #parents the first neck controller to the shoulder control
        else:
            mc.parent(neckControl, "Control_Neck_" + str(i-1)) #parents the following spine controllers to each previous spine  

    #head control
    headControl = mc.circle(nr = (0,1,0), c = (0,0,0), r = 15, d = 1, s = 16, name = "Control_Head")
    headPos = mc.xform("Skeleton_Head", q = True, t = True, ws = True)
    mc.move(headPos[0], headPos[1], headPos[2], headControl) 
    mc.parent(headControl, "Control_Neck_" + str(len(neck) - 1))

def setColor():
    mc.setAttr("Controller_Grp.overrideEnabled", 1) #sets override enabled in the attribute editor so that the color of the locators can be changed
    mc.setAttr("Controller_Grp.overrideColor", 21) #changes the color of the locators so they stand out more in the project

    leftControls = mc.ls("Control_L_*", type = "transform")

    for i in range(0, len(leftControls)):
        mc.setAttr(leftControls[i] + ".overrideEnabled", 1)
        mc.setAttr(leftControls[i] + ".overrideColor", 22)

    rightControls = mc.ls("Control_R_*", type = "transform")

    for i in range(0, len(rightControls)):
        mc.setAttr(rightControls[i] + ".overrideEnabled", 1)
        mc.setAttr(rightControls[i] + ".overrideColor", 18)

def deleteControllers():

    controls = mc.ls("Control*")
    mc.delete(controls)

    ik.deleteIK()

    constraint.deleteConstraints()