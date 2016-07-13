import brickpi
import time
import math
import numpy as np
from Canvas import Canvas

class Sonar:
    sigma = 3
    motorTurn = 2.9
    turnDirection = 1
    epsilon = 1
    
    
    def __init__(self,interf,p):
        self.canvas = Canvas()
        # Setup sonar sensor
        self.interface = interf
        self.port = p
        self.interface.sensorEnable(0, brickpi.SensorType.SENSOR_ULTRASONIC)
        
        # Setup sonar motor
        self.motors = [1]

        self.interface.motorEnable(self.motors[0])

        self.motorParams = self.interface.MotorAngleControllerParameters()
        self.motorParams.maxRotationAcceleration = 9.0
        self.motorParams.maxRotationSpeed =  10.0
        self.motorParams.feedForwardGain = 255/20.0
        self.motorParams.minPWM = 5.0
        self.motorParams.pidParameters.minOutput = -255
        self.motorParams.pidParameters.maxOutput = 255
        self.motorParams.pidParameters.k_p = 100.0
        self.motorParams.pidParameters.k_i = 100.0
        self.motorParams.pidParameters.k_d = 80.0

        self.interface.setMotorAngleControllerParameters(self.motors[0], self.motorParams)
        # ASSUMPTION: ASSUMES MOTOR STARTS FACING BACKWARD!
        self.zeroAngle = self.interface.getMotorAngles(self.motors)[0][0] + (math.pi * self.motorTurn)
        
    def getSonarReading(self):
        
        i = 10
        sonarReadings = np.zeros(i)
        
        for j in range(i):
            sonarReadings[j] = self.interface.getSensorValue(self.port)[0]

        return np.median(sonarReadings)


    def getSonarAndAngleReading(self):
        sR, sA = self.getSonarAndAngleReadingNoTurn()
        self._turnSonar()
        return sR, sA
    
    def getSonarAndAngleReadingNoTurn(self):
        i = 5
        sonarReadings = np.zeros(i)
        sonarAngles = np.zeros(i)
        
        
        for j in range(i):
            sonarReadings[j] = self.interface.getSensorValue(self.port)[0]
            sonarAngles[j] = self.interface.getMotorAngles(self.motors)[0][0]
            # time.sleep(0.00105) #change this to change the speed of reading(this is enough for ~240
            
        sonarAngles -= self.zeroAngle
        sonarAngles /= self.motorTurn

        return np.median(sonarReadings) - 1.5, -np.mean(sonarAngles)
        
    def _turnSonar(self):
        angle = self.interface.getMotorAngles(self.motors)[0][0]
        angleChange = (math.pi * self.motorTurn) / 2.0 # Turn 90 degrees
        
        if abs(angle - self.zeroAngle) < self.epsilon:
            # Motor is at the zero position
            self.interface.increaseMotorAngleReferences(self.motors,[self.turnDirection * angleChange])
            # print "Sonar at zero position"
            
        if angle - self.zeroAngle > angleChange - self.epsilon:
            # Motor is at the far right position
            self.interface.increaseMotorAngleReferences(self.motors,[-angleChange])
            self.turnDirection = -1
            # print "Sonar at far right position"
            
        if self.zeroAngle - angle > angleChange - self.epsilon:
            # Motor is at the far left position
            self.interface.increaseMotorAngleReferences(self.motors,[angleChange])
            self.turnDirection = 1
            # print "Sonar at far left position"
            
    def getSonar360(self, ls_obs, canvas):
        #Set angle diff between readings
        #Turn 180 right while taking sonar readings
        full360 = self.motorTurn * math.pi * 2.0 # 17.486 + 0.746
        increment = full360 / ls_obs.no_bins 
        # n_obs = 1000
        # increment = full360 / float(n_obs)
        startAngle = self.interface.getMotorAngles(self.motors)[0][0] 
        motorAngle = startAngle
        self.interface.increaseMotorAngleReferences(self.motors,[full360])        
        i = 0 #incerement when angle has incremented by degreeIncs
        sR = np.zeros((ls_obs.no_bins, 2))
        while (motorAngle < (startAngle + full360 + 0.03)): #0.077 is a consistent error value for speed
            motorAngle = self.interface.getMotorAngles(self.motors)[0][0]
            if ((motorAngle-startAngle) // increment) > i and i < ls_obs.no_bins:
                ls_obs.sig[i] = self.getSonarReading()                
                sR[i, 0], sR[i, 1] = self.getSonarAndAngleReadingNoTurn()                
                
                i += 1
        
        print "MADE {0} OBSERVATIONS".format(i)
        canvas.parkSonarCloud(sR)
        """
        
        for i in range(ls_obs.no_bins):
            line = [100, 100,100 + sR[i] * math.cos(sA[i]),100 + sR[i] * math.sin(sA[i])]            
            canvas.drawLine(line)
        """  
        
        #self.interface.increaseMotorAngleReferences(self.motors,[-full360/2.0])

        return ls_obs
    
    def rotateToFront(self):
        full360 = self.motorTurn * math.pi * 2.0
        self.interface.increaseMotorAngleReferences(self.motors,[-full360/2.0])
        
    def rotateToBack(self):
        full360 = self.motorTurn * math.pi * 2.0
        self.interface.increaseMotorAngleReferences(self.motors,[-full360])
        refAngle = self.interface.getMotorAngleReferences(self.motors)[0]
        motorAngle = self.interface.getMotorAngles(self.motors)[0][0] 
        while abs(motorAngle - refAngle) > 0.03:
            motorAngle = self.interface.getMotorAngles(self.motors)[0][0] 

            
        
    
    