import sys, os

def main(config):
    # Get the local holodeck installation and not the system (pip) one
    # assumes that the script is run from the root of the holodeck repo
    # TODO: Improve this so it's less brittle
    sys.path.insert(0, os.getcwd())
    
    import holodeck


# Run from command line
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Performance testing for holodeck")
    parser.add_argument("--goal-speed", "-gs", type=int, help="Target framerate", default=600, required=False)
    config = vars(parser.parse_args())
    results = main(config)

