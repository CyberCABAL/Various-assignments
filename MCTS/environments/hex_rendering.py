from networkx import Graph


def create_render(state):  # Should be done once.
    g = Graph()

    pos = {}
    edges = []
    index = 0

    target = state
    dim = len(target)
    y_start = dim
    x_start = 0
    for i in range(dim):
        row_dim = len(target[i])
        for j in range(row_dim):
            g.add_node(index)

            # Add Edges
            if j > 0 and i + 1 < dim:   # Next column, previous row.
                edges.append((index, index + row_dim - 1))
            if j + 1 < row_dim:     # Next in row.
                edges.append((index, index + 1))
            if i + 1 < dim and j < len(target[i + 1]):  # Next column, next row.
                edges.append((index, index + row_dim))

            pos[index] = (j + x_start, y_start - j)
            index += 1
        x_start -= 1
        y_start -= 1

    g.add_edges_from(edges)

    return g, pos
