from typing import List, Tuple

Position = Tuple[int, int]

def check_wall_collision(pos: Position, width: int, height: int) -> bool:
    """Return True if pos is outside the playfield (0..width-1, 0..height-1)."""
    x, y = pos
    return x < 0 or y < 0 or x >= width or y >= height

def check_self_collision(snake_body: List[Position]) -> bool:
    """
    Given a list of positions representing the snake from head to tail,
    return True if the head collides with any other segment.
    """
    if not snake_body:
        return False
    head = snake_body[0]
    return head in snake_body[1:]

def will_collide_next(head: Position, direction: Position, snake_body: List[Position],
                      width: int, height: int, will_grow: bool = False) -> bool:
    """
    Check whether the next head position will collide (wall or self).
    will_grow: if True, tail does not vacate this turn (e.g. after eating), so check against full body.
    """
    next_pos = (head[0] + direction[0], head[1] + direction[1])
    if check_wall_collision(next_pos, width, height):
        return True

    # If the snake will grow, tail remains; otherwise tail will vacate and last segment can be ignored.
    if will_grow:
        return next_pos in snake_body
    else:
        # when not growing, the tail cell is freed, so consider snake_body except last element
        return next_pos in snake_body[:-1]