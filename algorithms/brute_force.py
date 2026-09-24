import math
def brute_force_line(x1, y1, x2, y2):
    if x1 == x2:
        step = 1 if y2 >= y1 else -1
        return [(x1, y) for y in range(y1, y2 + step, step)]

    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    if x1 <= x2:
        xs = range(x1, x2 + 1)
    else:
        xs = range(x1, x2 - 1, -1)
    return [(x, math.floor(m * x + c + 0.5)) for x in xs]


if __name__ == "__main__":
    assert brute_force_line(2, 6, 10, 14)[0] == (2, 6)
    assert brute_force_line(2, 6, 10, 14)[-1] == (10, 14)
    assert len(brute_force_line(2, 6, 10, 14)) == 9
    assert brute_force_line(0, 0, 0, 10) == [(0, y) for y in range(11)]   # vertikal
    assert brute_force_line(0, 0, 10, 0) == [(x, 0) for x in range(11)]   # horizontal
    assert brute_force_line(10, 5, 0, 0)[::-1] == brute_force_line(0, 0, 10, 5)
    assert brute_force_line(0, 0, 10, 5)[-1] == (10, 5)                   # slope positif
    assert brute_force_line(0, 10, 10, 0)[-1] == (10, 0)                  # slope negatif
    print("brute_force OK")
