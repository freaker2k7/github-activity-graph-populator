# In this folder we have matrices of 7x7 cells (tilted to the left for easier calculation afterwards) - a smilie, a tree, or any pattern we like.

def flatten_matrix(matrix):
    return [commit for week in matrix for commit in week]
