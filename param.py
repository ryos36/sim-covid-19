width=1920
height=1080

r0=1.8
move_n=int(width*height * 0.1)
around=8
beds=int(width*height/1000)
jump_distance_long = int(width * 0.5)
jump_distance = int(width * 0.1)
jump_distance_rate_early=1.0
jump_distance_rate_base=0.9
use_jump_distance_change_flag=True
jump_distance_change=120
spreader_rate=0.7
days0=1
days1=12
days2=7
rate=r0/(days2 * around)
serious_rate=0.05/days1
serious_days=10
dead_rate=0.05/serious_days
revive_days=10

