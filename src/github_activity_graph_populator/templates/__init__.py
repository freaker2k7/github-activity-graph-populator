# In this folder we have matrices of 7 rows by at least 1 cells (tilted to the left for easier calculation afterwards) - a smilie, a tree, or any pattern we like.

conversions = {
    "0": 0,
    "1": 1,
    "2": 5,
    "3": 15,
    "4": 50,
}

rows = 7


def flatten_matrix(matrix: str):
    arr = []
    mtx = [list(row) for row in matrix.strip().splitlines()]
    cols = len(mtx[0] if mtx else [])

    if len(mtx) != rows:
        raise ValueError(f"Matrix must have {rows} rows")

    for week in range(rows):
        if len(mtx[week]) != cols:
            raise ValueError("All rows must have same number of columns")

    for day in range(cols):
        for week in range(rows):
            arr.append(conversions[mtx[week][day]])

    return arr
