import pytest

from app.dtos import Point
from app.services.processors import to_array_coord

# [room_size, cart_point, array_point]
point_transform_data_provider = [
    (3, Point(-1, 1), Point(0, 0)),
    (3, Point(0, 1), Point(1, 0)),
    (3, Point(1, 1), Point(2, 0)),
    (3, Point(0, -1), Point(1, 2)),
    (3, Point(0, 0), Point(1, 1)),
    (3, Point(0, 1), Point(1, 0)),
    (3, Point(-1, -1), Point(0, 2)),
    (3, Point(0, -1), Point(1, 2)),
    (3, Point(1, -1), Point(2, 2)),
    (20, Point(0, 0), Point(10, 10)),
    (20, Point(0, -10), Point(10, 20)),
    (20, Point(-10, 10), Point(0, 0)),
    (20, Point(-10, 0), Point(0, 10)),
    (20, Point(-10, -10), Point(0, 20)),
    (20, Point(10, -10), Point(20, 20)),
    (20, Point(10, 0), Point(20, 10)),
    (20, Point(10, 10), Point(20, 0)),
    (20, Point(0, 10), Point(10, 0)),
    (6, Point(-1, 2), Point(2, 1)),
    (6, Point(0, 0), Point(3, 3))
]


@pytest.mark.parametrize("room_size, origin, array_point", point_transform_data_provider)
def test_shift_point(room_size, origin, array_point):
    actual = to_array_coord(room_size, origin)

    assert actual == array_point, f"Cartesian point {origin} should be translated to array coordinate {array_point}"