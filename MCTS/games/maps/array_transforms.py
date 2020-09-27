from . import HexMap
from data_types import HexagonGrid


def map_from_bin_array(array2d, triangle: bool, content0, content1) -> HexMap:
    board = []
    for n in array2d:
        row = []
        for m in n:
            row.append(content0 if m == 0 else content1)
        board.append(row)
    return HexMap(HexagonGrid(board, triangle=triangle))
