import math
class Canvas:
    def __init__(self,map_size=210):
        self.map_size    = map_size;    # in cm;
        self.canvas_size = 768;         # in pixels;
        self.margin      = 0.05*map_size;
        self.scale       = self.canvas_size/(map_size+2*self.margin);

    def drawLine(self,line):
        x1 = self.__screenX(line[0]);
        y1 = self.__screenY(line[1]);
        x2 = self.__screenX(line[2]);
        y2 = self.__screenY(line[3]);
        print "drawLine:" + str((x1,y1,x2,y2))

    def drawParticles(self,data):
        # pass
        # """
        display = [(self.__screenX(d[0]),self.__screenY(d[1])) + d[2:] for d in data];
        print "drawParticles:" + str(display);
        # """

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale
    
    def drawArrow(self, coord, arrowSz=10):
        #pass
        # """
        dX = arrowSz * math.cos(coord[2]) 
        dY = arrowSz * math.sin(coord[2])
        
        self.drawLine([coord[0] - dX, coord[1] - dY, coord[0] + dX, coord[1] + dY])
        
        dL = arrowSz * math.cos(coord[2] + math.pi / 5.0) 
        dR = arrowSz * math.sin(coord[2] + math.pi / 5.0) 
        self.drawLine([coord[0] + dX, coord[1] + dY, coord[0] + dX - dL, coord[1] + dY - dR])
        
        dL = arrowSz * math.cos(coord[2] - math.pi / 5.0) 
        dR = arrowSz * math.sin(coord[2] - math.pi / 5.0) 
        self.drawLine([coord[0] + dX, coord[1] + dY, coord[0] + dX - dL, coord[1] + dY - dR])
        # """
        
    def drawWaypoint(self, wp, xSz=5):       
        self.drawLine([wp[0] - xSz, wp[1], wp[0] + xSz, wp[1]])
        self.drawLine([wp[0], wp[1] - xSz, wp[0], wp[1] + xSz])
        
    def parkSonarCloud(self, sonarR):
        self.sonarReadings = sonarR
        
    def drawSonarCloud(self, loc):
        pass
        """
        for sR in self.sonarReadings:
            line = [loc[0], loc[1],loc[0] + sR[0] * math.cos(loc[2] + sR[1]),loc[1] + sR[0] * math.sin(loc[2] + sR[1])]            
            self.drawLine(line)
        """