import math
def dda_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return [(x1, y1)]

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = float(x1), float(y1)
    pixels = []
    for _ in range(steps + 1):
        pixels.append((math.floor(x + 0.5), math.floor(y + 0.5)))
        x += x_inc
        y += y_inc
    return pixels


if __name__ == "__main__":
    p = dda_line(2, 6, 10, 14)
    assert p[0] == (2, 6) and p[-1] == (10, 14) and len(p) == 9
    assert dda_line(0, 0, 0, 10) == [(0, y) for y in range(11)]     # vertikal
    assert dda_line(0, 0, 10, 0) == [(x, 0) for x in range(11)]     # horizontal
    assert dda_line(10, 5, 0, 0)[::-1] == dda_line(0, 0, 10, 5)     # arah balik
    assert dda_line(0, 0, 10, 5)[-1] == (10, 5)                     # slope positif
    assert dda_line(0, 10, 10, 0)[-1] == (10, 0)                    # slope negatif
    assert dda_line(3, 3, 3, 3) == [(3, 3)]                         # satu titik
    print("dda OK")
