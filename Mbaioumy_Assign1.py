from PIL import Image
"Mazen Baioumy"
"Student Number: 250924925"
"Drawline method that implement's Bresenham's line algorithm"


class graphicsWindow:

    def __init__(self,width=640,height=480):
        self.__mode = 'RGB'
        self.__width = width
        self.__height = height
        self.__canvas = Image.new(self.__mode,(self.__width,self.__height))
        self.__image = self.__canvas.load()

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def drawPixel(self,pixel,color):
        self.__image[pixel[0],pixel[1]] = color

    def saveImage(self,fileName):
        self.__canvas.save(fileName)

    def drawLine(self, p1, p2, color):

        x1 = p1[0]
        y1 = p1[1]

        x2 = p2[0]
        y2 = p2[1]

        dy = abs(y2 - y1)  # delta x
        dx = abs(x2 - x1)  # delta y

        self.drawPixel([x1, y1], color)
        for i in range(x1, x2):
            if (i == x1):
                p = 2 * dy - dx

            else:
                if (p < 0):
                    p = p + 2 * dy

                else:
                    p = p + 2 * dy - 2 * dx
                    if (y1 > y2):
                        y1 += -1  # Decrement y if vector aims downward
                    else:
                        y1 += 1  # Increment otherwise
                x1 += 1

            # Manipulates points symmetrically to account for each quadrant
            if (dy < dx):
                self.drawPixel([x1, y1], color)
                self.drawPixel([y1, x1], color)
                self.drawPixel([-x1, -y1], color)
                self.drawPixel([-y1, -x1], color)