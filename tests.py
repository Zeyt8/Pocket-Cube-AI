from typing import Callable
import time
from pocket_cube.cube import Cube, Move

case1 = "R U' R' F' U"
case2 = "F' R U R U F' U'"
case3 = "F U U F' U' R R F' R"
case4 = "U' R U' F' R F F U' F U U"

# list of tests
test_list: list[list[Move]] = list(
    map(lambda t: list(map(Move.from_str, t.split(" "))),
        [case1, case2, case3, case4])
    )

def is_solved(cube: Cube) -> bool:
    """
    Checks if the cube is solved.

    Args:
        cube (Cube): The cube to check.

    Returns:
        bool: True if the cube is solved, False otherwise.
    """
    for i in range(len(cube.state)):
        if cube.state[i] != cube.goal_state[i]:
            return False
    return True

def test(algorithm: Callable[[Cube], list[Move]], tests: list[list[Move]], log: bool = True) -> list[tuple[bool, float, int, int]]:
    """
    Tests the algorithm with the given tests.

    Args:
        algorithm (Callable[[Cube], list[Move]]): The algorithm to test.
        tests (list[list[Move]]): The tests to run.

    Returns:
        list[tuple[float, int, int]]: The time taken, the number of states expanded and the length of the path for each test.
    """
    res: list[tuple[bool, float, int, int]] = []
    for idx, test in enumerate(tests):
        success: bool = True
        cube: Cube = Cube(test)
        start = time.time()
        (path, states) = algorithm(cube)
        end = time.time()
        for move in path:
            cube = cube.move(move)
        if not is_solved(cube):
            if log:
                print(f"Test {idx} failed. Time: {end - start} seconds. States expanded: {states}. Path length: {len(path)}")
            success = False
        else:
            if log:
                print(f"Test {idx} passed. Time: {end - start} seconds. States expanded: {states}. Path length: {len(path)}")
        res.append((success, end - start, states, len(path)))
    return res