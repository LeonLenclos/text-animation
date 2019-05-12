#!/usr/bin/env python3

import sys, os, time, re, argparse, subprocess

CLEAR = 'clear' if os.name == 'posix' else 'CLS'
# TODO: get_term_width, get_term_height and get_term_dimensions are curently
# not working for non-unix users.
SIZE = 'stty', 'size'

def clear():
    """Clear the terminal"""
    os.system(CLEAR)

def get_term_width():
    """Return the width of the terminal"""
    return get_term_dimensions()[0]

def get_term_height():
    """Return the height of the terminal"""
    return get_term_dimensions()[1]

def get_term_dimensions():
    """Return the width and the height of the terminal in a tuple"""
    height, width = subprocess.check_output(SIZE).split()
    return int(width), int(height)

class TextImage(str):
    """TextImage inherit from str and add some methods usefull for playing
       frames in a text animation"""

    def get_lines(self):
        """Return a list of splited lines"""
        return self.split('\n')

    def get_width(self):
        """Return the width of the frame (length of the longest line)"""
        return max(map(len, self.get_lines()))

    def get_height(self):
        """Return the height of the frame (number of lines)"""
        return len(self.get_lines())

    def show(self, x_offset=0, y_offset=0, delay=0):
        """Print the TextImage and sleep during a delay."""
        clear()
        sys.stdout.write(y_offset * '\n')
        for line in self.get_lines():
            sys.stdout.write(x_offset * ' ')
            sys.stdout.write(line)
            sys.stdout.write('\n')
        end_lines = get_term_height() - self.get_height() - y_offset - 1
        sys.stdout.write(end_lines * '\n')
        sys.stdout.flush()
        time.sleep(delay)


class TextAnimation():
    """TextAnimation is the class for text animations."""

    def __init__(self, frames=[]):
        """Init a TextAnimation with a list of str, a list of TextImage or
           nothing."""
        # All the frames are converted to TextImage objects.
        self.frames = list(map(TextImage, frames))

    def get_width(self):
        """Return the width of the widest frame"""
        return max(map(TextImage.get_width, self.frames))

    def get_height(self):
        """return the height of the highter frame"""
        return max(map(TextImage.get_height, self.frames))

    def read(self, center=True, loop=0, delay=0.1):
        """
        Read the text animation
        set loop to 0 for forever loop.
        """
        x_offset = y_offset = 0
        if center:
            x_offset = int(get_term_width()/2 - self.get_width()/2)
            y_offset = int(get_term_height()/2 - self.get_height()/2)

        i = 0
        while i < loop or loop == 0:
            for frame in self.frames:
                frame.show(x_offset, y_offset, delay)
            i += 1


def read_ta(file_name, separator='#'):
    """
    Read a text animation file.
    Take a `file_name` and return a list of strings (frames of the animation).
    In the file frames are separated by `separator` by default it is '#''
    """
    with open(file_name, 'r') as f:
        frames = f.read().split('#')
    return [frm for frm in frames if len(frm)>0 and frm != '\n']

def main():
    parser = argparse.ArgumentParser(description='Animate an .animtxt file.')
    parser.add_argument('file', type=str, nargs=1,
                        help='an .ta (text animation) file')
    parser.add_argument('--delay', '-d', type=int, default=0.1,
                        help='the delay between frames in seconds')
    parser.add_argument('--loop', '-l', type=int, default=0,
                        help='number of loops to play (default is infinte loop)')
    args = parser.parse_args()

    anim = TextAnimation(read_ta(args.file[0]))
    anim.read(delay=args.delay)

if __name__ == '__main__':
    main()
