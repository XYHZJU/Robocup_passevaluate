import library
import numpy as np
import math
PLAYER_NUM = 5
GURAD_SPEED = 1000
CANDIDATE_NUM = 5

# 第一个为leader，最后一个为goalkeeper
def generate_sample(player_num=PLAYER_NUM):
    PLAYERS = []
    for i in range(1,player_num):
        tempplayer = library.Player()
        tempplayer.generate()
        while(not tempplayer.verify()):

            tempplayer.generate()
        PLAYERS.append(tempplayer)
    tempplayer = library.GoalKeeper()
    tempplayer.generate()
    # tempplayer.show()
    while(not tempplayer.verify()):
        tempplayer.generate()
        # tempplayer.show()
    PLAYERS.append(tempplayer)
    BALL = library.Ball()
    BALL.generate()
    while(not BALL.verify()):
        BALL.generate()
        # BALL.show()

    return BALL,PLAYERS

def generate_candidate(candidate_num=CANDIDATE_NUM):
    CANDIDATES = []
    if candidate_num ==1:
        tempcandidate = library.Candidate()
        tempcandidate.generate()
        while(not tempcandidate.verify()):
            tempcandidate.generate()
        return tempcandidate
    for i in range(1,candidate_num):
        tempcandidate = library.Candidate()
        tempcandidate.generate()
        while(not tempcandidate.verify()):
            tempcandidate.generate()
        CANDIDATES.append(tempcandidate)
    return CANDIDATES



def clockwise_angle(v1, v2):
    x1,y1 = v1
    x2,y2 = v2
    dot = x1*x2+y1*y2
    det = x1*y2-y1*x2
    theta = np.arctan2(det, dot)
    theta = theta if theta>0 else 2*np.pi+theta
    return theta 

def eucliDist(A,B):
    return math.sqrt(sum([(a-b)**2 for (a,b) in zip(A,B)]))

 
def __point_to_line_distance(point, line1, line2):
    # print(point)
    px, py = point
    x1, y1 = line1
    x2, y2 = line2
    line_magnitude = eucliDist([x1, y1], [x2, y2])
    if line_magnitude < 0.00000001:
        return 9999
    else:
        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (line_magnitude * line_magnitude)
        if (u < 0.00001) or (u > 1):
            # 点到直线的投影不在线段内, 计算点到两个端点距离的最小值即为"点到线段最小距离"
            ix = eucliDist([px, py], [x1, y1])
            iy = eucliDist([px, py], [x2, y2])
            if ix > iy:
                distance = iy
            else:
                distance = ix
        else:
            # 投影点在线段内部, 计算方式同点到直线距离, u 为投影点距离x1在x1x2上的比例, 以此计算出投影点的坐标
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            distance = eucliDist([px, py], [ix, iy])
        return distance

def generate_evaluate(ball,players,candidate):
    # print("ballpos:",ball.Pos())
    LEADER = players[0]
    GOALKEEPER = players[-1]

    wClosestEnemyDist = 0.1
    wDist = 0.2
    # wGuardTime = 0.1
    wPassLineDist = 0.8
    min2PenaltyDist = 50
    wshoot_dir = 0.3

    min_dist = 99999
    min_pass_line_dist = 99999

    # players = players[1:]
    # for player in players:
    #     print("player.pos:",player.Pos())


    for player in players:
        if eucliDist(player.Pos(),candidate.Pos())<min_dist:
            min_dist = eucliDist(player.Pos(),candidate.Pos())
            closestenemy = player

        if __point_to_line_distance(ball.Pos(), player.Pos(), candidate.Pos())<min_pass_line_dist:
            min_pass_line_dist = __point_to_line_distance(ball.Pos(),  player.Pos(), candidate.Pos())
    defdist = eucliDist(candidate.Pos(),[library.PITCH_LENGTH/2,0])
    shoot_dir_sin = abs(library.PITCH_LENGTH/2 - candidate.Pos()[0])/defdist

    #归一化
    defdist = 1 - defdist/library.PITCH_LENGTH
    if (min_pass_line_dist>300):
        min_pass_line_dist = 1
    else:
        min_pass_line_dist = min_pass_line_dist/300
    
    if (min_dist>300):
        min_dist = 1
    else:
        min_dist = min_dist/300
    sum_value = wClosestEnemyDist*min_dist + wDist*defdist+ wPassLineDist*min_pass_line_dist+wshoot_dir*shoot_dir_sin
    return sum_value




def show_sample(ball,players):
    ball.show()
    for index,player in enumerate(players):
        print("index:",index)
        player.show()

def resize(ball,players,candidate):
    # print(type(ball))
    # ball = ball.copy()
    # ball.normalize()
    ball_vector = ball.Pos().copy()
    ball_vector,_ = ball.normalize()
    

    candidate_vector = candidate.Pos()
    candidate_vector = candidate.normalize()
    # candidate_vector = list(candidate_vector)
    # ball_vector.extend(ball.Vel())
    players_vector = []
    for player in players:
       
        
        player_vector = player.Pos().copy()
        player_vector,_ = player.normalize()
        # player_vector.extend(player.Vel())
        # player_vector = list(player_vector)
        player_vector.append(player.Ang())
        
        # player_vector.append(player.V_w())
        players_vector.extend(player_vector)
    sum_vector = ball_vector
    sum_vector.extend(players_vector)
    sum_vector.extend(candidate_vector)
    
    # sum_vector = np.array(sum_vector)
    # print(sum_vector)
    return sum_vector,len(sum_vector)

def generate_data(num):
    print("start generating")
    
    
    results = []
    values = []
    for i in range(1,num):
        # print("merged:",i)
        ball,players = generate_sample(5)
        
        # print("ball:",ball.Pos())
        candidate = generate_candidate(1)

        result,size = resize(ball,players,candidate)

        value = generate_evaluate(ball,players,candidate)

        results.append(result)
        values.append(value)

    results = np.array(results)
    results = results.astype(float)
    values = np.array(values)
    values = values.astype(float)

    return results,values,size

if __name__=="__main__":
    # data,_ = generate_data(10)
    # print(data)

    # ball,players = generate_sample(5)
    # candidates = generate_candidate(5)
    _,values,_ = generate_data(10)
    print(values)
    # for candidate in candidates:
    #     score = generate_evaluate(ball,players,candidate)
    #     print(score)




