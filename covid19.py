import random

width=1920
height=1080
earth=[[0]*height for i in range(width)]
#print(len(earth[0]))
earth[int(width*random.random())][int(height*random.random())] = 2 
#print(earth[1079][1919])
r0=1.8
days0=1
days1=14
move_n=int(width*height * 0.1)
days=days0+days1
around=8
pos = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, -1), (-1, 1), (0, 1), (1, 1)]
rate=r0/(days1 * around)
print(rate)

now_day = 1
while True:
    for w in range(width):
        for h in range(height):
            v = earth[w][h]
            if (0 < v) and (v <= days):
                earth[w][h] += 1
                if ( v <= days0 ):
                    continue
                for p in pos:
                    target_p = tuple(map(lambda x,y:x+y, (w, h), p))
                    if ((target_p[0] < 0) or (width <= target_p[0]) or
                        (target_p[1] < 0) or (height <= target_p[1])):
                        continue

                    if earth[target_p[0]][target_p[1]] != 0 :
                        continue

                    r = random.random()
                    hit = (r < rate)
                    #print(r, rate, hit)
                    if hit:
                        earth[target_p[0]][target_p[1]] = 1

    n = 0
    done_n = 0
    for w in range(width):
        for h in range(height):
            v = earth[w][h]
            if (0 < v) and (v <= days):
                n += 1
                #print(w, h, earth[w][h])
            elif ( days < v ):
                done_n += 1
    print(now_day, n, done_n, flush=True)
    now_day += 1
    if n == 0:
        print(done_n, done_n / (width * height))
        break
    for i in range(move_n):
        x0 = int(width*random.random())
        y0 = int(height*random.random())
        x1 = int(width*random.random())
        y1 = int(height*random.random())
        earth[x0][y0], earth[x1][y1] = earth[x1][y1], earth[x0][y0]


