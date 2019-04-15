import holodeck
import numpy as np
import time

env = holodeck.make("UrbanCity")
command = np.array([0,0,0,100])

t0 = time.time()
t1 = 0
t2 = 0
avg_fps = 0

for i in range(1,1000):
    t1 = time.time()
    state, _, _, _ = env.step(command)
    t2 = time.time()

    fps = 1/(t2 - t1)
    avg_fps = i/(t1 - t0)

    print("FPS:    ", fps)
    print("\nFPS_AVG:", avg_fps)
