from pocket_cube.cube import Cube
from pocket_cube.cube import Move
from utils import get_neighbors
import numpy as np
from typing import Callable

# neighbours of a certain square considering rotations as moves
square_neighbours = [[1,3,4,5], [0,2,4,5], [1,4,3,5], [0,2,4,5], [0,1,2,3], [0,1,2,3]]

def hamming(cube: Cube) -> int:
    """
    Returns the number of pieces that are not in the correct position.
    Not admisible.

    Args:
        cube (Cube): The cube to evaluate.
    
    Returns:
        int: The number of pieces that are not in the correct position.
    """
    return np.sum(cube.state != cube.goal_state)

def inverse_hamming(cube: Cube) -> int:
    """
    Returns the number of pieces that are in the correct position.
    Not admisible.

    Args:
        cube (Cube): The cube to evaluate.

    Returns:
        int: The number of pieces that are in the correct position.
    """
    return 24 - hamming(cube)

def blocked_hamming(cube: Cube) -> int:
    """
    Returns the number of faces that are not in the correct position, multiplied by 4.

    Args:
        cube (Cube): The cube to evaluate.

    Returns:
        int: The number of faces that are not in the correct position, multiplied by 4.
    """
    res: int = 0
    for i in range(6):
        for j in range(4):
            if cube.state[i * 4 + j] != cube.goal_state[i * 4 + j]:
                res += 1
                break
    return res * 4

def blocked_inverse_hamming(cube: Cube) -> int:
    """
    Returns the number of faces that are in the correct position, multiplied by 4.

    Args:
        cube (Cube): The cube to evaluate.

    Returns:
        int: The number of faces that are in the correct position, multiplied by 4.
    """
    return 24 - blocked_hamming(cube)

def __distance_to_correct_face(cube: Cube, square: int):
    """
    Returns the distance from a square to the correct face.

    Args:
        cube (Cube): The cube to evaluate.
        square (int): The square to evaluate.

    Returns:
        int: The distance from a square to the correct face.
    """
    color: int = cube.state[square]
    face: int = square // 4
    if color == face:
        return 0
    elif color in square_neighbours[face]:
        return 1
    else:
        return 2

def manhattan(cube: Cube) -> int:
    """
    Returns the sum of the distances from each square to the correct face.

    Args:
        cube (Cube): The cube to evaluate.

    Returns:
        int: The sum of the distances from each square to the correct face.
    """
    max_distance: int = 0
    for face in range(6):
        for i in range(face * 4, face * 4 + 4):
            distance: int = __distance_to_correct_face(cube, i)
            max_distance = max(max_distance, distance)
    return max_distance

def inverse_manhattan(cube: Cube) -> int:
    """
    Returns the sum of the distances from each square to the correct face, subtracted from the maximum.

    Args:
        cube (Cube): The cube to evaluate.

    Returns:
        int: The sum of the distances from each square to the correct face, subtracted from the maximum.
    """
    return 2 - manhattan(cube)

def build_database(max_depth: int = 7) -> dict[str, int]:
    """
    Builds a database of the distance to the solved state for each state with a depth lower than max_depth.

    Args:
        max_depth (int, optional): The maximum depth to search. Defaults to 7.

    Returns:
        dict[str, int]: The database.
    """
    database: dict[str, int] = {}
    frontier: list[tuple[Cube, int]] = [(Cube(), 0)]
    while frontier:
        (cube, depth) = frontier.pop()
        if cube.hash() not in database or database[cube.hash()] > depth:
            database[cube.hash()] = depth
            if depth < max_depth:
                for (neighbor, _) in get_neighbors(cube):
                    frontier.append((neighbor, depth + 1))
    return database

def database_heuristic(cube: Cube, database: dict[str, int], default_heuristic: Callable[[Cube], int]) -> int:
    """
    Returns a heuristic function that uses the databse heuristic if the entry exists, and the default heuristic otherwise.

    Args:
        default_heuristic (Callable[[Cube], int]): The default heuristic.

    Returns:
        int: The heuristic value.
    """
    if cube.hash() in database:
        return database[cube.hash()]
    else:
        return default_heuristic(cube)