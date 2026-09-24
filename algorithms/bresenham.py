def bresenham_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1

    err = dx - dy
    x, y = x1, y1
    pixels = []

    while True:
        pixels.append((x, y))
        if x == x2 and y == y2:
            return pixels

        e2 = 2 * err
        if e2 > -dy:            
            err -= dy
            x += sx
        if e2 < dx:             
            err += dx
            y += sy


if __name__ == "__main__":
    # Garis positif
    result = bresenham_line(2, 6, 10, 14)
    assert result[0] == (2, 6)
    assert result[-1] == (10, 14)

    # Garis vertikal
    result = bresenham_line(0, 0, 0, 10)
    assert result[0] == (0, 0)
    assert result[-1] == (0, 10)

    # Garis horizontal
    result = bresenham_line(0, 0, 10, 0)
    assert result[0] == (0, 0)
    assert result[-1] == (10, 0)
    
    # Garis slope negatif
    result = bresenham_line(0, 10, 10, 0)
    assert result[0] == (0, 10)
    assert result[-1] == (10, 0)

    # Arah terbalik
    result = bresenham_line(10, 5, 0, 0)
    assert result[0] == (10, 5)
    assert result[-1] == (0, 0)

    # Slope negatif dengan arah x menurun
    result = bresenham_line(10, 0, 0, 5)
    assert result[0] == (10, 0)
    assert result[-1] == (0, 5)

    print("bresenham OK")