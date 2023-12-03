from typing import Callable
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

def test(algorithm: Callable[[Cube], list[Move]], tests: list[list[Move]]) -> bool:
    """
    Tests the algorithm with the given tests.

    Args:
        algorithm (Callable[[Cube], list[Move]]): The algorithm to test.
        tests (list[list[Move]]): The tests to run.

    Returns:
        bool: True if all tests passed, False otherwise.
    """
    passed: bool = True
    for idx, test in enumerate(tests):
        cube: Cube = Cube(test)
        path: list[Move] = algorithm(cube)
        for move in path:
            cube = cube.move(move)
        if not is_solved(cube):
            print(f"Test {idx} failed")
            passed = False
        else:
            print(f"Test {idx} passed")
    return passed