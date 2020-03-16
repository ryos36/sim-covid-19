import random

width=1920
height=1080
earth=[[0]*height for i in range(width)]
#print(len(earth[0]))
w0=500
h0=500
w0=int(width*random.random())
h0=int(height*random.random())
earth[w0][h0] = 1 
#print(earth[1079][1919])
r0=1.8
move_n=int(width*height * 0.1)
around=8
beds=int(width*height/1000)
pos = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, -1), (-1, 1), (0, 1), (1, 1)]
jump_distance = int(width * 0.5)

STATE0_INIT=0
STATE1_INFECTION=0x100
STATE2_SPREADER=0x200
STATE3_SERIOUS=0x300
STATE4_DEAD=0x400
STATE5_REVIVE=0x500
STATE6_BLOCKER=0x600
STATE7_NO_PERSON=0x700
STATE8_MOLE=0x800

spreader_rate=0.5
days0=1
days1=14
rate=r0/(days1 * around)
serious_rate=0.1/days1
serious_days=10
dead_rate=0.1/serious_days
revive_days=10
STATE0_MARKED=days0 + 1

def next_state(state_days, lack_of_beds):
    state = state_days & 0xFF00
    days = state_days & 0xFF

    new_state_days = state
    if state_days < 0:
        pass
    elif state_days == STATE0_MARKED:
        pass
    elif state == STATE0_INIT:
        if days == 0:
            pass
        elif days == days0:
            if random.random() < spreader_rate:
                new_state_days = STATE1_INFECTION
            else:
                new_state_days = STATE2_SPREADER
        else:
            days += 1

    elif (state == STATE1_INFECTION) or (state == STATE2_SPREADER):
        if days == days1:
            new_state_days = STATE6_BLOCKER
        else:
            if (state == STATE1_INFECTION) and (random.random() < serious_rate):
                new_state_days = STATE3_SERIOUS
            else:
                days += 1
    elif state == STATE3_SERIOUS:
        if lack_of_beds:
            if random.random() < serious_rate:
                new_state_days = STATE4_DEAD
        elif days == serious_days:
                new_state_days = STATE5_REVIVE
        else:
            if random.random() < serious_rate:
                new_state_days = STATE4_DEAD
            else:
                days += 1
    elif state == STATE5_REVIVE:
        if days == revive_days:
            new_state_days = STATE6_BLOCKER
        else:
            days += 1

    if state == new_state_days:
        return state + days
    else:
        return new_state_days

now_day = 1
dead_n = 0
serious_beds_rate=0.0
while True:
    state_n = [0] * 8

    serious_n = 0
    for w in range(width):
        for h in range(height):
            v = earth[w][h]
            state = v & 0xFF00
            if state == STATE3_SERIOUS:
                serious_n += 1

            earth[w][h] = next_state(v, random.random() > serious_beds_rate)

            if (state == STATE1_INFECTION) or (state == STATE2_SPREADER):
            
                for p in pos:
                    target_p = tuple(map(lambda x,y:x+y, (w, h), p))
                    if ((target_p[0] < 0) or (width <= target_p[0]) or
                        (target_p[1] < 0) or (height <= target_p[1])):
                        continue

                    if earth[target_p[0]][target_p[1]] != STATE0_INIT :
                        continue

                    r = random.random()
                    hit = (r < rate)
                    #print(r, rate, hit)
                    if hit:
                        earth[target_p[0]][target_p[1]] = STATE0_MARKED

    if serious_n == 0:
        serious_beds_rate = 0.0
    else:
        serious_beds_rate = beds / serious_n

    for w in range(width):
        for h in range(height):
            v = earth[w][h]
            if v >= STATE7_NO_PERSON:
                continue;
            if v == STATE0_MARKED:
                earth[w][h] = 1
            state = v & 0xFF00
            if state == STATE0_INIT:
                if v == STATE0_INIT:
                    state_n[0] += 1
                else:
                    state_n[7] += 1
            else:
                state_n[state >> 8] += 1

            if state == STATE4_DEAD:
                dead_n += 1
                earth[w][h] = STATE7_NO_PERSON

            #if ( v > 0 ) and ( v < 100):
            #    print('here', w, h, v, earth[w][h]);

    print(now_day, state_n, dead_n, flush=True)
    now_day += 1
    if (state_n[1] == 0) and (state_n[2] == 0) and (state_n[3] == 0) and (state_n[5] == 0) and (state_n[7] == 0):
        print(state_n, state_n[6] / (width * height), dead_n)
        break
    for i in range(move_n):
        x0 = int(width*random.random())
        y0 = int(height*random.random())
        dx = int(jump_distance*random.random() - jump_distance/2)
        x1 = x0 + dx
        if (x1 >= width ) or ( x1 < 0 ):
            x1 = x0 - dx
        if (x1 >= width ) or ( x1 < 0 ):
            print(x1, x0, dx)
        assert(not ((x1 >= width ) or ( x1 < 0 )))

        dy = int(jump_distance*random.random() - jump_distance/2)
        y1 = y0 + dx
        if (y1 >= height ) or (y1 < 0 ):
            y1 = y0 - dx
        if (y1 >= height ) or (y1 < 0 ):
            print(y1, y0, dx)
        assert(not ((y1 >= height ) or (y1 < 0 )))
        v0 = earth[x0][y0]
        v1 = earth[x1][y1]
        if ( v0 != STATE8_MOLE ) and ( v1 != STATE8_MOLE ) and ( v0 != STATE1_INFECTION ) and ( v0 != STATE1_INFECTION ) and ( v0 != STATE3_SERIOUS ) and ( v1 != STATE3_SERIOUS) and ( v0 != STATE5_REVIVE) and ( v1 != STATE5_REVIVE ) :
            earth[x0][y0], earth[x1][y1] = v1, v0

