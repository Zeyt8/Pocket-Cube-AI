from typing import Callable
import time
from pocket_cube.cube import Cube, Move
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

case1 = "R U' R' F' U"
case2 = "F' R U R U F' U'"
case3 = "F U U F' U' R R F' R"
case4 = "U' R U' F' R F F U' F U U"

# list of tests
test_list: list[list[Move]] = list(
    map(lambda t: list(map(Move.from_str, t.split(" "))),
        [case1, case2, case3, case4])
    )

TestCase = tuple[bool, float, int, int]

def is_solved(cube: Cube) -> bool:
    """
    Checks if the cube is solved.

    Args:
        cube (Cube): The cube to check.

    Returns:
        bool: True if the cube is solved, False otherwise.
    """
    return np.array_equal(cube.state, cube.goal_state)

def test(algorithm: Callable[[Cube], tuple[list[Move], int]], tests: list[list[Move]], log: bool = True) -> list[TestCase]:
    """
    Tests the algorithm with the given tests.

    Args:
        algorithm (Callable[[Cube], list[Move]]): The algorithm to test.
        tests (list[list[Move]]): The tests to run.

    Returns:
        list[tuple[float, int, int]]: The time taken, the number of states expanded and the length of the path for each test.
    """
    res: list[TestCase] = []
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

def test_mcts(algorithm: Callable[[Cube, int, float, Callable[[Cube], int]], tuple[list[Move], int]], heuristic_list: list[Callable[[Cube], int]]) -> None:
    for heuristic in heuristic_list:
        for c in [0.1, 0.5]:
            for budget in [1000, 5000, 10000, 20000]:
                print(f"Heuristic: {heuristic.__name__} Budget: {budget}, c: {c}")
                test_results: list[list[TestCase]] = []
                for _ in range(0, 20):
                    test_results.append(test(lambda cube: algorithm(cube, budget, c, heuristic), test_list, False))
                # compute average test result
                test_results_averaged = []
                for i in range(len(test_list)):
                    # average for test i
                    test_result: tuple[float, int, int] = (0, 0, 0)
                    no_passed: int = 0
                    for result in test_results:
                        if result[i][0]:
                            no_passed += 1
                            test_result = (test_result[0] + result[i][1], test_result[1] + result[i][2], test_result[2] + result[i][3])
                    if (no_passed == 0):
                        print(f"Test {i} failed.")
                        test_results_averaged.append((False, 0, 0, 0))
                    else:
                        print(f"Accuracy: {no_passed / len(test_results) * 100}%. Test {i} average: Time: {test_result[0] / no_passed} seconds. States expanded: {test_result[1] / no_passed}. Path length: {test_result[2] / no_passed}")
                        test_results_averaged.append((True, test_result[0] / no_passed, test_result[1] / no_passed, test_result[2] / no_passed))
                draw_graph(test_results_averaged)

def draw_graph(test_cases: list[TestCase]) -> None:
    # time plot
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    bars = ax.bar(range(len(test_cases)), [test_case[1] for test_case in test_cases])
    ax.bar_label(bars)
    ax.set_xlabel("Test")
    ax.set_ylabel("Time")
    ax.set_title("Time taken by each test")
    plt.show()
    # states expanded plot
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    bars = ax.bar(range(len(test_cases)), [test_case[2] for test_case in test_cases])
    ax.bar_label(bars)
    ax.set_xlabel("Test")
    ax.set_ylabel("States expanded")
    ax.set_title("States expanded by each test")
    plt.show()
    # path length plot
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    bars = ax.bar(range(len(test_cases)), [test_case[3] for test_case in test_cases])
    ax.bar_label(bars)
    ax.set_xlabel("Test")
    ax.set_ylabel("Path length")
    ax.set_title("Path length of each test")
    plt.show()