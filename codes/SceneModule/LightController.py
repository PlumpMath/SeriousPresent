# -*- coding:utf-8 -*-

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import PointLight
from panda3d.core import Spotlight
from panda3d.core import Light
from panda3d.core import NodePath
from panda3d.core import PerspectiveLens

AMBIENT_LIGHT     = "AmbientLight"
DIRECTIONAL_LIGHT = "DirectionalLight"
POINT_LIGHT       = "PointLight"
SPOT_LIGHT        = "SpotLight"

class LightController(object):

    def __init__(self):

        self.__lightType = [ AMBIENT_LIGHT,
                             DIRECTIONAL_LIGHT,
                             POINT_LIGHT,
                             SPOT_LIGHT ]

        self.__ambientCount = 0
        self.__directionalCount = 0
        self.__pointCount = 0
        self.__spotCount = 0

        self.__lightMap = dict()

        pass

    # 需要创建光源实例，并且封装为NodePath
    def create_light(self,
                     lightType,
                     lightColor,
                     parentNode,
                     lightPos = None,
                     lightHpr = None,
                     shadow = True,
                     target = None
                     ):

        lightNP = None
        lightId = ""

        # Ambient Light
        if lightType is self.__lightType[0]:

            self.__ambientCount += 1
            lightId += (lightType + str(self.__ambientCount))

            lightNP = self.__create_ambient_light(lightId, lightColor)

        # Directional Light
        elif lightType is self.__lightType[1]:

            self.__directionalCount += 1
            lightId += (lightType + str(self.__directionalCount))

            lightNP = self.__create_directional_light(lightId, lightColor, lightHpr)

        # Point Light
        elif lightType is self.__lightType[2]:

            self.__pointCount += 1
            lightId += (lightType + str(self.__pointCount))

            lightNP = self.__create_point_light(lightId, lightColor, lightPos)

        # Spot Light
        elif lightType is self.__lightType[3]:

            self.__spotCount += 1
            lightId += (lightType + str(self.__spotCount))

            lightNP = self.__create_spot_light(lightId, lightColor, lightPos, target, shadow)

        else:

            return None

        lightNP.reparentTo(parentNode)

        self.__lightMap[lightId] = lightNP

        return lightNP

    def set_light_to(self, lightNPOrId, target):

        if isinstance(lightNPOrId, str) and \
            lightNPOrId in self.__lightMap.keys():

            target.setLight(self.__lightMap[lightNPOrId])

            print "'%s' sets light '%s'" % (target, lightNPOrId)

        elif isinstance(lightNPOrId.node(), Light) and \
            lightNPOrId in self.__lightMap.values():

            target.setLight(lightNPOrId)

            print "'%s' sets light '%s'" % (target, lightNPOrId)

        else:

            print "'%s' fails to set light '%s'" % (target, lightNPOrId)

        # 创建Ambient Light节点
    def __create_ambient_light(self, lightId, lightColor):

        ambientLight = AmbientLight(lightId)
        ambientLight.setColor(lightColor)

        ambientLightNP = NodePath(ambientLight)

        return ambientLightNP

    # 创建Directional Light节点
    def __create_directional_light(self, lightId, lightColor, lightHpr):

        directionalLight = DirectionalLight(lightId)
        directionalLight.setColor(lightColor)

        directionalLightNP = NodePath(directionalLight)

        directionalLightNP.setHpr(lightHpr)

        return directionalLightNP

    # 创建Point Light节点
    def __create_point_light(self, lightId, lightColor, lightPos):

        pointLight = PointLight(lightId)
        pointLight.setColor(lightColor)

        pointLightNP = NodePath(pointLight)

        pointLightNP.setPos(lightPos)

        return pointLightNP

    # 创建Spot Light节点
    def __create_spot_light(self, lightId, lightColor, lightPos, target, shadow = True):

        spotLight = Spotlight(lightId)
        spotLight.setColor(lightColor)
        spotLight.setLens(PerspectiveLens())
        spotLight.setShadowCaster(shadow)

        spotLightNP = NodePath(spotLight)

        spotLightNP.setPos(lightPos)
        spotLightNP.lookAt(target)

        return spotLightNP

    def get_light(self, lightId):

        if lightId not in self.__lightMap.keys():

            return None

        else:

            return self.__lightMap[lightId]

    def get_lightId(self, light):

        for k, v in self.__lightMap.iteritems():

            if v == light:

                return k

        return None

    def print_lightInfo(self):
        print "----- The Light Info -----"
        for k, v in self.__lightMap.iteritems():
            print "%s : %s" % (k, v)
        print "--------------------"
