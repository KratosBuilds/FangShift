import time
from src.movement import MovementState, apply_input

def fake_input_sequence(step):
    # Example: move right for 1s, then down
    if step < 60:
        return (1, 0)
    else:
        return (0, 1)

def main():
    state = MovementState(pos=(0.0, 0.0), direction=(1,0), speed=100.0)
    fps = 60.0
    dt = 1.0 / fps
    for step in range(120):
        inp = fake_input_sequence(step)
        state = apply_input(state, inp, dt, accel=8.0)
        print(f"step={{step}} pos={{state.pos}} vel={{state.velocity}}")
        time.sleep(0.01)

if __name__ == "__main__":
    main()
