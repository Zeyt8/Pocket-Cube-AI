from pocket_cube.cube import Cube
import numpy as np

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
    return np.sum(cube.state == cube.goal_state)
# %%
def manhattan(cube: Cube) -> int:
    return 0