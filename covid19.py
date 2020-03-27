import copy
import random
from version import version
from param import r0, init_n, move_n, around, beds, jump_distance_long , jump_distance , jump_distance_rate_base, jump_distance_rate_early, jump_distance_rate_lator, jump_distance_change_days_early, jump_distance_change_days_lator, use_jump_distance_change_flag, spreader_rate, days0, days1, days2, rate, serious_rate, serious_days, dead_rate, revive_days, use_check, use_hold, check_n, mhlw_check_rate

print(version, r0, init_n, move_n, around, beds, jump_distance_long , jump_distance , jump_distance_rate_base, jump_distance_rate_early, jump_distance_rate_lator, jump_distance_change_days_early, jump_distance_change_days_lator, use_jump_distance_change_flag, spreader_rate, days0, days1, days2, rate, serious_rate, serious_days, dead_rate, revive_days, use_check, use_hold, check_n, mhlw_check_rate)

width=1920
height=1080
earth=[[0]*height for i in range(width)]
for i in range(init_n):
    w0=int(width*random.random())
    h0=int(height*random.random())
    if earth[w0][h0] != 0:
        init_n -= 1

    earth[w0][h0] = days0 
pos = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, -1), (-1, 1), (0, 1), (1, 1)]

STATE0_INIT=0
STATE1_INFECTION=0x100
STATE2_SPREADER=0x200
STATE3_SERIOUS=0x300
STATE4_DEAD=0x400
STATE5_REVIVE=0x500
STATE6_BLOCKER=0x600
STATE7_NO_PERSON=0x700
STATE8_MOLE=0x800

STATE0_MARKED=days0 + 1
MHLW_CHECK_MARK = 0x1000000
HOLD_MARK = 0x1000000

serious_rate_list = [0.0] * (serious_days * 2)

def next_state(state_days, lack_of_beds, serious_rate_list):
    a_disappear_n = 0

    flags = state_days & 0xFF000000
    r0_hit_n = state_days & 0xFF0000
    state = state_days & 0xFF00
    days = state_days & 0xFF

    new_state_days = state
    if state_days < 0:
        pass
    elif (state_days & 0xFFFF) == STATE0_MARKED:
        #ダブルバッファを使ってない
        #バグが出そう(要チェック)
        pass
    elif state == STATE0_INIT:
        if days == 0:
            pass
        elif days == days0:
            if random.random() < spreader_rate:
                new_state_days = STATE2_SPREADER | 1
            else:
                new_state_days = STATE1_INFECTION | 1
                if random.random() < mhlw_check_rate:
                    flags |= MHLW_CHECK_MARK
        else:
            days += 1

    elif state == STATE1_INFECTION:
        if days == days1:
            new_state_days = STATE6_BLOCKER
        else:
            if random.random() < serious_rate:
                new_state_days = STATE3_SERIOUS | 1
            else:
                days += 1

    elif state == STATE2_SPREADER:
        if days == days2:
            new_state_days = STATE6_BLOCKER
        else:
            days += 1
                
    elif state == STATE3_SERIOUS:
        if lack_of_beds:
            if len(serious_rate_list) <= days:
                print(serious_rate_list)
                new_serious_rate_list = [0.0] * (days * 2)
                for i, e in enumerate(serious_rate_list):
                    new_serious_rate_list[i] = e
                serious_rate_list = new_serious_rate_list
                print('new', serious_rate_list)
            srate = serious_rate_list[days]
            if srate == 0.0:
                srate = (1 - serious_rate) ** days
                serious_rate_list[days] = srate
            if random.random() > srate:
                new_state_days = STATE4_DEAD
            #for i in range(days):
            #    if random.random() < serious_rate:
            #        new_state_days = STATE4_DEAD

        elif days == serious_days:
                new_state_days = STATE5_REVIVE | 1
        else:
            if random.random() < serious_rate:
                new_state_days = STATE4_DEAD
            else:
                days += 1
        if new_state_days == STATE4_DEAD:
            a_disappear_n += r0_hit_n >> 16
            #print('a_disappear_n', a_disappear_n)

    elif state == STATE5_REVIVE:
        if days == revive_days:
            new_state_days = STATE6_BLOCKER
        else:
            days += 1

    if state == new_state_days:
        new_state_days = state | days

    return (flags | r0_hit_n | new_state_days), a_disappear_n, serious_rate_list


def add_r0(w, h, hit_n):
    #せいぜい 10 以下程度を想定 255 は超えないだろう。
    assert (((earth[w][h] & 0xFF0000) >> 16) + hit_n ) < 256
    earth[w][h] += (hit_n << 16)

now_day = 1
dead_n = 0
disappear_n = 0
late_disappear_n = 0
mhlw_dead_n = 0
serious_beds_rate=0.0
if use_jump_distance_change_flag and (jump_distance_change_days_early > 0):
    jump_distance_rate=jump_distance_rate_early
else:
    jump_distance_rate=jump_distance_rate_base

not_realized_person = 0

while True:
    state_n = [0] * 9
    check_list = [0] * 2
    mhlw_list = [0] * 5
    disappear_n += late_disappear_n
    late_disappear_n = 0

    if use_check or use_hold:
        for i in range(check_n):
            w=int(width*random.random())
            h=int(height*random.random())
            v = earth[w][h]
            state = v & 0xFF00
            if ( state == STATE0_INIT ) or ( state == STATE6_BLOCKER ):
                # 発熱した数を取り除けていない
                check_list[0] += 1
            if ( state == STATE2_SPREADER ):
                check_list[1] += 1
                if use_hold:
                    earth[w][h] |= HOLD_MARK
        
    serious_n = 0
    for w in range(width):
        for h in range(height):
            v = earth[w][h]
            state = v & 0xFF00
            mark= v & 0xFF000000
            if state == STATE3_SERIOUS:
                serious_n += 1

            if (v & 0xFFFF) == (STATE2_SPREADER | days2):
                not_realized_person += 1
                
            earth[w][h], d_n, serious_rate_list = next_state(v, random.random() > serious_beds_rate, serious_rate_list)
            late_disappear_n += d_n

            if ((state == STATE1_INFECTION) or (state == STATE2_SPREADER)) and ((mark & HOLD_MARK) != HOLD_MARK):
            
                hit_n = 0
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
                        new_v = STATE0_MARKED
                        if mark & MHLW_CHECK_MARK:
                            new_v |= MHLW_CHECK_MARK
                        earth[target_p[0]][target_p[1]] = new_v
                        hit_n += 1
                            
                if hit_n > 0:
                    add_r0(w, h, hit_n)

    if serious_n == 0:
        serious_beds_rate = 0.0
    else:
        serious_beds_rate = beds / serious_n

    for w in range(width):
        for h in range(height):
            v = earth[w][h]
            state = v & 0xFF00
            if state >= STATE7_NO_PERSON:
                continue;
            if (v & 0xFFFF) == STATE0_MARKED:
                # mark の引継ぎ。クラス化していないので苦労している
                earth[w][h] = 1 | (v & 0xFF000000)

            if state == STATE6_BLOCKER:
                # クラス化してないので苦労している
                # 治った人の感染させてしまった人の数
                add_hit_n = (v & 0xFF0000) >> 16
                state_n[8] += add_hit_n

            if state == STATE0_INIT:
                if (v & 0xFFFF) == STATE0_INIT:
                    state_n[0] += 1
                else:
                    state_n[7] += 1
            else:
                state_n[state >> 8] += 1

            if (v & MHLW_CHECK_MARK) == MHLW_CHECK_MARK:
                if state == STATE0_INIT:
                    add_index = None
                elif state == STATE1_INFECTION:
                    add_index = 0
                elif state == STATE2_SPREADER:
                    add_index = None
                elif state == STATE3_SERIOUS:
                    add_index = 1
                elif state == STATE4_DEAD:
                    mhlw_dead_n += 1
                    add_index = 2
                elif state == STATE5_REVIVE:
                    add_index = 3
                elif state == STATE6_BLOCKER:
                    add_index = 4
                else:
                    print(state, hex(v))
                    assert False
                if add_index != None:
                    mhlw_list[add_index] += 1

            if state == STATE4_DEAD:
                dead_n += 1
                earth[w][h] = STATE7_NO_PERSON

            #if ( v > 0 ) and ( v < 100):
            #    print('here', w, h, v, earth[w][h]);

    print(now_day, state_n, dead_n, mhlw_list, mhlw_dead_n, check_list if use_check else '', flush=True)

    now_day += 1
    if use_jump_distance_change_flag:
        old_rate = jump_distance_rate
        if now_day == jump_distance_change_days_early:
            jump_distance_rate = jump_distance_rate_base
        elif now_day == jump_distance_change_days_lator:
            jump_distance_rate = jump_distance_rate_lator
        if old_rate != jump_distance_rate:
            print("jump_distance_rate", old_rate, "->", jump_distance_rate)

    if (state_n[1] == 0) and (state_n[2] == 0) and (state_n[3] == 0) and (state_n[5] == 0) and (state_n[7] == 0):
        break
    for i in range(move_n):
        x0 = int(width*random.random())
        y0 = int(height*random.random())
        jdistance = jump_distance if random.random() < jump_distance_rate else jump_distance_long
        dx = int(jdistance*random.random() - jdistance/2)
        x1 = x0 + dx
        if (x1 >= width ) or ( x1 < 0 ):
            x1 = x0 - dx
        if (x1 >= width ) or ( x1 < 0 ):
            print(x1, x0, dx, jdistance)
        assert(not ((x1 >= width ) or ( x1 < 0 )))

        dy = int(jdistance*random.random() - jdistance/2)
        y1 = y0 + dy
        if (y1 >= height ) or (y1 < 0 ):
            y1 = y0 - dy
        if (y1 >= height ) or (y1 < 0 ):
            print(y1, y0, dx, jdistance)
        assert(not ((y1 >= height ) or (y1 < 0 )))
        v0 = earth[x0][y0]
        v1 = earth[x1][y1]
        s0 = v0 & 0xFF00
        s1 = v1 & 0xFF00
        if ( s0 != STATE8_MOLE ) and ( s1 != STATE8_MOLE ) and ( s0 != STATE1_INFECTION ) and ( s0 != STATE1_INFECTION ) and ( s0 != STATE3_SERIOUS ) and ( s1 != STATE3_SERIOUS) and ( s0 != STATE5_REVIVE) and ( s1 != STATE5_REVIVE ) :
            earth[x0][y0], earth[x1][y1] = v1, v0

print(state_n, state_n[6] / (width * height), dead_n)
no_spreader_n=0
for w in range(width):
    for h in range(height):
        v = earth[w][h]
        state = v & 0xFF00
        if state == STATE6_BLOCKER:
            if (v & 0xFF0000) > 0:
                no_spreader_n += 1
print(no_spreader_n, not_realized_person)
            
