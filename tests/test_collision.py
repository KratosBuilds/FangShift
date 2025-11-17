"""
Unit tests for collision detection helpers.

Tests cover wall collision, self-collision, and food eating logic
for both grid-based and smooth movement modes.
"""

import pytest
from src.collision import (
    will_collide_wall,
    will_collide_self,
    will_collide_next,
    snap_to_grid,
    will_grow
)


class TestWallCollision:
    """Test wall collision detection."""
    
    def test_inside_boundaries(self):
        """Position inside grid should not collide."""
        assert not will_collide_wall((5.0, 5.0), 10, 10, 1.0)
        assert not will_collide_wall((0.0, 0.0), 10, 10, 1.0)
        assert not will_collide_wall((9.9, 9.9), 10, 10, 1.0)
    
    def test_outside_left_boundary(self):
        """Position left of grid should collide."""
        assert will_collide_wall((-0.1, 5.0), 10, 10, 1.0)
        assert will_collide_wall((-5.0, 5.0), 10, 10, 1.0)
    
    def test_outside_right_boundary(self):
        """Position right of grid should collide."""
        assert will_collide_wall((10.0, 5.0), 10, 10, 1.0)
        assert will_collide_wall((15.0, 5.0), 10, 10, 1.0)
    
    def test_outside_top_boundary(self):
        """Position above grid should collide."""
        assert will_collide_wall((5.0, -0.1), 10, 10, 1.0)
        assert will_collide_wall((5.0, -5.0), 10, 10, 1.0)
    
    def test_outside_bottom_boundary(self):
        """Position below grid should collide."""
        assert will_collide_wall((5.0, 10.0), 10, 10, 1.0)
        assert will_collide_wall((5.0, 15.0), 10, 10, 1.0)
    
    def test_different_cell_sizes(self):
        """Wall collision with different cell sizes."""
        # cell_size = 2.0, 10x10 grid means max = 20x20
        assert not will_collide_wall((10.0, 10.0), 10, 10, 2.0)
        assert will_collide_wall((20.0, 10.0), 10, 10, 2.0)
        assert will_collide_wall((10.0, 20.0), 10, 10, 2.0)


class TestSelfCollision:
    """Test self-collision detection."""
    
    def test_no_body_no_collision(self):
        """Empty body list should not collide."""
        assert not will_collide_self((5.0, 5.0), [], 0.5)
    
    def test_far_from_body(self):
        """Head far from body should not collide."""
        body = [(1.0, 1.0), (2.0, 1.0), (3.0, 1.0)]
        assert not will_collide_self((10.0, 10.0), body, 0.5)
    
    def test_collision_with_body(self):
        """Head touching body segment should collide."""
        body = [(5.0, 5.0), (6.0, 5.0), (7.0, 5.0)]
        # Head at same position as first body segment
        assert will_collide_self((5.0, 5.0), body, 0.5)
        # Head very close to second body segment
        assert will_collide_self((6.1, 5.0), body, 0.5)
    
    def test_tolerance_threshold(self):
        """Test collision tolerance parameter."""
        body = [(5.0, 5.0)]
        # Just outside tolerance
        assert not will_collide_self((5.6, 5.0), body, 0.5)
        # Just inside tolerance
        assert will_collide_self((5.4, 5.0), body, 0.5)
        # Larger tolerance
        assert will_collide_self((5.6, 5.0), body, 1.0)
    
    def test_diagonal_collision(self):
        """Test collision at diagonal positions."""
        body = [(5.0, 5.0)]
        # Diagonal distance ~0.42 < 0.5
        assert will_collide_self((5.3, 5.3), body, 0.5)
        # Diagonal distance ~0.71 > 0.5
        assert not will_collide_self((5.5, 5.5), body, 0.5)


class TestCollideNext:
    """Test predictive collision detection."""
    
    def test_no_collision_predicted(self):
        """Next position with no collision."""
        will_collide, col_type = will_collide_next(
            current_pos=(5.0, 5.0),
            velocity=(1.0, 0.0),
            dt=0.1,
            body_positions=[],
            grid_width=10,
            grid_height=10
        )
        assert not will_collide
        assert col_type == "none"
    
    def test_wall_collision_predicted(self):
        """Predict wall collision."""
        will_collide, col_type = will_collide_next(
            current_pos=(9.5, 5.0),
            velocity=(10.0, 0.0),  # Moving right fast
            dt=0.1,  # Next pos would be 10.5
            body_positions=[],
            grid_width=10,
            grid_height=10
        )
        assert will_collide
        assert col_type == "wall"
    
    def test_self_collision_predicted(self):
        """Predict self collision."""
        body = [(6.0, 5.0), (7.0, 5.0)]
        will_collide, col_type = will_collide_next(
            current_pos=(5.0, 5.0),
            velocity=(5.0, 0.0),  # Moving right
            dt=0.15,  # Next pos would be 5.75, close to 6.0
            body_positions=body,
            grid_width=10,
            grid_height=10,
            tolerance=0.5
        )
        assert will_collide
        assert col_type == "self"
    
    def test_wall_priority_over_self(self):
        """Wall collision detected before self collision."""
        body = [(11.0, 5.0)]  # Outside grid
        will_collide, col_type = will_collide_next(
            current_pos=(9.5, 5.0),
            velocity=(10.0, 0.0),
            dt=0.1,
            body_positions=body,
            grid_width=10,
            grid_height=10
        )
        # Should detect wall first
        assert will_collide
        assert col_type == "wall"


class TestSnapToGrid:
    """Test grid snapping utility."""
    
    def test_exact_grid_positions(self):
        """Exact grid positions should snap correctly."""
        assert snap_to_grid((0.0, 0.0), 1.0) == (0, 0)
        assert snap_to_grid((5.0, 3.0), 1.0) == (5, 3)
        assert snap_to_grid((10.0, 10.0), 1.0) == (10, 10)
    
    def test_fractional_positions(self):
        """Fractional positions should snap to floor."""
        assert snap_to_grid((5.3, 3.7), 1.0) == (5, 3)
        assert snap_to_grid((0.9, 0.9), 1.0) == (0, 0)
        assert snap_to_grid((9.99, 9.01), 1.0) == (9, 9)
    
    def test_different_cell_sizes(self):
        """Snapping with different cell sizes."""
        assert snap_to_grid((10.0, 10.0), 2.0) == (5, 5)
        assert snap_to_grid((15.0, 9.0), 3.0) == (5, 3)
        assert snap_to_grid((0.5, 0.5), 0.5) == (1, 1)
    
    def test_negative_positions(self):
        """Negative positions should snap correctly."""
        assert snap_to_grid((-1.0, -1.0), 1.0) == (-1, -1)
        assert snap_to_grid((-0.5, -0.5), 1.0) == (0, 0)


class TestWillGrow:
    """Test food eating detection."""
    
    def test_exact_food_position(self):
        """Head at exact food position should eat."""
        assert will_grow((5.0, 5.0), (5.0, 5.0), 0.5)
    
    def test_close_to_food(self):
        """Head close to food should eat."""
        assert will_grow((5.0, 5.0), (5.3, 5.0), 0.5)
        assert will_grow((5.0, 5.0), (5.0, 5.4), 0.5)
        # Diagonal ~0.42 < 0.5
        assert will_grow((5.0, 5.0), (5.3, 5.3), 0.5)
    
    def test_far_from_food(self):
        """Head far from food should not eat."""
        assert not will_grow((5.0, 5.0), (10.0, 10.0), 0.5)
        assert not will_grow((5.0, 5.0), (5.6, 5.0), 0.5)
    
    def test_tolerance_threshold(self):
        """Test food eating tolerance."""
        # Just outside default tolerance
        assert not will_grow((5.0, 5.0), (5.6, 5.0), 0.5)
        # Inside larger tolerance
        assert will_grow((5.0, 5.0), (5.6, 5.0), 1.0)
    
    def test_diagonal_food_eating(self):
        """Test eating food at diagonal positions."""
        # Diagonal distance ~0.71 > 0.5
        assert not will_grow((5.0, 5.0), (5.5, 5.5), 0.5)
        # Diagonal distance ~0.71 < 1.0
        assert will_grow((5.0, 5.0), (5.5, 5.5), 1.0)
