# In this folder we have matrices of 7x7 cells (tilted to the left for easier calculation afterwards) - a smilie, a tree, or any pattern we like.

conversions = {
    "0": 0,
    "1": 1,
    "2": 5,
    "3": 10,
    "4": 30,
}

size = 7


def flatten_matrix(matrix: str):
    arr = []
    m = [list(row) for row in matrix.strip().split("\n")]

    for week in range(size):
        for day in range(size):
            arr.append(conversions[m[week][day]])

    return arr
