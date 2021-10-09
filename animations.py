from enum import Enum
import tkinter as tk
import random
from screeninfo import get_monitors
from itertools import repeat

class Canvas:
 window: tk.Tk
 label: tk.Label
 resolution: any
 def __init__(self, window, label, resolution):
  self.window = window
  self.label = label
  self.resolution = resolution




class AnimationStates(Enum):
 IDLE = 0
 IDLE_TO_SLEEP = 1
 SLEEP = 2
 SLEEP_TO_IDLE = 3
 WALK_NEGATIVE = 4
 WALK_POSITIVE = 5
 GRABBED = 6
 FALLING = 7
 LANDED = 8



class Animation:
 """Defines the event numbers for this animation 
 and the ways this animation can transfer to the
 next animation
 """
 next_animation_states: list[AnimationStates]
 frames: list 
 frame_timer: int
 v_x: int
 v_y: int
 repititions: int # How many times to repeat given animation before moving onto the next animation
 frame_multiplier: int # Whether or not to duplicate frames (useful for fast updating animations)

 def __init__(self, next_animation_states, frames, frame_timer = 100, v_x = 0, v_y = 0, repititions = 0, frame_multiplier = 1):
    self.next_animation_states = next_animation_states
    self.frame_timer = frame_timer
    self.frames = [x for item in frames for x in repeat(item, frame_multiplier)]
    self.v_x = v_x
    self.v_y = v_y
    self.repititions = repititions

 def next(self, animator):
    if animator.repititions < self.repititions:
        animator.repititions += 1
        return animator.state
    else:
        animator.repititions = 0 
    return random.choice(self.next_animation_states)

 def get_velocity(self):
    return (self.v_x, self.v_y)


class Animator:
    frame_number: int
    state: AnimationStates
    animations: dict[AnimationStates, Animation]
    repititions: int

    def __init__(self, frame_number, state, animations):
        self.frame_number = frame_number
        self.state = state
        self.animations = animations
        self.repititions = 0

    def set_state(self, state):
        if (state == self.state):
            return
        self.frame_number = 0
        self.state = state


def get_animations(impath):
    idle = [tk.PhotoImage(file=impath+'idle.gif',format = 'gif -index %i' %(i)) for i in range(5)]#idle gif
    idle_to_sleep = [tk.PhotoImage(file=impath+'idle_to_sleep.gif',format = 'gif -index %i' %(i)) for i in range(8)]#idle to sleep gif
    sleep = [tk.PhotoImage(file=impath+'sleep.gif',format = 'gif -index %i' %(i)) for i in range(3)]#sleep gif
    sleep_to_idle = [tk.PhotoImage(file=impath+'sleep_to_idle.gif',format = 'gif -index %i' %(i)) for i in range(8)]#sleep to idle gif
    walk_positive = [tk.PhotoImage(file=impath+'walking_positive.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to left gif
    walk_negative = [tk.PhotoImage(file=impath+'walking_negative.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to right gif



    

    standing_actions = [AnimationStates.IDLE_TO_SLEEP]
    #make it less likely to sleep!
    standing_actions.extend(repeat(AnimationStates.IDLE, 3))
    standing_actions.extend(repeat(AnimationStates.WALK_NEGATIVE, 4))
    standing_actions.extend(repeat(AnimationStates.WALK_POSITIVE, 4))

    ANIMATIONS: dict[AnimationStates, Animation] = {
    AnimationStates.IDLE: Animation(
        standing_actions, 
        idle, frame_timer = 400),   
    AnimationStates.IDLE_TO_SLEEP: Animation(
        [AnimationStates.SLEEP], 
        idle_to_sleep),
    AnimationStates.SLEEP: Animation(
        [AnimationStates.SLEEP, AnimationStates.SLEEP, AnimationStates.SLEEP, AnimationStates.SLEEP, AnimationStates.SLEEP_TO_IDLE], 
        sleep, frame_timer = 1000),
    AnimationStates.SLEEP_TO_IDLE: Animation(
        [AnimationStates.IDLE], 
        sleep_to_idle),
    AnimationStates.WALK_POSITIVE: Animation(
        standing_actions, 
        walk_positive, v_x=3),
    AnimationStates.WALK_NEGATIVE: Animation(
        standing_actions, 
        walk_negative, v_x=-3),
    AnimationStates.GRABBED:  Animation(
        [AnimationStates.GRABBED], 
        walk_positive, frame_timer=50),
    AnimationStates.FALLING:  Animation(
        [AnimationStates.FALLING], 
        walk_negative, frame_timer=10,
        frame_multiplier = 2),
    }
    ANIMATIONS[AnimationStates.LANDED] = ANIMATIONS[AnimationStates.IDLE]

    
    assert(len(AnimationStates) == len(ANIMATIONS.keys()))
    return ANIMATIONS



