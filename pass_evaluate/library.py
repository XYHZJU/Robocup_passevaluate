from math import pi
import random
# from typing_extensions import Self
from xml.etree.ElementTree import PI


PITCH_LENGTH = 9000
PITCH_WIDTH = 6000
BALL_V_MAX_X = 400
BALL_V_MAX_Y = 1500
PLAYER_V_MAX_X = 1500
PLAYER_V_MAX_Y = 1500
PENALTY_LENGTH = 2000
PENALTY_WIDTH = 800


class Ball:
    x = 0
    y = 0
    v_x = 0
    v_y = 0
    pos = [x,y]
    vel = [v_x,v_y]

    def __init__(self, pos=[0,0], vel=[0,0]):
        self.pos = pos
        self.vel = vel
    
    def Pos(self):
        return self.pos
    
    def Vel(self):
        return self.vel
    
    def generate(self):
        self.x = random.uniform(0, PITCH_LENGTH/2)
        self.y = random.uniform(-PITCH_WIDTH/2, PITCH_WIDTH/2)
        self.v_x = random.uniform(-BALL_V_MAX_X,BALL_V_MAX_X)
        self.v_y = random.uniform(-BALL_V_MAX_Y,BALL_V_MAX_Y)
        self.pos = [self.x,self.y]
        self.vel = [self.v_x,self.v_y]
    
    def normalize(self):
        x = self.x/PITCH_LENGTH/2
        y = self.y/PITCH_WIDTH+0.5
        v_x = self.v_x/PITCH_LENGTH
        v_y = self.v_y/PENALTY_WIDTH+0.5
        pos = [x,y]
        vel = [v_x,v_y]
        return pos,vel
    
    def show(self):
        print("pos:",self.pos)
        print("vel:",self.vel)
    
    def verify(self):
        if (self.x>PITCH_LENGTH - PENALTY_WIDTH and abs(self.y)<PENALTY_LENGTH/2):
            return False
        return True

class Candidate:
    x = 0
    y = 0
    pos =[x,y]
    def __init__(self, pos=[0,0]):
        self.pos = pos

    def Pos(self):
        return self.pos  
    def generate(self):
        self.x = random.uniform(0, PITCH_LENGTH/2)
        self.y = random.uniform(-PITCH_WIDTH/2, PITCH_WIDTH/2)
        
        self.pos = [self.x,self.y]
    
    def normalize(self):
        x = self.x/(PITCH_LENGTH/2)
        y = self.y/PITCH_WIDTH+0.5
        pos = [x,y]
        return pos
        
    def show(self):
        print("pos:",self.pos)

    def verify(self):
        if (self.x>PITCH_LENGTH - PENALTY_WIDTH and abs(self.y)<PENALTY_LENGTH/2):
            return False
        return True

class Player:
    x = 0
    y = 0
    v_x = 0
    v_y = 0
    ang = 0
    v_w = 0
    pos = [x,y]
    vel = [v_x,v_y]

    def __init__(self, pos=[0,0], vel=[0,0], v_w=0):
        self.pos = pos
        self.vel = vel
        self.v_w = v_w
    
    def Pos(self):
        return self.pos
    def Vel(self):
        return self.vel
    def Ang(self):
        return self.ang
    def V_w(self):
        return self.v_w
    def generate(self):
        self.x = random.uniform(0, PITCH_LENGTH/2)
        self.y = random.uniform(-PITCH_WIDTH/2, PITCH_WIDTH/2)
        self.v_x = random.uniform(-PLAYER_V_MAX_X,PLAYER_V_MAX_X)
        self.v_y = random.uniform(-PLAYER_V_MAX_Y,PLAYER_V_MAX_Y)
        self.ang = random.uniform(-180,180)/360+0.5
        self.v_w = random.uniform(-pi,pi)
        self.pos = [self.x,self.y]
        self.vel = [self.v_x,self.v_y]
    def normalize(self):
        x = self.x/(PITCH_LENGTH/2)
        y = self.y/PITCH_WIDTH+0.5
        v_x = self.v_x/(PITCH_LENGTH/2)
        v_y = self.v_y/(2*PLAYER_V_MAX_Y)+0.5
        pos = [x,y]
        vel = [v_x,v_y]
        return pos,vel

    
    def show(self):
        print("pos:",self.pos)
        print("vel:",self.vel)
        print("ang:",self.ang)
        print("v_w:",self.v_w)
    
    def verify(self):
        if (self.x>PITCH_LENGTH - PENALTY_WIDTH and abs(self.y)<PENALTY_LENGTH):
            return False
        return True


class GoalKeeper(Player):
    def generate(self):
        self.x = PITCH_LENGTH/2
        self.y = random.uniform(-PENALTY_LENGTH/2, PENALTY_LENGTH/2)
        self.v_x = random.uniform(-PLAYER_V_MAX_X,PLAYER_V_MAX_X)
        self.v_y = random.uniform(-PLAYER_V_MAX_Y,PLAYER_V_MAX_Y)
        self.ang = 180/180
        self.v_w = random.uniform(-pi,pi)
        self.pos = [self.x,self.y]
        self.vel = [self.v_x,self.v_y]

    def normalize(self):
        x = 1
        y = self.y/PENALTY_LENGTH+0.5
        v_x = self.v_x/(PITCH_LENGTH/2)
        v_y = self.v_y/(2*PLAYER_V_MAX_Y)+0.5
        pos = [x,y]
        vel = [v_x,v_y]
        return pos,vel

    def verify(self):
        return True

GUARD_MIN_TIME = 1
GUARD_MAX_TIME = 8

DEF_MIN_DIST = 1500
DEF_MAX_DIST = 7000

CLOSEST_ENM_DIST = 200
LONGEST_ENM_DIST = 3000

SHOOT_MIN_DIR = 15
SHOOT_MAX_DIR = 90

MIN_PASS_DIST = 1500
MAX_PASS_DIST = 5000


class PassIndex:
    guardtime = 0
    defdist = 0
    closestenemydist = 0
    shoot_dir = 0
    passlinedist = 0
    GOAL = 0

    discreted = 0
    guardtime_status = ""
    defdist_status = ""
    closestenemydist_status = ""
    shoot_dir_status = ""
    passlinedist_status = ""



    def __init__(self, guardtime = 0, defdist = 0,closestenemydist = 0, shoot_dir = 0, passlinedist = 0,GOAL = 0):
        self.guardtime = guardtime
        self.defdist = defdist
        self.closestenemydist = closestenemydist
        self.shoot_dir = shoot_dir
        self.passlinedist = passlinedist
        self.GOAL = GOAL
    
    def Guardtime(self):
        return self.guardtime,self.guardtime_status
    def Defdist(self):
        return self.defdist,self.defdist_status
    def Closestenemydist(self):
        return self.closestenemydist,self.closestenemydist_status
    def Shoot_dir(self):
        return self.shoot_dir,self.shoot_dir_status
    def Passlinedist(self):
        return self.passlinedist,self.passlinedist_status
    def Goal(self):
        return self.GOAL

    def generate(self):
        self.guardtime = random.uniform(GUARD_MIN_TIME,GUARD_MAX_TIME)
        self.defdist = random.uniform(DEF_MIN_DIST,DEF_MAX_DIST)
        self.closestenemydist = random.uniform(CLOSEST_ENM_DIST,LONGEST_ENM_DIST)
        self.shoot_dir = random.uniform(SHOOT_MIN_DIR,SHOOT_MAX_DIR)
        self.passlinedist = random.uniform(MIN_PASS_DIST,MAX_PASS_DIST)
        self.GOAL = random.randint(0,1)
    
    def discrete_value(self):
        self.discreted = 1

        if self.guardtime<GUARD_MIN_TIME + (GUARD_MAX_TIME - GUARD_MIN_TIME)/3:
            self.guardtime_status = "SMALL"
        elif  self.guardtime<GUARD_MIN_TIME + (GUARD_MAX_TIME - GUARD_MIN_TIME)*2/3:
            self.guardtime_status = "MEDIUM"
        else :
            self.guardtime_status = "LARGE"
        
        if self.defdist<DEF_MIN_DIST + (DEF_MAX_DIST - DEF_MIN_DIST)/3:
            self.defdist_status = "SMALL"
        elif self.defdist<DEF_MIN_DIST + (DEF_MAX_DIST - DEF_MIN_DIST)*2/3:
            self.defdist_status = "MEDIUM"
        else :
            self.defdist_status = "LARGE"

        if self.closestenemydist<CLOSEST_ENM_DIST + (LONGEST_ENM_DIST - CLOSEST_ENM_DIST)/3:
            self.closestenemydist_status = "SMALL"
        elif  self.closestenemydist<CLOSEST_ENM_DIST + (LONGEST_ENM_DIST - CLOSEST_ENM_DIST)*2/3:
            self.closestenemydist_status = "MEDIUM"
        else :
            self.closestenemydist_status = "LARGE"

        if self.shoot_dir < SHOOT_MIN_DIR + (SHOOT_MAX_DIR - SHOOT_MIN_DIR )/3:
            self.shoot_dir_status = "SMALL"
        elif self.shoot_dir < SHOOT_MIN_DIR + (SHOOT_MAX_DIR - SHOOT_MIN_DIR )*2/3:
            self.shoot_dir_status = "MEDIUM"
        else :
            self.shoot_dir_status = "LARGE"

        if self.passlinedist < MIN_PASS_DIST + (MAX_PASS_DIST - MIN_PASS_DIST )/3:
            self.passlinedist_status = "SMALL"
        elif self.passlinedist < MIN_PASS_DIST + (MAX_PASS_DIST - MIN_PASS_DIST )*2/3:
            self.passlinedist_status = "MEDIUM"
        else :
            self.passlinedist_status = "LARGE" 

    def show(self):
        print('guardtime:{} ,defdist:{} ,closestenemy:{} ,shootdir:{} ,passlinedist:{} ,goal:{}'.format(self.guardtime_status,self.defdist_status,self.closestenemydist_status,self.shoot_dir_status,self.passlinedist_status,self.GOAL))







