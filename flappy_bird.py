#!/opt/homebrew/bin/python3.11

################################
# CREDITS:
# AmerikanisherAdler 
# Rugmonkey09
################################

import threading
import curses
from curses import wrapper
import time
import random

#vars
start_time = time.time()
speed = 4.0
accel = 0.05
score = 0
stop = True

def welcome(stdscr):
    height, width = stdscr.getmaxyx()
    x = (width - len("|_|   |_||__,_| .__/| .__/|___. | |____/|_|_|  |__,_|")) // 2
    y = height // 3 
    center = (width - len("Press any key to begin!")) // 2
    stdscr.clear()
    stdscr.addstr(y-5, x, "")
    stdscr.addstr(y-4, x, " _____ _                           ____            _ ")
    stdscr.addstr(y-3, x, "|  ___| |                         |  _ \\          | |")
    stdscr.addstr(y-3, x+40, "(•}", curses.color_pair(4))
    stdscr.addstr(y-2, x, "| |__ | | __ _ _ __  _ __  _   _  | |_) |_ _ __ __| |", curses.color_pair(4))
    stdscr.addstr(y-1, x, "|  __|| |/ _' | '_ \\| '_ \\| | | | |  _ <| | '__/ _' |", curses.color_pair(4))
    stdscr.addstr(y+0, x, "| |   | | (_| | |_) | |_) | |_| | | |_) | | | | (_| |")
    stdscr.addstr(y+1, x, "|_|   |_|\\__,_| .__/| .__/\\___. | |____/|_|_|  \\__,_|")
    stdscr.addstr(y+2, x, "              | |   | |    ___/ |                    ")
    stdscr.addstr(y+3, x, "              |_|   |_|   |____/                     ")
    stdscr.addstr(y+4, x, "")
    stdscr.addstr(y+5, x+30, "[Developed by: AmerikanischerAdler]")
    stdscr.addstr(y+5, x+45, "AmerikanischerAdler", curses.color_pair(4))
    stdscr.addstr(y+8, center, "Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display(stdscr, fy, score, pipe_num1, pipe_num2):
    height, width = stdscr.getmaxyx()
    fx = (width - len("(•}")) // 5
    border_str = str("/" * width)
    x_instructions = (width - len("Press SPACE to flap")) // 2
    
    stdscr.addstr(0, 0, f"{border_str}")
    stdscr.addstr(fy, fx - 1, "(", curses.color_pair(4))
    stdscr.addstr(fy, fx, "•", curses.color_pair(4))
    stdscr.addstr(fy, fx + 1, "}", curses.color_pair(4))
    stdscr.addstr(height - 2, 0, f"{border_str}")
    stdscr.addstr(height - 1, x_instructions, "Press SPACE to flap")
    stdscr.addstr(height - 1, 0, f"Score: {score}", curses.color_pair(1))

    # pipes
    pipe_list = []
    pipe_x = width // 2 - 5
    pipe_top = 1
    pipe_bottom = height - 3
    tpipe = Pipes(pipe_x, pipe_top)
    bpipe = Pipes(pipe_x, pipe_bottom)
    stdscr.addstr(tpipe.y, tpipe.x, "|          |", curses.color_pair(1))

    # top pipes
    for num in range(pipe_num1 - 3):
        pipe_top_new = pipe_top + 1 + num
        newpipe = Pipes(pipe_x, pipe_top_new)
        pipe_list += newpipe.coords
        stdscr.addstr(newpipe.y, newpipe.x, "|          |", curses.color_pair(1))
        
    pipe_cap_top = Pipes(pipe_x, pipe_top_new + 1)
    pipe_list += pipe_cap_top.coords
    stdscr.addstr(pipe_cap_top.y, pipe_cap_top.x, "============", curses.color_pair(1))

    # bottom pipes
    for i in range(pipe_num2 - 3):
        pipe_bottom_new = pipe_bottom - i
        new_pipe = Pipes(pipe_x, pipe_bottom_new)
        pipe_list += new_pipe.coords
        stdscr.addstr(new_pipe.y, new_pipe.x, "|          |", curses.color_pair(1))
        
    pipe_cap_bottom = Pipes(pipe_x, pipe_bottom_new - 1)
    pipe_list += pipe_cap_bottom.coords
    stdscr.addstr(pipe_cap_bottom.y, pipe_cap_bottom.x, "============", curses.color_pair(1))

    # debugging
    lenp = pipe_list[1]
    stdscr.addstr(1, 0, f"{lenp}")


# movement of pipes
class Pipes():
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y 
        self.coords = (self.x, self.y)

    def move(self, x, y):
        self.x += x 
        self.y += y

# score
def score_func():
    global flappy_dies
    global score

    while not flappy_dies:
        time.sleep(speed - ((time.time() - start_time) % speed))
        score += 1

# gravity
def gravity():
    global flappy_dies
    global fy
    global accel
    global fall_vel

    while not flappy_dies:
        time.sleep(fall_vel - ((time.time() - start_time) % fall_vel))
        fy += 1

        if fall_vel > 0.25:
            fall_vel -= accel
            accel += 0.05
        elif fall_vel > 0.1:
            fall_vel -= 0.01

def game(stdscr):
    stdscr.nodelay(True)
    height, width = stdscr.getmaxyx()
    pipe_num1 = random.randint(4, (height // 2))
    pipe_num2 = height - pipe_num1 - 8

    global fy
    fy = height // 2
    global score
    score = 0
    global accel 
    accel = 0.05
    global flappy_dies
    flappy_dies = False
    global fall_vel
    fall_vel = 0.75

    grav = threading.Thread(target=gravity)
    grav.start()

    score_thread = threading.Thread(target=score_func)
    score_thread.start()

    while True:
        stdscr.erase()
        display(stdscr, fy, score, pipe_num1, pipe_num2)
        stdscr.refresh()

        # flappy dies
        if fy < 1 or fy > height - 3:
            accel = 0.05
            score = 0

            stdscr.nodelay(False)
            flappy_dies = True

            grav.join()
            score_thread.join()
            break

        try:
            key = stdscr.getkey()
        except:
            continue
 
        if ord(key) == 32:
            if fy > 2:
                fy -= 2
                accel = 0.05
                fall_vel = 0.75
            elif fy == 2:
                fy -= 1
                accel = 0.05
                fall_vel = 0.75
       
        if ord(key) == 27:
            accel = 0.05
            fall_vel = 0.75
            flappy_dies = True
            stdscr.nodelay(False) 
            break

"""
the pipes move left at $speed based on $level
when not complete space around flappy's front, he dies
"""

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    welcome(stdscr) 

    height, width = stdscr.getmaxyx()
    h_middle = height // 2 
    w_middle = (width - len("Press any key to play again...")) // 2 
    a_middle = (width - len("Flappy Died. :(")) // 2 
    t_middle = (width - len("Press ESC to exit")) // 2 

    while True:
        game(stdscr)
        stdscr.addstr(h_middle - 2, a_middle, "Flappy Died. :(", curses.color_pair(2))
        stdscr.addstr(h_middle, w_middle, "Press any key to play again...", curses.A_BOLD)
        stdscr.addstr(h_middle + 2, t_middle, "Press ESC to exit")
        key = stdscr.getkey()
		
        if ord(key) == 27:
	        break

if __name__ == "__main__":
    wrapper(main)

