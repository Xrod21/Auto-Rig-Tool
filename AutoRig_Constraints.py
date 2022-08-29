import maya.cmds as mc

def createConstraints(): #ik

    mc.cycleCheck(e = False)

    #root constraint
    rootControl = mc.ls("Control_Root")
    rootJoint = mc.ls("Skeleton_Root")

    mc.parentConstraint(rootControl, rootJoint, mo = True, n = "root_parentConstraint")

    spineConstraint()
    headConstraint()
    shoulderConstraint()

    fingerConstraintsIK()
    fingerConstraintsFK()

    armConstraintsIK()
    legConstraintsIK()

    armConstraintsFK()
    legConstraintsFK()

    toeConstraintsIK()
    toeConstraintsFK()
    
def spineConstraint():
    Spines = mc.ls("Skeleton_Spine_*") #getting a ref of the spine joint(s)

    for i, s in enumerate(Spines): #for loop used to create controls for the spine
        spineControl = mc.ls("Control_Spine_" + str(i))
        spineJoint = mc.ls("Skeleton_Spine_" + str(i))
        
        spineConstraint = mc.orientConstraint(spineControl, spineJoint, mo = True, n = "spine_" + str(i) + "_orientConstraint")

def headConstraint():

    #neck base constraint
    neckBaseControl = mc.ls("Control_NeckBase")
    neckBaseJoint = mc.ls("Skeleton_NeckBase")

    mc.orientConstraint(neckBaseControl, neckBaseJoint, mo = True, n = "neckBase_orientConstraint")

    #neck constraint
    Neck = mc.ls("Skeleton_Neck_*")

    for i, n in enumerate(Neck): #for loop used to create controls for the spine
        neckControl = mc.ls("Control_Neck_" + str(i))
        neckJoint = mc.ls("Skeleton_Neck_" + str(i))
        
        mc.orientConstraint(neckControl, neckJoint, mo = True, n = "neck_" + str(i) + "_orientConstraint")

    #head constraint
    headControl = mc.ls("Control_Head")
    headJoint = mc.ls("Skeleton_Head")

    mc.orientConstraint(headControl, headJoint, mo = True, n = "head_orientConstraint")

def shoulderConstraint(): #accounts for clavicle to shoudler constraint 

    #shoulder constraint
    shoulderControl = mc.ls("Control_Shoulder")

    l_clavicleJoint = mc.ls("Skeleton_L_Clavicle")
    r_clavicleJoint = mc.ls("Skeleton_R_Clavicle")

    mc.parentConstraint(shoulderControl, l_clavicleJoint, mo = True, n = "l_clavicle_parentConstraint")
    mc.parentConstraint(shoulderControl, r_clavicleJoint, mo = True, n = "r_clavicle_parentConstraint")   

def fingerConstraintsIK():
    
    #left fingers
    l_fingeramount_ik = mc.ls("Control_L_Finger_*_0_IK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_fingeramount_ik)):
        for j in range(0,3):
            l_fingerControl_ik = mc.ls("Control_" + "L" + "_Finger_" + str(i) + "_" + str(j) + "_IK")
            l_fingerJoint = mc.ls("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j))

            mc.orientConstraint(l_fingerControl_ik, l_fingerJoint, mo = True, n = "Control_L_Finger_" + str(i) + "_" + str(j) + "_IK" + "_Constraint")

   #right fingers
    r_fingeramount_ik = mc.ls("Control_R_Finger_*_0_IK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_fingeramount_ik)):
        for j in range(0,3):
            r_fingerControl_ik = mc.ls("Control_" + "R" + "_Finger_" + str(i) + "_" + str(j) + "_IK")
            r_fingerJoint = mc.ls("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j))

            mc.orientConstraint(r_fingerControl_ik, r_fingerJoint, mo = True, n = "Control_R_Finger_" + str(i) + "_" + str(j) + "_IK" + "_Constraint")

def fingerConstraintsFK():
    #left fingers
    l_fingeramount_fk = mc.ls("Control_L_Finger_*_0_FK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_fingeramount_fk)):
        for j in range(0,3):
            l_fingerControl_fk = mc.ls("Control_" + "L" + "_Finger_" + str(i) + "_" + str(j) + "_FK")
            l_fingerJoint = mc.ls("Skeleton_" + "L" + "_Finger_" + str(i) + "_" + str(j))

            mc.orientConstraint(l_fingerControl_fk, l_fingerJoint, mo = True, n = "Control_L_Finger_" + str(i) + "_" + str(j) + "_FK" + "_Constraint")

   #right fingers
    r_fingeramount_fk = mc.ls("Control_R_Finger_*_0_FK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_fingeramount_fk)):
        for j in range(0,3):
            r_fingerControl_fk = mc.ls("Control_" + "R" + "_Finger_" + str(i) + "_" + str(j) + "_FK")
            r_fingerJoint = mc.ls("Skeleton_" + "R" + "_Finger_" + str(i) + "_" + str(j))

            mc.orientConstraint(r_fingerControl_fk, r_fingerJoint, mo = True, n = "Control_R_Finger_" + str(i) + "_" + str(j) + "_FK" + "_Constraint")

def armConstraintsIK(): #ik

    #left elbow ik
    l_elbowControl_ik = mc.ls("Control_L_Elbow_IK")
    l_elbowHandle_ik = mc.ls("IK_L_Arm")

    mc.poleVectorConstraint(l_elbowControl_ik, l_elbowHandle_ik, w = 1, n = "l_elbow_poleConstraint_IK")

    #left wrist ik
    l_wristControl_ik = mc.ls("Control_L_Wrist_IK")
    l_wristHandle_ik = mc.ls("IK_L_Arm")
    l_wristJoint = mc.ls("Skeleton_L_Wrist")

    mc.pointConstraint(l_wristControl_ik, l_wristHandle_ik, mo = True, n = "l_wrist_pointConstraint_IK") #allows the ik wrist controller to manip the left arm ik handle when moved
    mc.orientConstraint(l_wristControl_ik, l_wristJoint, mo = True, n = "l_wrist_orientConstraint_IK") #allows the ik wrist controller to manip the left wrist joint when rotated

    #right elbow ik
    r_elbowControl_ik = mc.ls("Control_R_Elbow_IK")
    r_elbowHandle_ik = mc.ls("IK_R_Arm")

    mc.poleVectorConstraint(r_elbowControl_ik, r_elbowHandle_ik, w = 1, n = "r_elbow_poleConstraint_IK")

    #right wrist ik
    r_wristControl_ik = mc.ls("Control_R_Wrist_IK")
    r_wristHandle_ik = mc.ls("IK_R_Arm")
    r_wristJoint = mc.ls("Skeleton_R_Wrist")

    mc.pointConstraint(r_wristControl_ik, r_wristHandle_ik, mo = True, n = "r_wrist_pointConstraint_IK") #allows the ik wrist controller to manip the left arm ik handle when moved
    mc.orientConstraint(r_wristControl_ik, r_wristJoint, mo = True, n = "r_wrist_orientConstraint_IK") #allows the ik wrist controller to manip the left wrist joint when rotated

def legConstraintsIK():

    #left knee ik
    l_kneeControl_ik = mc.ls("Control_L_Knee_IK")
    l_kneeHandle_ik = mc.ls("IK_L_Leg")

    mc.poleVectorConstraint(l_kneeControl_ik, l_kneeHandle_ik, w = 1, n = "l_knee_poleConstraint_IK")

    #left ankle ik
    l_ankleControl_ik = mc.ls("Control_L_Ankle_IK")
    l_ankleHandle_ik = mc.ls("IK_L_Leg")
    l_ankleJoint = mc.ls("Skeleton_L_Ankle")

    mc.pointConstraint(l_ankleControl_ik, l_ankleHandle_ik, mo = True, n = "l_ankle_pointConstraint_IK") #allows the ik wrist controller to manip the left arm ik handle when moved
    mc.orientConstraint(l_ankleControl_ik, l_ankleJoint, mo = True, n = "l_ankle_orientConstraint_IK") #allows the ik wrist controller to manip the left wrist joint when rotated

    #right knee ik
    r_kneeControl_ik = mc.ls("Control_R_Knee_IK")
    r_kneeHandle_ik = mc.ls("IK_R_Leg")

    mc.poleVectorConstraint(r_kneeControl_ik, r_kneeHandle_ik, w = 1, n = "r_knee_poleConstraint_IK")

    #right ankle ik
    r_ankleControl_ik = mc.ls("Control_R_Ankle_IK")
    r_ankleHandle_ik = mc.ls("IK_R_Leg")
    r_ankleJoint = mc.ls("Skeleton_R_Ankle")

    mc.pointConstraint(r_ankleControl_ik, r_ankleHandle_ik, mo = True, n = "r_ankle_pointConstraint_IK") #allows the ik wrist controller to manip the left arm ik handle when moved
    mc.orientConstraint(r_ankleControl_ik, r_ankleJoint, mo = True, n = "r_ankle_orientConstraint_IK") #allows the ik wrist controller to manip the left wrist joint when rotated

    # reverseFootIK()

def reverseFootIK():
    if mc.objExists("Skeleton_L_Inv_Heel"):
        mc.parent("Skeleton_L_Inv_Heel", w = True)
        mc.parent("Skeleton_L_Inv_Heel", "Control_L_Ankle_IK")

        mc.parent("Skeleton_R_Inv_Heel", w = True)
        mc.parent("Skeleton_R_Inv_Heel", "Control_R_Ankle_IK")

        mc.parent("IK_L_Leg", "Control_L_Ankle_IK")
    else:
        pass

def armConstraintsFK(): #fk 

    #left arm fk
    l_shoulderControl_fk = mc.ls("Control_L_Shoulder_FK") #grabs a ref for the shoulder fk control
    l_elbowControl_fk = mc.ls("Control_L_Elbow_FK")
    l_wristControl_fk = mc.ls("Control_L_Wrist_FK") 

    l_shoulderJoint = mc.ls("Skeleton_L_Shoulder") #grabs a ref for the shoulder joint
    l_elbowJoint = mc.ls("Skeleton_L_Elbow") 
    l_wristJoint = mc.ls("Skeleton_L_Wrist")   

    mc.parentConstraint(l_shoulderControl_fk, l_shoulderJoint, mo = True, n = "l_shoulder_parentConstraint_FK")
    mc.parentConstraint(l_elbowControl_fk, l_elbowJoint, mo = True, n = "l_elbow_parentConstraint_FK")
    mc.parentConstraint(l_wristControl_fk, l_wristJoint, mo = True, n = "l_wrist_parentConstraint_FK")

    #right arm fk
    r_shoulderControl_fk = mc.ls("Control_R_Shoulder_FK") #grabs a ref for the shoulder fk control
    r_elbowControl_fk = mc.ls("Control_R_Elbow_FK")
    r_wristControl_fk = mc.ls("Control_R_Wrist_FK") 

    r_shoulderJoint = mc.ls("Skeleton_R_Shoulder") #grabs a ref for the shoulder joint
    r_elbowJoint = mc.ls("Skeleton_R_Elbow") 
    r_wristJoint = mc.ls("Skeleton_R_Wrist")   

    mc.parentConstraint(r_shoulderControl_fk, r_shoulderJoint, mo = True, n = "r_shoulder_parentConstraint_FK")
    mc.parentConstraint(r_elbowControl_fk, r_elbowJoint, mo = True, n = "r_elbow_parentConstraint_FK")
    mc.parentConstraint(r_wristControl_fk, r_wristJoint, mo = True, n = "r_wrist_parentConstraint_FK")

def legConstraintsFK():
    
    #pelvis fk
    pelvisControl = mc.ls("Control_Pelvis")
    pelvisJoint = mc.ls("Skeleton_Pelvis")

    l_hipJoint = mc.ls("Skeleton_L_Hip")
    r_hipJoint = mc.ls("Skeleton_R_Hip")

    mc.orientConstraint(pelvisControl, l_hipJoint, mo = True, n = "l_pelvis_orientConstraint_FK")
    mc.orientConstraint(pelvisControl, r_hipJoint, mo = True, n = "r_pelvis_orientConstraint_FK")

    #left leg fk
    l_hipControl_fk = mc.ls("Control_L_Hip_FK") #grabs a ref for the shoulder fk control
    l_kneeControl_fk = mc.ls("Control_L_Knee_FK")
    l_ankleControl_fk = mc.ls("Control_L_Ankle_FK") 
    l_footControl_fk = mc.ls("Control_L_FootBase_FK")

    l_hipJoint = mc.ls("Skeleton_L_Hip") #grabs a ref for the shoulder joint
    l_kneeJoint = mc.ls("Skeleton_L_Knee") 
    l_ankleJoint = mc.ls("Skeleton_L_Ankle")   
    l_footJoint = mc.ls("Skeleton_L_Foot")

    mc.parentConstraint(l_hipControl_fk, l_hipJoint, mo = True, n = "l_hip_parentConstraint_FK")
    mc.parentConstraint(l_kneeControl_fk, l_kneeJoint, mo = True, n = "l_knee_parentConstraint_FK")
    mc.parentConstraint(l_ankleControl_fk, l_ankleJoint, mo = True, n = "l_ankle_parentConstraint_FK")
    mc.parentConstraint(l_footControl_fk, l_footJoint, mo = True, n = "l_foot_parentConstraint_FK")    

    #right leg fk
    r_hipControl_fk = mc.ls("Control_R_Hip_FK") #grabs a ref for the shoulder fk control
    r_kneeControl_fk = mc.ls("Control_R_Knee_FK")
    r_ankleControl_fk = mc.ls("Control_R_Ankle_FK") 
    r_footControl_fk = mc.ls("Control_R_FootBase_FK")

    r_hipJoint = mc.ls("Skeleton_R_Hip") #grabs a ref for the shoulder joint
    r_kneeJoint = mc.ls("Skeleton_R_Knee") 
    r_ankleJoint = mc.ls("Skeleton_R_Ankle")   
    r_footJoint = mc.ls("Skeleton_R_Foot")

    mc.parentConstraint(r_hipControl_fk, r_hipJoint, mo = True, n = "r_hip_parentConstraint_FK")
    mc.parentConstraint(r_kneeControl_fk, r_kneeJoint, mo = True, n = "r_knee_parentConstraint_FK")
    mc.parentConstraint(r_ankleControl_fk, r_ankleJoint, mo = True, n = "r_ankle_parentConstraint_FK")
    mc.parentConstraint(r_footControl_fk, r_footJoint, mo = True, n = "r_foot_parentConstraint_FK") 

def toeConstraintsIK():

    #left toes ik
    l_toeamount = mc.ls("Control_L_Toe_*" + "_IK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_toeamount)):
        l_toeControl_ik = mc.ls("Control_L_Toe_" + str(i) + "_IK") 
        l_toeJoint_ik = mc.ls("Skeleton_L_Toe" + str(i)) 

        mc.orientConstraint(l_toeControl_ik, l_toeJoint_ik, mo = True, n = "Control_L_Toe_" + str(i) + "_IK_Constraint")

    #right toes ik
    r_toeamount = mc.ls("Control_R_Toe_*" + "_IK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_toeamount)):
        r_toeControl_ik = mc.ls("Control_R_Toe_" + str(i) + "_IK") 
        r_toeJoint_ik = mc.ls("Skeleton_R_Toe" + str(i)) 

        mc.orientConstraint(r_toeControl_ik, r_toeJoint_ik, mo = True, n = "Control_R_Toe_" + str(i) + "_IK_Constraint")

def toeConstraintsFK():

    #left toes
    l_toeamount = mc.ls("Control_L_Toe_*" + "_FK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(l_toeamount)):
        l_toeControl_fk = mc.ls("Control_L_Toe_" + str(i) + "_FK") 
        l_toeJoint_fk = mc.ls("Skeleton_L_Toe" + str(i)) 

        mc.orientConstraint(l_toeControl_fk, l_toeJoint_fk, mo = True, n = "Control_L_Toe_" + str(i) + "_FK_Constraint") 

    #right toes
    r_toeamount = mc.ls("Control_R_Toe_*" + "_FK", type = "transform") #if code doesn't work, try replacing the "L" in the list with an "*"

    for i in range(0, len(r_toeamount)):
        r_toeControl_fk = mc.ls("Control_R_Toe_" + str(i) + "_FK") 
        r_toeJoint_fk = mc.ls("Skeleton_R_Toe" + str(i)) 

        mc.orientConstraint(r_toeControl_fk, r_toeJoint_fk, mo = True, n = "Control_R_Toe_" + str(i) + "_FK_Constraint")

def deleteConstraints():
    selection = mc.ls("*Constraint*")
    mc.delete(selection)


#USE FOR REF LATER
#connectAttr -f nurbsCircle1.ik_fk_switch Skeleton_L_Wrist_parentConstraint1.Control_L_Wrist_FKW0;
#setAttr "Control_L_Wrist_FK.visibility" 0;