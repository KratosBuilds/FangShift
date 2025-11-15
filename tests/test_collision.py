import pytest
from src.collision import check_wall_collision, check_self_collision, will_collide_next

def test_check_wall_collision_inside():
    assert not check_wall_collision((2, 3), width=10, height=10)

def test_check_wall_collision_outside():
    assert check_wall_collision((-1, 0), width=10, height=10)
    assert check_wall_collision((10, 0), width=10, height=10)
    assert check_wall_collision((0, 10), width=10, height=10)

def test_check_self_collision_empty():
    assert not check_self_collision([])

def test_check_self_collision_no_collision():
    snake = [(2,2), (2,1), (2,0)]
    assert not check_self_collision(snake)

def test_check_self_collision_hit():
    snake = [(2,2), (3,2), (2,2), (2,1)]
    assert check_self_collision(snake)

def test_will_collide_next_wall():
    assert will_collide_next((9,5), (1,0), [(9,5)], width=10, height=10) is True

def test_will_collide_next_self_no_grow():
    snake = [(2,2), (2,3), (2,4)]
    # moving up into the tail cell should be allowed if not growing because tail vacates
    assert will_collide_next((2,3), (0,1), snake, width=10, height=10, will_grow=False) is False

def test_will_collide_next_self_grow():
    snake = [(2,2), (2,3), (2,4)]
    # if growing, moving into the tail is a collision
    assert will_collide_next((2,3), (0,1), snake, width=10, height=10, will_grow=True) is True