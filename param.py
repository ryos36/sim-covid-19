width=1920
height=1080

r0=2.0
move_n=int(width*height * 0.1)
around=8
beds=int(width*height/1000)
jump_distance_long = int(width * 0.5)
jump_distance = int(width * 0.1)
jump_distance_rate=0.9
spreader_rate=0.5
days0=1
days1=12
days2=7
rate=r0/(days2 * around)
serious_rate=0.1/days1
serious_days=10
dead_rate=0.1/serious_days
revive_days=10

