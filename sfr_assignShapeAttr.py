from maya import cmds
from functools import partial
from random import uniform as rand
from pprint import pprint as pretty
###generate attr on shape nodes###

class assignAttr(object):

    def __init__(self):
        self.window = 'sfr_assignAttrUI'
        self.layout = 'sfr_assignAttrLayout01'
        self.textField = 'sfr_assignAttrTxtField01'
        self.menuGrp = 'sfr_assignAttrMenuGrp'
        self.buttonAssign = 'sfr_assignAttrButton01'
        self.stripAttr = 'sfr_removeAttr'
        self.delAllAttr = 'sfr_removeAllAttr'
        self.stripAll = 'sfr_stripAll'
        self.listSpecAttr = 'sfr_listSpecAttr'
        self.listAttr = 'sfr_listAllAttr'
        self.rowLayout1 = 'sfr_addAttrrowColumnLayout1'
        self.rowLayout2 = 'sfr_addAttrrowColumnLayout2'
        self.scrollAttr = 'sfr_addAttrScroll01'
        self.scrollShap = 'sfr_addAttrScroll02'
        self.btnSelObjects = 'sfr_addAttrSelObj'
        self.checkBox = 'sfr_addAttrCheckBox'
        self.minVal = 'sfr_addAttrRandMin'
        self.maxVal = 'sfr_addAttrRandMax'
        self.renderType = 'sfr_addAttrRenderType'
        self.arn = ''
        self.X = 'X'
        self.Y = 'Y'
        self.Z = 'Z'
        self.rowLayoutFloat3 = 'sfr_rowLayoutFloat3'
        self.printType = 'sfr_printTypeBtn'
        self.float3ValX = 'sfr_float3ValX'
        self.float3ValY = 'sfr_float3ValY'
        self.float3ValZ = 'sfr_float3ValZ'
        self.useFloat3Val = 'sfr_useFloat3Val'
        self.integer = 'sfr_integerBox'
        self.copyAttrInField = 'sfr_buttonCopyAttrInTxt'
        # query UI attr

    def sfr_queryAll(self):
        # query all the UI information and call the procedure in the others
        self.attrName = cmds.textField(self.textField, q = 1, tx = 1)
        self.checkVal = cmds.checkBox(self.checkBox, q = 1, v = 1)
        self.minV = cmds.floatField(self.minVal, q = 1, v = 1)
        self.maxV = cmds.floatField(self.maxVal, q = 1, v = 1)
        self.attType = cmds.optionMenuGrp(self.menuGrp, q =1, v = 1)
        self.renderer = cmds.optionMenuGrp(self.renderType, q = 1, v = 1)
        self.float3X = cmds.floatField(self.float3ValX, q = 1, v = 1)
        self.float3Y = cmds.floatField(self.float3ValY, q = 1, v = 1)
        self.float3Z = cmds.floatField(self.float3ValZ, q = 1, v = 1)
        self.int = cmds.checkBox(self.integer, q = 1, v = 1)
        self.arn
        if self.renderer == 'arnold':
            self.arn = 'mtoa_constant_'
        else:
            self.arn = ''

        return self.float3X, self.float3Y, self.float3Z, self.int
        return self.attrName, self.checkVal, self.minV, self.maxV, self.attType, self.renderer

# this looks for every attributes existing in the scene and returns them
    def sfr_allAttr(self):
        sel = cmds.ls(ap = 1)
        rel = cmds.listRelatives(sel, f=1, ad=1, type = 'shape')
        self.objWithAttr = {}
        self.attributes = []
        for r in rel:
            attr = cmds.listAttr(r, ud = 1)
            if attr == None:
                continue
            for a in attr:
                if self.X in a or self.Y in a or self.Z in a:
                    continue
                if not a in self.attributes:
                    self.attributes.append(a)

        for r in rel:
            attr = cmds.listAttr(r, ud = 1)
            if attr == None:
                continue
            for a in attr:
                if self.X in a or self.Y in a or self.Z in a:
                    continue
                if not a in self.objWithAttr.keys():
                    self.objWithAttr[a] = {'obj' : [r] }
                else:
                    self.objWithAttr[a]['obj'].append(r)
        
        return self.attributes
        return self.objWithAttr


# this part defines all the procedures to add attributes based on type

    def sfr_addFloatAttr(self):
        self.sfr_queryAll()
        self.checkVal = cmds.checkBox(self.checkBox, q = 1, v = 1)
        self.int = cmds.checkBox(self.integer, q = 1, v = 1)
        sel = cmds.ls(sl=1)
        rel = cmds.listRelatives(sel, f = 1 , ad = 1, type = 'shape')
        attrStart = []
        for r in rel:
            if not self.int == 1:
                randomV = rand(self.minV, self.maxV)
            else:
                randomV = int(rand(self.minV, self.maxV))
            if not cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)):
                if not self.checkVal == 1:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'float', dv = 0.000)
                else:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'float', dv = 0.000)
                    cmds.setAttr('%s.%s%s' % (r, self.arn, self.attrName), randomV)
            elif cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)) and self.checkVal == 1:
                cmds.setAttr('%s.%s%s' % (r, self.arn, self.attrName), randomV)
            else:
                cmds.warning('%s attribute already exists on this object' % (self.attrName,))

    def sfr_turnOffCheckVam(self,args):
        self.checkVal = cmds.checkBox(self.checkBox, q = 1, v = 1)
        if not self.checkVal == 0:
            cmds.checkBox(self.checkBox, e = 1, v = 0)

    def sfr_turnOffFloat3(self,args):
        self.checkFloat3 = cmds.checkBox(self.useFloat3Val, q = 1 , v = 1)
        if not self.checkFloat3 == 0:
            cmds.checkBox(self.useFloat3Val, e = 1, v = 0)

    def sfr_addFloat3Attr(self):
        self.sfr_queryAll()
        self.checkVal = cmds.checkBox(self.checkBox, q = 1, v = 1)
        self.checkFloat3 = cmds.checkBox(self.useFloat3Val, q = 1 , v = 1)
        self.int = cmds.checkBox(self.integer, q = 1, v = 1)
        sel = cmds.ls(sl=1)
        rel = cmds.listRelatives(sel, f = 1 , ad = 1, type = 'shape')
        for r in rel:
            if not self.int == 1:
                randomR = rand(self.minV, self.maxV)
                randomG = rand(self.minV, self.maxV)
                randomB = rand(self.minV, self.maxV)
            else:
                randomR = int(rand(self.minV, self.maxV))
                randomG = int(rand(self.minV, self.maxV))
                randomB = int(rand(self.minV, self.maxV))
            if not cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)):
                if not self.checkVal == 1 and self.checkFloat3 == 0:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'float3')
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.X), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Y), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Z), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                elif not self.checkVal == 1 and self.checkFloat3 == 1:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'float3')
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.X), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Y), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Z), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.X), self.float3X)
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Y), self.float3Y)
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Z), self.float3Z)                    
                else:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'float3')
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.X), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Y), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Z), at = 'float', p = '%s%s' % (self.arn, self.attrName))
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.X), randomR)
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Y), randomG)
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Z), randomB)
            elif cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)) and self.checkVal == 1 and self.checkFloat3 == 0:
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.X), randomR)
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Y), randomG)
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Z), randomB)
            elif cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)) and self.checkVal == 0 and self.checkFloat3 == 1:
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.X), self.float3X)
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Y), self.float3Y)
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Z), self.float3Z)
            else:
                cmds.warning('%s attribute already exists on this object' % (self.attrName,))

    def sfr_addBoolAttr(self):
        self.sfr_queryAll()
        sel = cmds.ls(sl = 1)
        rel = cmds.listRelatives(sel, f = 1, ad = 1, type = 'shape')
        for r in rel:
            if not cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)):
                cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'bool')
            else:
                cmds.warning('%s attribute already exists on this object' % (self.attrName,))

    def sfr_addVectorAttr(self):
        self.sfr_queryAll()
        self.checkVal = cmds.checkBox(self.checkBox, q = 1, v = 1)
        self.int = cmds.checkBox(self.integer, q = 1, v = 1)
        sel = cmds.ls(sl = 1)
        rel = cmds.listRelatives(sel, f = 1, ad = 1, type = 'shape')
        for r in rel:
            if not self.int == 1:
                randomR = rand(self.minV, self.maxV)
                randomG = rand(self.minV, self.maxV)
                randomB = rand(self.minV, self.maxV)
            else:
                randomR = int(rand(self.minV, self.maxV))
                randomG = int(rand(self.minV, self.maxV))
                randomB = int(rand(self.minV, self.maxV))
            if not cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)):
                if not self.checkVal == 1:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'double3')
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.X), at = 'double', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Y), at = 'double', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Z), at = 'double', p = '%s%s' % (self.arn, self.attrName))
                else:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'double3')
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.X), at = 'double', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Y), at = 'double', p = '%s%s' % (self.arn, self.attrName))
                    cmds.addAttr(r, ln = '%s%s%s' % (self.arn, self.attrName, self.Z), at = 'double', p = '%s%s' % (self.arn, self.attrName))
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.X), randomR)
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Y), randomG)
                    cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Z), randomB)
            elif cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)) and self.checkVal == 1:
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.X), randomR)
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Y), randomG)
                cmds.setAttr('%s.%s%s%s' % (r,self.arn,self.attrName,self.Z), randomB)
            else:
                cmds.warning('%s attribute already exists on this object' % (self.attrName,))

    def sfr_addInteger(self):
        self.sfr_queryAll()
        self.checkVal = cmds.checkBox(self.checkBox, q = 1, v =1)
        sel = cmds.ls( sl = 1)
        rel = cmds.listRelatives(sel, f = 1, ad = 1, type = 'shape')
        for r in rel:
            randomNumber = int(rand(self.minV, self.maxV))
            if not cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)):
                if not self.checkVal == 1:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'long')
                else:
                    cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), at = 'long')
                    cmds.setAttr('%s.%s%s' % (r,self.arn, self.attrName), randomNumber)
            elif cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)) and self.checkVal == 1:
                cmds.setAttr('%s.%s%s' % (r,self.arn, self.attrName), randomNumber)
            else:
                cmds.warning('%s attribute already exists on this object' % (self.attrName,))                

    def sfr_addStringAttr(self):
        self.sfr_queryAll()
        self.checkVal = cmds.checkBox(self.checkBox, q = 1, v =1)
        sel = cmds.ls( sl = 1)
        rel = cmds.listRelatives(sel, f = 1, ad = 1, type = 'shape')
        for r in rel:
            if not cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)):
                cmds.addAttr(r, ln = '%s%s' % (self.arn, self.attrName), dt = 'string')
            else:
                cmds.warning('%s attribute already exists on this object' % (self.attrName,))


# this part defines the procedures to add commands to buttons
    def sfr_assignGivenAttr(self, args):
        self.sfr_queryAll()
        sel = cmds.ls(sl=1)
        #get shape node
        rel = cmds.listRelatives(sel, f = 1, ad = 1, type = 'mesh')
        print self.attrName, self.checkVal, self.minV, self.maxV, self.attType, self.renderer
        if self.attType == 'float':
            self.sfr_addFloatAttr()
        elif self.attType == 'float3':
            self.sfr_addFloat3Attr()
        elif self.attType == 'vector':
            self.sfr_addVectorAttr()
        elif self.attType == 'integer':
            self.sfr_addInteger()
        elif self.attType == 'boolean':
            self.sfr_addBoolAttr()
        elif self.attType == 'string':
            self.sfr_addStringAttr()

    def sfr_deleteAttrFromSel(self,args):
        self.sfr_queryAll()
        sel = cmds.ls(sl=1)
        rel = cmds.listRelatives(sel, f = 1 , ad = 1, type = 'shape')
        for r in rel:
            if cmds.objExists('%s.%s%s' % (r, self.arn, self.attrName)):
                cmds.deleteAttr('%s.%s%s' % (r, self.arn, self.attrName))

    def sfr_deleteAttrWNameInScene(self,args):
        # this delete the attribute specified in the text field
        #to delete from everything in the scene
        self.sfr_queryAll()
        self.sfr_allAttr()
        sel = cmds.ls(ap = 1)
        rel = cmds.listRelatives(sel, f = 1, ad = 1, type = 'shape')
        for a in self.attributes:
            for r in rel:
                if cmds.objExists('%s.%s' % (r,a)) and self.attrName in a:
                    cmds.deleteAttr('%s.%s' % (r,a))

    def sfr_stripAllAttrInScene(self,args):
        # delete every existing attributes in the scene
        self.sfr_queryAll()
        self.sfr_allAttr()
        sel = cmds.ls(ap = 1)
        rel = cmds.listRelatives(sel, f = 1, ad = 1, type = 'shape')
        objWithAttr = []
        for a in self.attributes:
            for r in rel:
                if cmds.objExists('%s.%s' % (r,a)):
                    cmds.deleteAttr('%s.%s' % (r,a))

    
    def sfr_appendAttr(self,args):
        #list all attributes in scene and append to scroll List
        self.sfr_queryAll()
        self.sfr_allAttr()
        cmds.textScrollList(self.scrollAttr, e = 1, ra =1)
        for a in self.attributes:
            cmds.textScrollList(self.scrollAttr, e = 1, a = a)

    def sfr_appendObject(self):
        self.sfr_queryAll()
        self.sfr_allAttr()
        # query selected item in scrollList
        attrSel = cmds.textScrollList(self.scrollAttr, q = 1, si = 1)
        #clean possible items
        cmds.textScrollList(self.scrollShap, e = 1, ra =1)
        objects = []
        for k, v in self.objWithAttr.iteritems():
            if attrSel[0] in k:
                for el in v['obj']:
                    objects.append(el)
        for o in objects:
            transform = '|'.join(o.split('|')[:-1])
            cmds.textScrollList(self.scrollShap, e = 1 , a = transform)
            
    def sfr_selectObjInList(self, args):
        objects = cmds.textScrollList(self.scrollShap, q = 1, si = 1)
        cmds.select(objects)

    def sfr_printThatSucker(self, args):
        self.sfr_queryAll()
        self.sfr_allAttr()
        if self.renderer == 'arnold':
            attrSel = 'mtoa_constant_%s' % (cmds.textField(self.textField, q = 1, tx = 1))
        else:
            attrSel = (cmds.textField(self.textField, q = 1, tx = 1))

        obj = cmds.ls(sl = 1)
        rel = cmds.listRelatives(obj,f=1,ad=1, type = 'shape')
        for r in rel:
            if cmds.objExists('%s.%s' % (r,attrSel)):
                attr = cmds.getAttr('%s.%s' % (r,attrSel), type =1 )
                if 'double' in attr:
                    print '%s is a FUCKING DOUBLE' % (attrSel)
                else:
                    print '%s is ok. You cool bro' % (attrSel)
            else:
                print '%s.%s does not exists' % (r,attrSel)

    def sfr_copyAttrInField(self, args):
        self.sfr_queryAll()
        self.sfr_allAttr()
        selectedAttr = cmds.textScrollList(self.scrollAttr, q = 1, si = 1)
        if self.renderer == 'arnold':
            theAttr = selectedAttr[0].split(self.arn)[-1]
            cmds.textField(self.textField, e = 1, tx = theAttr )
        else:
            cmds.textField(self.textField, e = 1, tx = selectedAttr[0])

# this part defines the UI of the script
    def assignAttrUI(self):
        width = 550
        if cmds.window(self.window, q = 1, ex = 1):
            cmds.deleteUI(self.window, window = 1)
        cmds.window(self.window, w = width, h = width)
        cmds.columnLayout(self.layout, w = width, adj = 1)
        cmds.optionMenuGrp(self.renderType, l = 'renderer')
        cmds.menuItem('arnold')
        cmds.menuItem('prman')
        cmds.text('give a name to your attr', rs = 1)
        cmds.textField(self.textField, tx = 'myAttr')
        cmds.text('attr type')

        cmds.optionMenuGrp(self.menuGrp, l = 'type')
        cmds.menuItem('float')
        cmds.menuItem('float3')
        cmds.menuItem('boolean')
        cmds.menuItem('integer')
        cmds.menuItem('vector')
        cmds.menuItem('string')

        cmds.checkBox(self.checkBox, l = 'assign random value', onc = partial(self.sfr_turnOffFloat3))
        cmds.checkBox(self.integer, l = 'integer')
        cmds.text('minimum value',w=50)

        cmds.floatField(self.minVal, v= 0.0)
        cmds.text('maximum value',w=50)
        cmds.floatField(self.maxVal, v=1.0)
        cmds.separator('sfr_aattrSep02', h = 15, p = self.layout)

        cmds.checkBox(self.useFloat3Val, l = 'use rgb values', v = 0, onc = partial(self.sfr_turnOffCheckVam))
        cmds.rowColumnLayout(self.rowLayoutFloat3, nc = 3, p = self.layout)
        cmds.floatField(self.float3ValX, v = 0.180, w = (width*0.33), p = self.rowLayoutFloat3)
        cmds.floatField(self.float3ValY, v = 0.180, w = (width*0.33), p = self.rowLayoutFloat3)
        cmds.floatField(self.float3ValZ, v = 0.180, w = (width*0.33), p = self.rowLayoutFloat3)
        cmds.separator('sfr_rowLayout3Sep', h =15, w = width, p = self.layout)

        cmds.button(self.buttonAssign, l = 'add attribute to sel', c = partial(self.sfr_assignGivenAttr), p = self.layout)
        cmds.button(self.stripAttr, l = 'delete attr from sel', c = partial(self.sfr_deleteAttrFromSel), p = self.layout)
        cmds.button(self.delAllAttr, l = 'delete all attr with name in scene', c = partial(self.sfr_deleteAttrWNameInScene), p = self.layout)
        cmds.button(self.stripAll, l = 'delete every attr', c = partial(self.sfr_stripAllAttrInScene), p = self.layout)

        cmds.separator('sfr_aattrSep01', h = 15, p = self.layout)
        cmds.button(self.listAttr, l = 'list every attr in scene', c = partial(self.sfr_appendAttr),h = 40, p = self.layout )
        #cmds.button(self.listSpecAttr, l = 'list shapes with sel attr in scene', c = partial(self.sfr_appendObject), h = 40, p = self.layout)
        cmds.rowColumnLayout(self.rowLayout2, nc = 2, w = width, p = self.layout)
        cmds.text('attr list')
        cmds.text('object list')
        cmds.textScrollList(self.scrollAttr, ams = 0, sc = partial(self.sfr_appendObject))
        cmds.textScrollList(self.scrollShap, ams = 1)
        cmds.button(self.btnSelObjects, l = 'select objects in list', c = partial(self.sfr_selectObjInList), p = self.layout, h = 40)
        cmds.separator('printFuckingType', h = 15, w = 200)
        cmds.button(self.printType, l = 'print that type sucker', c= partial(self.sfr_printThatSucker),p = self.layout)
        cmds.button(self.copyAttrInField, l = 'copy selected attr in text field', c = partial(self.sfr_copyAttrInField), p = self.layout)
        cmds.showWindow(self.window)
