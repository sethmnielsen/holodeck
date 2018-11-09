import time

SHORT_TEST = 240
MEDIUM_TEST = 1000
LONG_TEST = 5000

WARP_SPEED = 600

def average_resting_framerate(world, frames):
    import holodeck
    
    with holodeck.make(world) as env:
        start_time = time.perf_counter()
        for x in range(0, frames):
            env.tick()
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        real_fps = frames / elapsed_time
        c_fraction = real_fps/WARP_SPEED

        print("Got {} frames in {:.5f}s, fps = {:.2f} ({:.2f}c)".format(frames, elapsed_time, real_fps, c_fraction))

        return real_fps, c_fraction

def test_average_framerate():
    results = average_resting_framerate("UrbanCity", SHORT_TEST)
    results = average_resting_framerate("UrbanCity", MEDIUM_TEST)
    # results = average_resting_framerate("UrbanCity", LONG_TEST)

    # If we dip below .1c, fail the test
    assert results[1] > 0.1, "Simulation ran at {:.2f}c! ({:.2f} fps)".format(results[1], results[0])