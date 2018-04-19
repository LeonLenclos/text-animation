import sys, os, time, re, argparse, subprocess
CLEAR = 'clear' if os.name == 'posix' else 'CLS'


def anim(frames, delay=0.1):
    """Anim a list of strings with a delay"""

    # Get console dimensions
    console_height, console_width = subprocess.check_output(['stty', 'size']).split()
    console_height, console_width = int(console_height), int(console_width)

    print(console_height, console_width)

    # Get animation dimensions
    width, height = 0, 0
    for frame in frames:
        lines = frame.split("\n")
        if len(lines) > height:
            height = len(lines)
        for line in lines:
            if len(line)> width:
                width = len(line)

    # Get offset for centering
    offset_x = int(console_width/2 - width/2)
    offset_y = int(console_height/2 - height/2)

    # Center frames in the console
    for i, frame in enumerate(frames):
        lines = [" " * offset_x + line for line in frame.split("\n")]
        frames[i] = "\n" * offset_y + "\n".join(lines)

    # Step through forever, frame by frame
    while True:
        for frame in frames:
            # Clear the console
            os.system(CLEAR)


            # Write the current frame on stdout and sleep
            sys.stdout.write(frame + "\n")
            sys.stdout.flush()
            time.sleep(delay)

def read_anitxt(file_name):
    with open(file_name, 'r') as f:
        frames = f.read().split('#')
    return [frm for frm in frames if len(frm)>0 and frm != '\n']



parser = argparse.ArgumentParser(description='Animate an .animtxt file.')
parser.add_argument('file', type=str, nargs=1,
                    help='an .animtxt file')
parser.add_argument('--delay', '-d', type=int, default=0.1,
                    help='the delay between frames in seconds)')
args = parser.parse_args()

anim(read_anitxt(args.file[0]), delay=args.delay)
