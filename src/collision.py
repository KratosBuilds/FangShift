"""
Grid-friendly collision detection helpers for FangShift snake game.

This module provides collision detection logic for:
- Wall collisions (boundary checking)
- Self-collisions (snake hitting its own body)
"""

from typing import Tuple, List


def will_collide_wall(
    pos: Tuple[float, float],
    grid_width: int,
    grid_height: int,
    cell_size: float = 1.0
) -> bool:
    """
    Check if a position collides with the game boundaries.
    
    Args:
        pos: Current position (x, y) in game units
        grid_width: Width of the game grid in cells
        grid_height: Height of the game grid in cells
        cell_size: Size of each grid cell (default 1.0)
    
    Returns:
        True if position is outside boundaries, False otherwise
    """
    x, y = pos
    max_x = grid_width * cell_size
    max_y = grid_height * cell_size
    
    return x < 0 or x >= max_x or y < 0 or y >= max_y


def will_collide_self(
    head_pos: Tuple[float, float],
    body_positions: List[Tuple[float, float]],
    tolerance: float = 0.5
) -> bool:
    """
    Check if the snake's head collides with its own body.
    
    Args:
        head_pos: Position of the snake's head (x, y)
        body_positions: List of body segment positions (excluding head)
        tolerance: Distance threshold for collision detection (default 0.5)
    
    Returns:
        True if head collides with any body segment, False otherwise
    """
    head_x, head_y = head_pos
    
    for body_x, body_y in body_positions:
        # Calculate distance between head and body segment
        distance = ((head_x - body_x) ** 2 + (head_y - body_y) ** 2) ** 0.5
        if distance < tolerance:
            return True
    
    return False


def will_collide_next(
    current_pos: Tuple[float, float],
    velocity: Tuple[float, float],
    dt: float,
    body_positions: List[Tuple[float, float]],
    grid_width: int,
    grid_height: int,
    cell_size: float = 1.0,
    tolerance: float = 0.5
) -> Tuple[bool, str]:
    """
    Predict if the next position will result in a collision.
    
    Args:
        current_pos: Current head position (x, y)
        velocity: Current velocity (vx, vy)
        dt: Time step for prediction
        body_positions: List of body segment positions
        grid_width: Width of the game grid
        grid_height: Height of the game grid
        cell_size: Size of each grid cell (default 1.0)
        tolerance: Distance threshold for self-collision (default 0.5)
    
    Returns:
        Tuple of (will_collide: bool, collision_type: str)
        collision_type can be "wall", "self", or "none"
    """
    # Calculate next position
    next_x = current_pos[0] + velocity[0] * dt
    next_y = current_pos[1] + velocity[1] * dt
    next_pos = (next_x, next_y)
    
    # Check wall collision
    if will_collide_wall(next_pos, grid_width, grid_height, cell_size):
        return (True, "wall")
    
    # Check self collision
    if will_collide_self(next_pos, body_positions, tolerance):
        return (True, "self")
    
    return (False, "none")


def snap_to_grid(pos: Tuple[float, float], cell_size: float = 1.0) -> Tuple[int, int]:
    """
    Snap a continuous position to the nearest grid cell.
    
    Args:
        pos: Position (x, y) in game units
        cell_size: Size of each grid cell (default 1.0)
    
    Returns:
        Grid coordinates (grid_x, grid_y) as integers
    """
    x, y = pos
    grid_x = int(x / cell_size)
    grid_y = int(y / cell_size)
    return (grid_x, grid_y)


def will_grow(
    head_pos: Tuple[float, float],
    food_pos: Tuple[float, float],
    tolerance: float = 0.5
) -> bool:
    """
    Check if the snake's head is close enough to food to eat it.
    
    Args:
        head_pos: Position of the snake's head (x, y)
        food_pos: Position of the food (x, y)
        tolerance: Distance threshold for eating food (default 0.5)
    
    Returns:
        True if snake should grow (ate food), False otherwise
    """
    head_x, head_y = head_pos
    food_x, food_y = food_pos
    
    distance = ((head_x - food_x) ** 2 + (head_y - food_y) ** 2) ** 0.5
    return distance < tolerance
