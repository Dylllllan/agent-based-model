def distanceBetweenPoints(point1: tuple, point2: tuple) -> float:
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def getPositionInDirection(position: tuple, direction: tuple) -> tuple:
    return position[0] + direction[0], position[1] + direction[1]
