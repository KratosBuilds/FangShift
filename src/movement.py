from dataclasses import dataclass
from typing import Tuple

@dataclass
class MovementState:
    pos: Tuple[float, float]
    direction: Tuple[int, int]
    speed: float     # cells per second (or pixels per second)
    velocity: Tuple[float, float] = (0.0, 0.0)

def apply_input(state: MovementState, input_dir: Tuple[int, int], dt: float, accel: float = 10.0):
    """
    input_dir: (-1,0),(1,0),(0,-1),(0,1) or (0,0)
    dt: delta time in seconds
    accel: acceleration factor
    """
    # target velocity in units/sec
    target_v = (input_dir[0] * state.speed, input_dir[1] * state.speed)
    vx = state.velocity[0] + (target_v[0] - state.velocity[0]) * min(accel * dt, 1.0)
    vy = state.velocity[1] + (target_v[1] - state.velocity[1]) * min(accel * dt, 1.0)
    state.velocity = (vx, vy)

    # integrate position
    state.pos = (state.pos[0] + vx * dt, state.pos[1] + vy * dt)
    return state
