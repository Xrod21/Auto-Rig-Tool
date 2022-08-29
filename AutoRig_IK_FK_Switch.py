
import maya.cmds as mc

class ikFKSwitch():

    def __init__(self):
        self.CreateSwitchWindow()

    def CreateSwitchWindow(self):

        mc.window("IK/FK Switch")
        mc.rowColumnLayout(nc = 3)

        def separators():
            mc.separator(h = 10, w = 100, st = "none")
            mc.separator(h = 10, w = 100, st = "none")
            mc.separator(h = 10, w = 100, st = "none")

        separators()

        mc.text("IK/FK Switch", l = "IK/FK Switch")

        self.switchChoice = mc.radioCollection("SwitchCollection")
        mc.radioButton("IK", l = "IK", w = 100,)
        mc.radioButton("FK", l = "FK", w = 100,)

        separators()

        mc.separator(h = 10, st = "none")
        mc.button(l = "Set Kinematics", w = 100, c = self.setKinematics)
        mc.separator(h = 10, st = "none")

        separators()

        mc.showWindow()

    def setKinematics(self, void):
        
        switchChoice = mc.radioCollection("SwitchCollection", q = True, sl = True)

        if switchChoice != "IK" and switchChoice != "FK":
            mc.confirmDialog(title = "No Kinematic Selected", message = "Please Select IK or FK to change Kinematic", button = "OK")
            return

        if switchChoice == "IK":

            #parent the left fingers to the ik wrist controller 

            # l_fingerList = mc.ls("Control_L_Finger_*_0_IK", type = "transform")
            # mc.parent(l_fingerList, w = True)
            # mc.parent(l_fingerList, "Control_L_Wrist_IK")

            #setting IK controls visible
            #left arm controls
            mc.setAttr("Control_L_Wrist_IK.visibility", 1)
            mc.setAttr("Control_L_Elbow_IK.visibility", 1)

            #left arm constraint
            mc.setAttr("l_wrist_orientConstraint_IK.Control_L_Wrist_IKW0", 1) #connected to joint skeleton 

            mc.setAttr("l_wrist_pointConstraint_IK.Control_L_Wrist_IKW0", 1) #connected to ik handle
            mc.setAttr("l_elbow_poleConstraint_IK.Control_L_Elbow_IKW0", 1) #connected to ik handle

            #left finger constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)
            l_fingeramount = mc.ls("Control_L_Finger_*_0_IK", type = "transform")

            for i in range(0, len(l_fingeramount)):
                for j in range(0,3):  
                    #changing visibilty of left control fingers               
                    l_fingercontrol_ik = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_IK.visibility", 1)
                    l_fingercontrol_fk = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_FK.visibility", 0)

                    #changing weight of left control fingers  
                    l_fingerconstraint_ik = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_L_Finger_" + str(i) + "_" + str(j) + "_IKW0", 1)
                    l_fingerconstraint_fk = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_L_Finger_" + str(i) + "_" + str(j) + "_FKW1", 0)           

            #left arm ik handle
            mc.setAttr("IK_L_Arm.ikBlend", 1) #setting the weight of the ik handle itself

            #parent the right fingers to the ik wrist controller 
            r_fingerList = mc.ls("Control_R_Finger_*_0_IK", type = "transform")
            mc.parent(r_fingerList, w = True)
            mc.parent(r_fingerList, "Control_R_Wrist_IK")

            #right arm control
            mc.setAttr("Control_R_Wrist_IK.visibility", 1)
            mc.setAttr("Control_R_Elbow_IK.visibility", 1)

            #right arm constraint
            mc.setAttr("r_wrist_orientConstraint_IK.Control_R_Wrist_IKW0", 1) #connected to joint skeleton 

            mc.setAttr("r_wrist_pointConstraint_IK.Control_R_Wrist_IKW0", 1) #connected to ik handle
            mc.setAttr("r_elbow_poleConstraint_IK.Control_R_Elbow_IKW0", 1) #connected to ik handle

            #right finger constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)
            r_fingeramount = mc.ls("Control_R_Finger_*_0_IK", type = "transform")

            for i in range(0, len(r_fingeramount)):
                for j in range(0,3):
                    #changing visibilty of right control fingers
                    r_fingercontrol_ik = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_IK.visibility", 1)
                    r_fingercontrol_fk = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_FK.visibility", 0)

                    #changing weight of right control fingers 
                    r_fingerconstraint_ik = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_R_Finger_" + str(i) + "_" + str(j) + "_IKW0", 1)
                    r_fingerconstraint_fk = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_R_Finger_" + str(i) + "_" + str(j) + "_FKW1", 0)           

            #right arm ik handle
            mc.setAttr("IK_R_Arm.ikBlend", 1) #setting the weight of the ik handle itself

            #left leg control ik
            mc.setAttr("Control_L_Ankle_IK.visibility", 1)
            mc.setAttr("Control_L_Knee_IK.visibility", 1)

            #left leg constraint ik
            mc.setAttr("l_ankle_orientConstraint_IK.Control_L_Ankle_IKW0", 1)

            mc.setAttr("l_ankle_pointConstraint_IK.Control_L_Ankle_IKW0", 1) #connected to ik handle
            mc.setAttr("l_knee_poleConstraint_IK.Control_L_Knee_IKW0", 1) #connected to ik handle

            #left toe constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)
            l_toeamount = mc.ls("Control_L_Toe_*_IK", type = "transform")

            for i in range(0, len(l_toeamount)):
                #changing visibilty of left control toes            
                l_toecontrol_ik = mc.setAttr("Control_L_Toe_" + str(i) + "_IK.visibility", 1)
                l_toecontrol_fk = mc.setAttr("Control_L_Toe_" + str(i) + "_FK.visibility", 0)

                #changing weight of left control toes 
                l_toeconstraint_ik = mc.setAttr("Control_L_Toe_" + str(i) + "_FK_Constraint.Control_L_Toe_" + str(i) + "_IKW0", 1)
                l_toeconstraint_fk = mc.setAttr("Control_L_Toe_" + str(i) + "_FK_Constraint.Control_L_Toe_" + str(i) + "_FKW1", 0)           

            #left leg ik handle
            mc.setAttr("IK_L_Leg.ikBlend", 1) #setting the weight of the ik handle itself

            #right leg control ik
            mc.setAttr("Control_R_Ankle_IK.visibility", 1)
            mc.setAttr("Control_R_Knee_IK.visibility", 1)

            #right leg constraint ik
            mc.setAttr("r_ankle_orientConstraint_IK.Control_R_Ankle_IKW0", 1)

            mc.setAttr("r_ankle_pointConstraint_IK.Control_R_Ankle_IKW0", 1) #connected to ik handle
            mc.setAttr("r_knee_poleConstraint_IK.Control_R_Knee_IKW0", 1) #connected to ik handle

            #right toe constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)
            r_toeamount = mc.ls("Control_R_Toe_*_IK", type = "transform")

            for i in range(0, len(r_toeamount)):
                #changing visibilty of right control toes            
                r_toecontrol_ik = mc.setAttr("Control_R_Toe_" + str(i) + "_IK.visibility", 1)
                r_toecontrol_fk = mc.setAttr("Control_R_Toe_" + str(i) + "_FK.visibility", 0)

                #changing weight of right control toes
                r_toeconstraint_ik = mc.setAttr("Control_R_Toe_" + str(i) + "_FK_Constraint.Control_R_Toe_" + str(i) + "_IKW0", 1)
                r_toeconstraint_fk = mc.setAttr("Control_R_Toe_" + str(i) + "_FK_Constraint.Control_R_Toe_" + str(i) + "_FKW1", 0)

            #right leg ik handle
            mc.setAttr("IK_R_Leg.ikBlend", 1) #connected to ik handle

            #setting FK controls invisible
            #left arm control 
            mc.setAttr("Control_L_Wrist_FK.visibility", 0)
            mc.setAttr("Control_L_Elbow_FK.visibility", 0)
            mc.setAttr("Control_L_Shoulder_FK.visibility", 0)

            #left arm constraint
            mc.setAttr("l_wrist_parentConstraint_FK.Control_L_Wrist_FKW0", 0)
            mc.setAttr("l_elbow_parentConstraint_FK.Control_L_Elbow_FKW0", 0)
            mc.setAttr("l_shoulder_parentConstraint_FK.Control_L_Shoulder_FKW0", 0)

            #right arm control
            mc.setAttr("Control_R_Wrist_FK.visibility", 0)
            mc.setAttr("Control_R_Elbow_FK.visibility", 0)
            mc.setAttr("Control_R_Shoulder_FK.visibility", 0)

            #right arm constraint
            mc.setAttr("r_wrist_parentConstraint_FK.Control_R_Wrist_FKW0", 0)
            mc.setAttr("r_elbow_parentConstraint_FK.Control_R_Elbow_FKW0", 0)
            mc.setAttr("r_shoulder_parentConstraint_FK.Control_R_Shoulder_FKW0", 0)

            #left leg control
            mc.setAttr("Control_L_Hip_FK.visibility", 0)
            mc.setAttr("Control_L_Knee_FK.visibility", 0)
            mc.setAttr("Control_L_Ankle_FK.visibility", 0)
            mc.setAttr("Control_L_FootBase_FK.visibility", 0)

            #left leg constraint fk #IF THINGS BREAK GET RID OF THIS CODE (ABORT)
            mc.setAttr("l_hip_parentConstraint_FK.Control_L_Hip_FKW0", 0)
            mc.setAttr("l_pelvis_orientConstraint_FK.Control_PelvisW0", 0)
            mc.setAttr("l_knee_parentConstraint_FK.Control_L_Knee_FKW0", 0)
            mc.setAttr("l_ankle_parentConstraint_FK.Control_L_Ankle_FKW0", 0)
            mc.setAttr("l_foot_parentConstraint_FK.Control_L_FootBase_FKW0", 0)

            #right leg control
            mc.setAttr("Control_R_Hip_FK.visibility", 0)
            mc.setAttr("Control_R_Knee_FK.visibility", 0)
            mc.setAttr("Control_R_Ankle_FK.visibility", 0)
            mc.setAttr("Control_R_FootBase_FK.visibility", 0)

            #right leg constraint fk #IF THINGS BREAK GET RID OF THIS CODE (ABORT)
            mc.setAttr("r_hip_parentConstraint_FK.Control_R_Hip_FKW0", 0)
            mc.setAttr("r_pelvis_orientConstraint_FK.Control_PelvisW0", 0)
            mc.setAttr("r_knee_parentConstraint_FK.Control_R_Knee_FKW0", 0)
            mc.setAttr("r_ankle_parentConstraint_FK.Control_R_Ankle_FKW0", 0)
            mc.setAttr("r_foot_parentConstraint_FK.Control_R_FootBase_FKW0", 0)

        elif switchChoice == "FK":

            #parent the left fingers to the fk wrist controller 

            l_fingerList = mc.ls("Control_L_Finger_*_0_IK", type = "transform")
            mc.parent(l_fingerList, w = True)
            mc.parent(l_fingerList, "Control_L_Wrist_IK")

            #setting FK controls visible
            #left arm control
            mc.setAttr("Control_L_Wrist_FK.visibility", 1)
            mc.setAttr("Control_L_Elbow_FK.visibility", 1)
            mc.setAttr("Control_L_Shoulder_FK.visibility", 1)

            #left arm constraint
            mc.setAttr("l_wrist_parentConstraint_FK.Control_L_Wrist_FKW0", 1)
            mc.setAttr("l_elbow_parentConstraint_FK.Control_L_Elbow_FKW0", 1)
            mc.setAttr("l_shoulder_parentConstraint_FK.Control_L_Shoulder_FKW0", 1)

            #left finger constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)

            l_fingeramount = mc.ls("Control_L_Finger_*_0_IK", type = "transform")

            for i in range(0, len(l_fingeramount)):
                for j in range(0,3):  
                    #changing visibilty of left control fingers               
                    l_fingercontrol_ik = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_IK.visibility", 0)
                    l_fingercontrol_fk = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_FK.visibility", 1)

                    #changing weight of left control fingers  
                    l_fingerconstraint_ik = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_L_Finger_" + str(i) + "_" + str(j) + "_IKW0", 0)
                    l_fingerconstraint_fk = mc.setAttr("Control_L_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_L_Finger_" + str(i) + "_" + str(j) + "_FKW1", 1)           

            #right arm control
            mc.setAttr("Control_R_Wrist_FK.visibility", 1)
            mc.setAttr("Control_R_Elbow_FK.visibility", 1)
            mc.setAttr("Control_R_Shoulder_FK.visibility", 1)

            #right arm constraint
            mc.setAttr("r_wrist_parentConstraint_FK.Control_R_Wrist_FKW0", 1)
            mc.setAttr("r_elbow_parentConstraint_FK.Control_R_Elbow_FKW0", 1)
            mc.setAttr("r_shoulder_parentConstraint_FK.Control_R_Shoulder_FKW0", 1)

            #right finger constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)

            r_fingeramount = mc.ls("Control_R_Finger_*_0_IK", type = "transform")

            for i in range(0, len(r_fingeramount)):
                for j in range(0,3):
                    #changing visibilty of right control fingers
                    r_fingercontrol_ik = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_IK.visibility", 0)
                    r_fingercontrol_fk = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_FK.visibility", 1)

                    #changing weight of right control fingers 
                    r_fingerconstraint_ik = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_R_Finger_" + str(i) + "_" + str(j) + "_IKW0", 0)
                    r_fingerconstraint_fk = mc.setAttr("Control_R_Finger_" + str(i) + "_" + str(j) + "_FK_Constraint.Control_R_Finger_" + str(i) + "_" + str(j) + "_FKW1", 1)           

            #left leg control
            mc.setAttr("Control_L_Hip_FK.visibility", 1)
            mc.setAttr("Control_L_Knee_FK.visibility", 1)
            mc.setAttr("Control_L_Ankle_FK.visibility", 1)
            mc.setAttr("Control_L_FootBase_FK.visibility", 1)

            #left leg constraint fk #IF THINGS BREAK GET RID OF THIS CODE (ABORT)
            mc.setAttr("l_hip_parentConstraint_FK.Control_L_Hip_FKW0", 1)
            mc.setAttr("l_pelvis_orientConstraint_FK.Control_PelvisW0", 1)
            mc.setAttr("l_knee_parentConstraint_FK.Control_L_Knee_FKW0", 1)
            mc.setAttr("l_ankle_parentConstraint_FK.Control_L_Ankle_FKW0", 1)
            mc.setAttr("l_foot_parentConstraint_FK.Control_L_FootBase_FKW0", 1)

            #left toe constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)

            l_toeamount = mc.ls("Control_L_Toe_*_IK", type = "transform")

            for i in range(0, len(l_toeamount)):
                #changing visibilty of left control toes            
                l_toecontrol_ik = mc.setAttr("Control_L_Toe_" + str(i) + "_IK.visibility", 0)
                l_toecontrol_fk = mc.setAttr("Control_L_Toe_" + str(i) + "_FK.visibility", 1)

                #changing weight of left control toes
                l_toeconstraint_ik = mc.setAttr("Control_L_Toe_" + str(i) + "_FK_Constraint.Control_L_Toe_" + str(i) + "_IKW0", 0)
                l_toeconstraint_fk = mc.setAttr("Control_L_Toe_" + str(i) + "_FK_Constraint.Control_L_Toe_" + str(i) + "_FKW1", 1)           

            #right leg control
            mc.setAttr("Control_R_Hip_FK.visibility", 1)
            mc.setAttr("Control_R_Knee_FK.visibility", 1)
            mc.setAttr("Control_R_Ankle_FK.visibility", 1)
            mc.setAttr("Control_R_FootBase_FK.visibility", 1)

            #right leg constraint fk #IF THINGS BREAK GET RID OF THIS CODE (ABORT)
            mc.setAttr("r_hip_parentConstraint_FK.Control_R_Hip_FKW0", 1)
            mc.setAttr("r_pelvis_orientConstraint_FK.Control_PelvisW0", 1)
            mc.setAttr("r_knee_parentConstraint_FK.Control_R_Knee_FKW0", 1)
            mc.setAttr("r_ankle_parentConstraint_FK.Control_R_Ankle_FKW0", 1)
            mc.setAttr("r_foot_parentConstraint_FK.Control_R_FootBase_FKW0", 1)

            #right toe constraint IK And FK (We're affecting the ik with the fk constraint since it contains the ik attr)

            r_toeamount = mc.ls("Control_R_Toe_*_IK", type = "transform")

            for i in range(0, len(r_toeamount)):
                #changing visibilty of right control toes            
                r_toecontrol_ik = mc.setAttr("Control_R_Toe_" + str(i) + "_IK.visibility", 0)
                r_toecontrol_fk = mc.setAttr("Control_R_Toe_" + str(i) + "_FK.visibility", 1)

                #changing weight of right control toes
                r_toeconstraint_ik = mc.setAttr("Control_R_Toe_" + str(i) + "_FK_Constraint.Control_R_Toe_" + str(i) + "_IKW0", 0)
                r_toeconstraint_fk = mc.setAttr("Control_R_Toe_" + str(i) + "_FK_Constraint.Control_R_Toe_" + str(i) + "_FKW1", 1)

            #setting IK controls invisible
            #left arm controls
            mc.setAttr("Control_L_Wrist_IK.visibility", 0)
            mc.setAttr("Control_L_Elbow_IK.visibility", 0)

            #left arm constraint
            mc.setAttr("l_wrist_orientConstraint_IK.Control_L_Wrist_IKW0", 0) #connected to joint skeleton 

            mc.setAttr("l_wrist_pointConstraint_IK.Control_L_Wrist_IKW0", 0) #connected to ik handle
            mc.setAttr("l_elbow_poleConstraint_IK.Control_L_Elbow_IKW0", 0) #connected to ik handle

            #left arm ik handle
            mc.setAttr("IK_L_Arm.ikBlend", 0) #connected to ik handle

            #right arm control
            mc.setAttr("Control_R_Wrist_IK.visibility", 0)
            mc.setAttr("Control_R_Elbow_IK.visibility", 0)

            #right arm constraint
            mc.setAttr("r_wrist_orientConstraint_IK.Control_R_Wrist_IKW0", 0) #connected to joint skeleton 

            mc.setAttr("r_wrist_pointConstraint_IK.Control_R_Wrist_IKW0", 0) #connected to ik handle
            mc.setAttr("r_elbow_poleConstraint_IK.Control_R_Elbow_IKW0", 0) #connected to ik handle

            #right arm ik handle
            mc.setAttr("IK_R_Arm.ikBlend", 0) #connected to ik handle

            #left leg control
            mc.setAttr("Control_L_Ankle_IK.visibility", 0)
            mc.setAttr("Control_L_Knee_IK.visibility", 0)

            #left leg constraint
            mc.setAttr("l_ankle_orientConstraint_IK.Control_L_Ankle_IKW0", 0)

            mc.setAttr("l_ankle_pointConstraint_IK.Control_L_Ankle_IKW0", 0) #connected to ik handle
            mc.setAttr("l_knee_poleConstraint_IK.Control_L_Knee_IKW0", 0) #connected to ik handle

            #left leg ik handle
            mc.setAttr("IK_L_Leg.ikBlend", 0) #connected to ik handle

            #right leg control
            mc.setAttr("Control_R_Ankle_IK.visibility", 0)
            mc.setAttr("Control_R_Knee_IK.visibility", 0)

            #right leg constraint
            mc.setAttr("r_ankle_orientConstraint_IK.Control_R_Ankle_IKW0", 0)

            mc.setAttr("r_ankle_pointConstraint_IK.Control_R_Ankle_IKW0", 0) #connected to ik handle
            mc.setAttr("r_knee_poleConstraint_IK.Control_R_Knee_IKW0", 0) #connected to ik handle

            #right leg ik handle
            mc.setAttr("IK_R_Leg.ikBlend", 0) #connected to ik handle