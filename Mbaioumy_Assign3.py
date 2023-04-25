import numpy as np
from matrix import matrix


class tessel:

    def __init__(self, objectTuple, camera, light):
        self.__faceList = []  # List of faces with attributes
        EPSILON = 0.001

        # Transform light position into viewing coordinates
        Lv = camera.worldToViewingCoordinates(light.getPosition())

        for object in objectTuple:
            u = object.getURange()[0]
            while u + object.getUVDelta()[0] < object.getURange()[1] + EPSILON:
                v = object.getVRange()[0]
                while v + object.getUVDelta()[1] < object.getVRange()[1] + EPSILON:

                    # Collect surface points and transform them into viewing coordinates
                    __p1 = camera.worldToViewingCoordinates(object.getT() * object.getPoint(u, v))
                    __p2 = camera.worldToViewingCoordinates(
                        object.getT() * object.getPoint(u + object.getUVDelta()[0], v))
                    __p3 = camera.worldToViewingCoordinates(
                        object.getT() * object.getPoint(u + object.getUVDelta()[0], v + object.getUVDelta()[1]))
                    __p4 = camera.worldToViewingCoordinates(
                        object.getT() * object.getPoint(u, v + object.getUVDelta()[1]))
                    # Compute vector elements necessary for face shading
                    facePoints = (__p1, __p2, __p3, __p4)
                    ref = object.getReflectance()
                    col = object.getColor()
                    C = self.__centroid(facePoints)  # Find centroid point of face
                    N = self.__vectorNormal(facePoints)  # Find normal vector to face
                    S = self.__vectorToLightSource(Lv, C)  # Find vector to light source
                    R = self.__vectorSpecular(S, N)  # Find specular reflection vector
                    V = self.__vectorToCentroid(C)  # Find vector from surface centroid to origin of viewing coordinates

                    # If surface is not a back face
                    if (self.dot(V, N) > 0):
                        # Compute face shading
                        Id = max(0, (self.dot(S, N) / (self.nnorm(S) * self.nnorm(N))))
                        Is = max(0, (self.dot(R, V) / (self.nnorm(R) * self.nnorm(V)))) ** (ref[3])
                        shading = ref[0] + (ref[1] * Id) + (ref[2] * Is)
                        Red = int(round(shading * col[0]))
                        Green = int(round(shading * col[1]))
                        Blue = int(round(shading * col[2]))

                        shading = (Red, Green, Blue)

                        # Transform 3D points expressed in viewing coordinates into 2D pixel coordinates
                        p1 = camera.viewingToPixelCoordinates(__p1)
                        p2 = camera.viewingToPixelCoordinates(__p2)
                        p3 = camera.viewingToPixelCoordinates(__p3)
                        p4 = camera.viewingToPixelCoordinates(__p4)

                        # Add the surface to the face list. Each list element is composed of the following items:
                        # [depth of the face centroid point (its Z coordinate), list of face points in pixel coordinates, face shading]
                        self.__faceList.append((C.get(2, 0), (p1, p2, p3, p4), shading))
                    v += object.getUVDelta()[1]
                u += object.getUVDelta()[0]

    def __centroid(self, facePoints):

        # Returns the column matrix containing the face centroid point
        sides = facePoints[0] + facePoints[1] + facePoints[2] + facePoints[3]
        return sides.scalarMultiply(0.25)

    def __vectorNormal(self, facePoints):

        # Returns the column matrix containing the normal vector to the face.
        m1 = (facePoints[2] - facePoints[0]).removeRow(3).transpose()
        m2 = (facePoints[3] - facePoints[1]).removeRow(3).transpose()
        cp = (m1.crossProduct(m2)).transpose().insertRow(3, 0)
        return self.nnormalize(cp)

    def __vectorToLightSource(self, L, C):

        # Returns the column matrix containing the vector from the centroid to the light source
        return L - C

    def __vectorSpecular(self, S, N):
        r = S.scalarMultiply(-1) + N.scalarMultiply(2 * (self.dot(N, S)) / (N.norm() ** 2))
        # Returns the column matrix containing the vector of specular reflection
        return r

    def __vectorToCentroid(self, C):

        # Returns the column matrix containing the vector from the face centroid point to the origin of the viewing coordinates
        c = -C
        return c

    def getFaceList(self):  # Returns the face list ready for drawing
        return self.__faceList

    # My own dot product How about it
    def dot(self, v1, v2):
        return v1.get(0, 0) * v2.get(0, 0) + v1.get(1, 0) * v2.get(1, 0) + v1.get(2, 0) * v2.get(2, 0)

    # My own normal formula
    def nnorm(self, v1):
        return (v1.get(0, 0) ** 2 + v1.get(1, 0) ** 2 + v1.get(2, 0) ** 2) ** (1 / 2)

    # Normalizing
    def nnormalize(self, v1):
        z = self.nnorm(v1)
        return v1.scalarMultiply(z)




class lightSource:

    def __init__(self,position=matrix(np.zeros((4,1))),color=(0,0,0),intensity=(1.0,1.0,1.0)):
        self.__position = position
        self.__color = color
        self.__intensity = intensity

    def getPosition(self):
        return self.__position
    def getColor(self):
        return self.__color
    def getIntensity(self):
        return self.__intensity

    def setPosition(self,position):
        self.__position = position
    def setColor(self,color):
        self.__color = color
    def setIntensity(self,intensity):
        self.__intensity = intensity