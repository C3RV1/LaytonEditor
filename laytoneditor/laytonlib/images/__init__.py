"""
Contains general functions used for images.
"""

def rgb_to_bgr555(r, g, b):
    b = b >> 3
    g = g >> 3
    r = r >> 3
    sum = (b << 10) + (g << 5) + r
    return sum

def bgr555_to_rgb(bgr555_sum):
    b = (bgr555_sum & (2**5-1)) << 3
    g = ((bgr555_sum >> 5) & (2**5-1)) << 3
    r = ((bgr555_sum >> 10) & (2**5-1)) << 3
    return (b, g, r)

def np_copy(dest, src, loc):
    x, y = loc
    h, w, d = src.shape
    h2, w2, d = dest[y:y+h, x:x+w].shape
    dest[y:y + h, x:x + w] = src[:h2, :w2]
    return dest