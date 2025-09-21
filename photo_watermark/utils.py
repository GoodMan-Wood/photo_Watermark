from typing import Tuple


def parse_hex_color(s: str) -> Tuple[int, int, int]:
    """Parse color like #RRGGBB or common color names. Returns (r,g,b)."""
    s = s.strip()
    if s.startswith('#'):
        s = s.lstrip('#')
        if len(s) == 6:
            r = int(s[0:2], 16)
            g = int(s[2:4], 16)
            b = int(s[4:6], 16)
            return (r, g, b)
        elif len(s) == 3:
            r = int(s[0]*2, 16)
            g = int(s[1]*2, 16)
            b = int(s[2]*2, 16)
            return (r, g, b)
        else:
            raise ValueError('Unsupported hex color format')
    # simple named colors
    names = {
        'white': (255,255,255),
        'black': (0,0,0),
        'red': (255,0,0),
        'green': (0,128,0),
        'blue': (0,0,255),
        'yellow': (255,255,0),
    }
    key = s.lower()
    if key in names:
        return names[key]
    raise ValueError(f'Unknown color: {s}')
