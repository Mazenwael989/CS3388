''' CS3388 Assignment #2     Mazen Baioumy 250924925  |  Creates a graphics window filled with objects of each of the parametric classes '''

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

'''                     cameraMatrix  Class                                                                          '''

class cameraMatrix:

    def __init__(self, UP, E, G, nearPlane=10.0, farPlane=50.0, width=640, height=480, theta=90.0):
        __Mp = self.__setMp(nearPlane, farPlane)
        __T1 = self.__setT1(nearPlane, theta, width / height)
        __S1 = self.__setS1(nearPlane, theta, width / height)
        __T2 = self.__setT2()
        __S2 = self.__setS2(width, height)
        __W2 = self.__setW2(height)

        self.__UP = UP.normalize()
        self.__N = (E - G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).transpose().crossProduct(self.__N.transpose()).normalize().transpose()
        self.__V = self.__N.transpose().crossProduct(self.__U.transpose()).transpose()
        self.__Mv = self.__setMv(self.__U, self.__V, self.__N, E)
        self.__C = __W2 * __S2 * __T2 * __S1 * __T1 * __Mp
        self.__M = self.__C * self.__Mv

    def __setMv(self, U, V, N, E):
        __Mv = matrix(np.zeros((4, 4)))  # Start by making Mv a 0 matrix
        negE = E.scalarMultiply(-1) #Get -1*E for dot product calculations
        #Set each element row by row
        __Mv.set(0, 0, U.get(0, 0))
        __Mv.set(0, 1, U.get(1, 0))
        __Mv.set(0, 2, U.get(2, 0))
        __Mv.set(0, 3, (negE.get(0,0)*U.get(0,0) + negE.get(1,0)*U.get(1,0) + negE.get(2,0)*U.get(2,0)))  #Set to -1*E dot U

        __Mv.set(1, 0, V.get(0, 0))
        __Mv.set(1, 1, V.get(1, 0))
        __Mv.set(1, 2, V.get(2, 0))
        __Mv.set(1, 3, (negE.get(0,0)*V.get(0,0) + negE.get(1,0)*V.get(1,0) + negE.get(2,0)*V.get(2,0)))  #Set to -1*E dot V

        __Mv.set(2, 0, N.get(0, 0))
        __Mv.set(2, 1, N.get(1, 0))
        __Mv.set(2, 2, N.get(2, 0))
        __Mv.set(2, 3, (negE.get(0,0)*N.get(0,0) + negE.get(1,0)*N.get(1,0) + negE.get(2,0)*N.get(2,0)))  #Set to -1*E dot N

        __Mv.set(3, 0, 0)
        __Mv.set(3, 1, 0)
        __Mv.set(3, 2, 0)
        __Mv.set(3, 3, 1)

        return __Mv

    def __setMp(self, nearPlane, farPlane):
        a = (-1) * (farPlane + nearPlane) / (farPlane - nearPlane)  #get a
        b = (-2) * farPlane * nearPlane / (farPlane - nearPlane)    #get b

        __Mp = matrix(np.zeros((4, 4)))  #Start with 0 matrix

        #Fill the matrix properly
        __Mp.set(0, 0, nearPlane)
        __Mp.set(1, 1, nearPlane)
        __Mp.set(2, 2, a)
        __Mp.set(2, 3, b)
        __Mp.set(3, 2, -1)

        return __Mp

    def __setT1(self, nearPlane, theta, aspect):
        t = nearPlane * (tan((pi / 180) * (theta / 2))) #get t
        b = (-1) * t    #get b
        r = aspect * t  #get r
        l = r * (-1)    #get l

        __T1 = matrix(np.zeros((4, 4)))  #Start with 0 matrix

        #Fill the matrix
        __T1.set(0, 0, 1)
        __T1.set(0, 3, ((-1) * (r + l)) / 2)
        __T1.set(1, 1, 1)
        __T1.set(1, 3, ((-1) * (t + b)) / 2)
        __T1.set(2, 2, 1)
        __T1.set(3, 3, 1)

        return __T1

    def __setS1(self, nearPlane, theta, aspect):
        t = nearPlane * (tan((pi / 180) * (theta / 2))) #get t
        b = (-1) * t    #get b
        r = aspect * t  #get r
        l = -1 * r  #get l

        __S1 = matrix(np.identity(4))  #Start with 4x4 identity matrix
        #Set the rest of matrix
        __S1.set(0, 0, 2 / (r - l))
        __S1.set(1, 1, 2 / (t - b))

        return __S1

    def __setT2(self):
        __T2 = matrix(np.zeros((4, 4)))  #Start with 0 matrix
        #Set up the rest of the matrix
        __T2.set(0, 0, 1)
        __T2.set(0, 3, 1)
        __T2.set(1, 1, 1)
        __T2.set(1, 3, 1)
        __T2.set(2, 2, 1)
        __T2.set(3, 3, 1)

        return __T2

    def __setS2(self, width, height):
        __S2 = matrix(np.zeros((4, 4)))  #Start with 0 matrix
        #Set up the rest of the matrix
        __S2.set(0, 0, width / 2)
        __S2.set(1, 1, height / 2)
        __S2.set(2, 2, 1)
        __S2.set(3, 3, 1)

        return __S2

    def __setW2(self, height):
        __W2 = matrix(np.zeros((4, 4))) #Start with 0 matrix
        #Set the rest of the matrix
        __W2.set(0, 0, 1)
        __W2.set(1, 1, -1)
        __W2.set(1, 3, height)
        __W2.set(2, 2, 1)
        __W2.set(3, 3, 1)

        return __W2

    def worldToViewingCoordinates(self, P):
        return self.__Mv * P

    def viewingToImageCoordinates(self, P):
        return self.__C * P

    def imageToPixelCoordinates(self, P):
        return P.scalarMultiply(1.0 / P.get(3, 0))

    def worldToImageCoordinates(self, P):
        return self.__M * P

    def worldToPixelCoordinates(self, P):
        return self.__M * P.scalarMultiply(1.0 / (self.__M * P).get(3, 0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

'''                     parametricPlane  Class                                                                          '''

class parametricPlane(parametricObject):

    def __init__(self,T=matrix(np.identity(4)), Width = 1.0, Length = 1.0, Color=(0,0,0), Ref=(0.0,0.0,0.0), uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        super().__init__(T,Color,Ref,uRange,vRange,uvDelta)

        self.Width = Width
        self.Length = Length


    def getPoint(self,u,v):
        __P = matrix(np.ones((4,1)))    #Start with matrix full of 1's
        #Set to plane transformation matrix
        __P.set(0, 0, u*self.Width)
        __P.set(1, 0, v*self.Length)
        __P.set(2, 0, 0)

        return __P


'''                     parametricCircle  Class                                                                          '''

class parametricCircle(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),Radius=1.0,Color=(0,0,0),Ref=(0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        super().__init__(T,Color,Ref,uRange,vRange,uvDelta)

        self.Radius = Radius

    def getPoint(self,u,v):
        __P = matrix(np.ones((4,1)))    #Start with matrix full of 1's
        #Make transformation matrix for circle
        __P.set(0, 0, self.Radius*u*cos(v))
        __P.set(1, 0, self.Radius*u*sin(v))
        __P.set(2, 0, 0)

        return __P


'''                     parametricCone  Class                                                                          '''

class parametricCone(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),Height=1.0, Radius=1.0, Color=(0,0,0),Ref=(0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        super().__init__(T,Color,Ref,uRange,vRange,uvDelta)

        self.Height = Height
        self.Radius = Radius

    def getPoint(self,u,v):
        __P = matrix(np.ones((4,1)))    #Start with matrix full of 1's
        #Make the transformation matrix for a cone
        __P.set(0, 0, (((self.Height*(1-u))/self.Height)*self.Radius*cos(v)))
        __P.set(1, 0, (((self.Height*(1-u))/self.Height)*self.Radius*sin(v)))
        __P.set(2, 0, self.Height*u)

        return __P


'''                     parametricCylinder  Class                                                                          '''

class parametricCylinder(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),Height=1.0, Radius=1.0, Color=(0,0,0),Ref=(0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        super().__init__(T,Color,Ref,uRange,vRange,uvDelta)

        self.Height = Height
        self.Radius = Radius

    def getPoint(self,u,v):
        __P = matrix(np.ones((4,1)))    #Start with matrix full of 1's
        #Make transformation matrix for cylinder
        __P.set(0, 0, self.Radius*cos(v))
        __P.set(1, 0, self.Radius*sin(v))
        __P.set(2, 0, self.Height*u)

        return __P