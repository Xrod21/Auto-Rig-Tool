#Xavier Rodriguez
#Python AutoRig Tool For Maya

import maya.cmds as mc
import AutoRig_Locators as locators
import AutoRig_Joints as joints
import AutoRig_SecondaryLocators as S_locators
import AutoRig_IK as ik
import AutoRig_Controllers as controls
import AutoRig_Constraints as constraint
import AutoRig_IK_FK_Switch as switch

#Locators = reload(locators)
#Joints = reload(joints)
#S_Locators = reload(S_locators)
#IK = reload(ik)
#Controls = reload(controls)
#Constraint = reload(constraint)
#Switch = reload(switch)

#Setting Up Tool UI

#class AutoRig():

#def __init__(self):
    #self.createMainUI()

def separators():
    mc.separator(h = 10, st = "none", w = 150)
    mc.separator(h = 10, st = "none", w = 150)
    mc.separator(h = 10, st = "none", w = 150)

def createMainUI():
    mc.window("XR Auto Rig")
    mc.columnLayout(adj = True)

    mc.rowColumnLayout(nc = 3)

    separators()

    mc.separator(st = "none")
    mc.text("Settings", l = "Rig Settings")
    mc.separator(st = "none")

    separators()

    locators.createFields()

    separators()

    mc.separator(st = "none")
    mc.button(l = "Create Base Locators", w = 150, c = "locators.createLocators()")
    mc.separator(st = "none")

    separators()

    mc.separator(st = "none")
    mc.text("Edit_Locator", l = "Edit Locators")
    mc.separator(st = "none")                

    separators()

    mc.button(l = "Mirror Locators L->R", w = 150, c = "locators.mirrorLocators()") #flesh out this button to be more in line with the "mirror skin weights" tool
    mc.button(l = "Delete Locators", w = 150, c = "locators.deleteLocators()")
    mc.button(l = "Lock/Unlock Locators", w = 150, c = "locators.lockLocators(locators.editMode)")


    separators()

    mc.separator(st = "none")
    mc.text("Secondary_Locators", l = "Secondary Locators")
    mc.separator(st = "none")

    separators()

    mc.separator(st = "none")
    mc.button(l = "Secondary Locators Menu", w = 150, c = "S_locators.SecondaryLocators()")
    mc.separator(st = "none")

    separators()

    mc.separator(st = "none")
    mc.text("Skeleton", l = "Skeleton")
    mc.separator(st = "none")        

    separators()

    mc.button(l = "Create Skeleton", w = 150, c = "joints.createJoints()")
    mc.button(l = "Delete Skeleton", w = 150, c = "joints.deleteJoints()")
    mc.button(l = "Bind Skeleton", w = 150, c = "joints.bindSkin()")
    # mc.button(l = "Reset Skeleton", w = 150, c = "joints.resetJoints()")

    separators()

    # mc.separator(st = "none")
    # mc.text("IK", l = "IK")
    # mc.separator(st = "none")        

    # separators()

    # mc.button(l = "Create IK", w = 150, c = "ik.IKHandles()")
    # mc.button(l = "Delete IK", w = 150, c = "ik.deleteIK()")
    # mc.button(l = "IK/FK Switch Menu", w = 150, c = "switch.ikFKSwitch()")

    # separators()

    mc.separator(st = "none")
    mc.text("Control", l = "Controls")
    mc.separator(st = "none")        

    separators()

    mc.button(l = "Create Controls", w = 150, c = "controls.createControllers()")
    mc.button(l = "Delete Controls", w = 150, c = "controls.deleteControllers()")
    mc.button(l = "IK/FK Switch Menu", w = 150, c = "switch.ikFKSwitch()")

    # mc.button(l = "Create Constraints", w = 150, c = "constraint.createConstraints()")   

    # separators()

    # mc.separator(st = "none")
    # mc.button(l = "Delete Constraints", w = 150, c = "constraint.deleteConstraints()")  
    # mc.separator(st = "none")   

    separators()

    mc.showWindow()

createMainUI()