def midpoint_circle(xc, yc, radius):
    """Return unique pixels from Midpoint Circle Algorithm."""
    if radius < 0:
        raise ValueError("Radius tidak boleh negatif.")

    pixels = []
    x, y = 0, radius
    decision = 1 - radius

    while x <= y:
        candidates = (
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x),
        )
        for pixel in candidates:
            if pixel not in pixels:
                pixels.append(pixel)

        x += 1
        if decision < 0:
            decision += 2 * x + 1
        else:
            y -= 1
            decision += 2 * (x - y) + 1

    return pixels
