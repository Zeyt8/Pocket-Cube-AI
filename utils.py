from pocket_cube.cube import Cube, Move

FrontierItem = tuple[int, str, Cube]
DiscoveredDict = dict[str, tuple[str, Move, int]]

def get_neighbors(cube: Cube) -> list[tuple[Cube, Move]]:
    """
    Returns the neighbors of the given cube.

    Args:
        cube (Cube): The cube to get the neighbors of.

    Returns:
        list[tuple[Cube, Move]]: The neighbors of the given cube.
    """
    return [(cube.move(move), move) for move in Move]

def get_path(cube_hash: str, discovered: DiscoveredDict) -> list[Move]:
    """
    Returns the path to the given cube.

    Args:
        cube_hash (str): The hash of the cube to get the path to.
        discovered (DiscoveredDict): The dictionary of discovered cubes.

    Returns:
        list[Move]: The path to the given cube.
    """
    path: list[Move] = []
    currentNode = discovered[cube_hash]
    while currentNode[0] is not None:
        path.append(currentNode[1])
        currentNode = discovered[currentNode[0]]
    path.reverse()
    return path

def met_in_the_middle(cubes1: DiscoveredDict, cubes2: DiscoveredDict) -> str:
    """
    Returns the hash of the cube that was discovered by both frontiers.

    Args:
        cubes1 (DiscoveredDict): The dictionary of discovered cubes of the first frontier.
        cubes2 (DiscoveredDict): The dictionary of discovered cubes of the second frontier.

    Returns:
        str: The hash of the cube that was discovered by both frontiers.
    """
    for key in cubes1:
        if key in cubes2:
            return key
    return None