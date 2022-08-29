from audioop import add
import maya.cmds as mc
import AutoRig_Locators as locator

def IKHandles():

    #IK Group
    if mc.objExists("IK_Grp"):
        mc.confirmDialog(title = "Error", message = "IK already exists. Please create locators to be deleted", button = "OK")
        return
    else:
        mc.group(em = True, name = "IK_Grp")

    #Arm IK Handles
    mc.ikHandle(n = "IK_L_Arm", sj = "Skeleton_L_Shoulder", ee ="Skeleton_L_Wrist", sol = "ikRPsolver")
    mc.parent("IK_L_Arm", "IK_Grp")

    mc.ikHandle(n = "IK_R_Arm", sj = "Skeleton_R_Shoulder", ee ="Skeleton_R_Wrist", sol = "ikRPsolver")
    mc.parent("IK_R_Arm", "IK_Grp")

    #Leg IK Handles
    mc.ikHandle(n = "IK_L_Leg", sj = "Skeleton_L_Hip", ee ="Skeleton_L_Ankle", sol = "ikRPsolver")
    mc.parent("IK_L_Leg", "IK_Grp")

    mc.ikHandle(n = "IK_R_Leg", sj = "Skeleton_R_Hip", ee ="Skeleton_R_Ankle", sol = "ikRPsolver")
    mc.parent("IK_R_Leg", "IK_Grp")

    #Foot Handles
    #mc.ikHandle(n = "IK_L_Foot", sj = "Skeleton_L_Ankle", ee ="Skeleton_L_Foot", sol = "ikSCsolver")
    #mc.parent("IK_L_Foot", "IK_Grp")

    #mc.ikHandle(n = "IK_L_Toe", sj = "Skeleton_L_Foot", ee ="Skeleton_L_Toe0", sol = "ikSCsolver")  

    #mc.ikHandle(n = "IK_R_Foot", sj = "Skeleton_R_Ankle", ee ="Skeleton_R_Foot", sol = "ikSCsolver")
    #mc.parent("IK_R_Foot", "IK_Grp")

    #mc.ikHandle(n = "IK_R_Toe", sj = "Skeleton_R_Foot", ee ="Skeleton_R_Toe0", sol = "ikSCsolver")     

    #Toe Handles
    #leftToePos = mc.xform(mc.ls("Skeleton_L_Toe0"), q = True, t = True, ws = True)
    #rightToePos = mc.xform(mc.ls("Skeleton_R_Toe0"), q = True, t = True, ws = True)

    #leftFootPos = mc.xform(mc.ls("Skeleton_L_Foot"), q = True, t = True, ws = True)
    #rightFootPos = mc.xform(mc.ls("Skeleton_R_Foot"), q = True, t = True, ws = True)

    #leftToeIK = mc.ikHandle("IK_L_Toe", q = True, ee = True)
    #mc.move(leftFootPos[0], leftToePos[1], leftToePos[2], leftToeIK +".scalePivot", leftToeIK +".rotatePivot") #URGENT! update ik for toes to use the foot pos as ref to move the toes on the x-axis
    #mc.makeIdentity(leftToeIK, a = True, t = 1, r = 1, s = 1) #freezes transformation on the pelvis
    #mc.parent("IK_L_Toe", "IK_L_Foot", a = True)

    #rightToeIK = mc.ikHandle("IK_R_Toe", q = True, ee = True) 
    #mc.move(rightFootPos[0], rightToePos[1], rightToePos[2], rightToeIK +".scalePivot", rightToeIK +".rotatePivot") #URGENT! update ik for toes to use the foot pos as ref to move the toes on the x-axis
    #mc.makeIdentity(rightToeIK, a = True, t = 1, r = 1, s = 1) #freezes transformation on the pelvis
    #mc.parent("IK_R_Toe", "IK_R_Foot", a = True)

    # #Spine Handle
    # pelvisPos = mc.xform("Skeleton_Pelvis", q = True, t = True, ws = True)
    # spines = mc.ls("Skeleton_Spine_*", type = "joint")

    # spinePos = []

    # for i, sp in enumerate(spines):
    #     spinePos.append(mc.xform(spines[i], q = True, t = True, ws = True))

    # mc.curve(p = [(pelvisPos[0], pelvisPos[1], pelvisPos[2])], n = "Curve_Spine", d = 1)

    # for i, sp in enumerate(spinePos):
    #     mc.curve("Curve_Spine", a = True, p = [(spinePos[i][0], spinePos[i][1], spinePos[i][2])])
    
    # mc.parent("Curve_Spine", "IK_Grp")

    # curveCV = mc.ls("Curve_Spine.cv[0:]", fl = True)


    # for i, cv in enumerate(curveCV):
    #     c = mc.cluster(cv, cv, n = "Cluster_" + str(i) + "_")

    #     if i == 0:
    #         mc.parent(c, "IK_Grp")
    #     else:
    #         mc.parent(c, "Cluster_" + str(i - 1) + "_Handle")

    # mc.ikHandle(n = "IK_Spine", sj = "Skeleton_Pelvis", ee ="Skeleton_Spine_" + str((locator.mc.intField(locator.spineCount, query = True, value = True) - 1)), sol = "ikSplineSolver", c = "Curve_Spine")
    # mc.parent("IK_Spine", "IK_Grp")

def deleteIK():
    if mc.objExists("IK_Grp"):
        #grabs a list of all the IK, curves, and clusters in the outliner
        ik = mc.ls("IK*")
        #curve = mc.ls("curve*")
        Curve = mc.ls("Curve*")

        #deletes all ik in the scene
        mc.delete(ik)
        #mc.delete(curve)
        #mc.delete(Curve)

    else:
        mc.confirmDialog(title = "Error", message = "IK doesn't exist. Please create IK to be deleted", button = "OK")
        return

def resetIK():
    if mc.objExists("IK_L_Arm"):
        #grabs a list of all the IK, curves, and clusters in the outliner
        ik = mc.ls("IK*")
        curve = mc.ls("curve*")
        Curve = mc.ls("Curve*")

        #deletes all ik in the scene
        mc.delete(ik)
        mc.delete(curve)
        mc.delete(Curve)

        #creates a new set of ik handles 
        IKHandles()
    else:
        mc.confirmDialog(title = "Error", message = "IK doesn't exist. Please create IK to reset", button = "OK")
        return  

#def resetIK_UI():

    #ResetIK = resetIK()

    #window = mc.window("Reset IK")
    #mc.columnLayout(adj = True)

    #mc.separator(h = 10)
    #mc.text("Are You Sure", l = "Are you sure you want to reset the ik?")
    #mc.separator(h = 10)

    #mc.button(l = "Yes", w = 200, c = ("ResetIK")
    #mc.button(l = "No", w = 200, c = ('mc.deleteUI(\"' + window + '\", window=True)'))

    #mc.showWindow(window)  