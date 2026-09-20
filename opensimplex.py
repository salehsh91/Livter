"""
Pure-Python 2D OpenSimplex noise (drop-in for the parts of the `opensimplex`
package that Livter uses).

Why this file exists
--------------------
The PyPI package `opensimplex` (>= 0.4) has a hard dependency on numpy, which is
slow and fragile to cross-compile for Android with python-for-android. This
module needs nothing except the standard library, so it builds and runs
anywhere. Put it next to main.py; because the app folder is first on sys.path,
`from opensimplex import OpenSimplex` will pick this file automatically, and
`opensimplex` must NOT be listed in buildozer.spec requirements any more.

Algorithm: Kurt Spencer's OpenSimplex noise (2014, public domain), 2D only.

Supported API
-------------
    from opensimplex import OpenSimplex
    gen = OpenSimplex(seed=123)
    value = gen.noise2(x, y)          # float in [-1, 1]

Also available: OpenSimplex.noise2d(x, y) (alias, old 0.3 name) and the
module-level helpers seed(n), noise2(x, y) that the 0.4 package offers.
"""

from math import floor

__all__ = ["OpenSimplex", "seed", "random_seed", "noise2"]

_STRETCH_2D = -0.211324865405187   # (1 / sqrt(2 + 1) - 1) / 2
_SQUISH_2D = 0.366025403784439     # (sqrt(2 + 1) - 1) / 2
_NORM_2D = 47.0

_GRADIENTS_2D = (
    5, 2, 2, 5,
    -5, 2, -2, 5,
    5, -2, 2, -5,
    -5, -2, -2, -5,
)

_LCG_MUL = 6364136223846793005
_LCG_ADD = 1442695040888963407


def _wrap64(value):
    """Wrap an int to signed 64 bit, like a Java/C `long`."""
    return (value + 0x8000000000000000) % 0x10000000000000000 - 0x8000000000000000


def _build_perm(seed_value):
    perm = [0] * 256
    source = list(range(256))
    s = _wrap64(int(seed_value))
    s = _wrap64(s * _LCG_MUL + _LCG_ADD)
    s = _wrap64(s * _LCG_MUL + _LCG_ADD)
    s = _wrap64(s * _LCG_MUL + _LCG_ADD)
    for i in range(255, -1, -1):
        s = _wrap64(s * _LCG_MUL + _LCG_ADD)
        r = (s + 31) % (i + 1)          # Python % is already non-negative
        perm[i] = source[r]
        source[r] = source[i]
    return perm


class OpenSimplex:
    """2D OpenSimplex noise generator with a deterministic seed."""

    def __init__(self, seed=0):
        self._perm = _build_perm(seed)

    def noise2(self, x, y):
        perm = self._perm
        grad = _GRADIENTS_2D
        squish = _SQUISH_2D

        # Stretch input onto the grid and find the super-cell origin.
        stretch_offset = (x + y) * _STRETCH_2D
        xs = x + stretch_offset
        ys = y + stretch_offset
        xsb = floor(xs)
        ysb = floor(ys)

        # Squish back to get the real-space coordinates of the origin.
        squish_offset = (xsb + ysb) * squish
        dx0 = x - (xsb + squish_offset)
        dy0 = y - (ysb + squish_offset)

        # Position inside the super-cell (stretched space).
        xins = xs - xsb
        yins = ys - ysb
        in_sum = xins + yins

        value = 0.0

        # Contribution from (1, 0)
        dx1 = dx0 - 1 - squish
        dy1 = dy0 - squish
        attn = 2 - dx1 * dx1 - dy1 * dy1
        if attn > 0:
            attn *= attn
            i = perm[(perm[(xsb + 1) & 255] + ysb) & 255] & 14
            value += attn * attn * (grad[i] * dx1 + grad[i + 1] * dy1)

        # Contribution from (0, 1)
        dx2 = dx0 - squish
        dy2 = dy0 - 1 - squish
        attn = 2 - dx2 * dx2 - dy2 * dy2
        if attn > 0:
            attn *= attn
            i = perm[(perm[xsb & 255] + ysb + 1) & 255] & 14
            value += attn * attn * (grad[i] * dx2 + grad[i + 1] * dy2)

        if in_sum <= 1:
            # Inside the triangle (2-simplex) at (0, 0)
            zins = 1 - in_sum
            if zins > xins or zins > yins:
                # (0, 0) is one of the two closest triangle vertices
                if xins > yins:
                    xsv_ext = xsb + 1
                    ysv_ext = ysb - 1
                    dx_ext = dx0 - 1
                    dy_ext = dy0 + 1
                else:
                    xsv_ext = xsb - 1
                    ysv_ext = ysb + 1
                    dx_ext = dx0 + 1
                    dy_ext = dy0 - 1
            else:
                # (1, 0) and (0, 1) are the two closest vertices
                xsv_ext = xsb + 1
                ysv_ext = ysb + 1
                dx_ext = dx0 - 1 - 2 * squish
                dy_ext = dy0 - 1 - 2 * squish
        else:
            # Inside the triangle (2-simplex) at (1, 1)
            zins = 2 - in_sum
            if zins < xins or zins < yins:
                # (1, 1) is one of the two closest triangle vertices
                if xins > yins:
                    xsv_ext = xsb + 2
                    ysv_ext = ysb
                    dx_ext = dx0 - 2 - 2 * squish
                    dy_ext = dy0 - 2 * squish
                else:
                    xsv_ext = xsb
                    ysv_ext = ysb + 2
                    dx_ext = dx0 - 2 * squish
                    dy_ext = dy0 - 2 - 2 * squish
            else:
                # (1, 0) and (0, 1) are the two closest vertices
                dx_ext = dx0
                dy_ext = dy0
                xsv_ext = xsb
                ysv_ext = ysb
            xsb += 1
            ysb += 1
            dx0 = dx0 - 1 - 2 * squish
            dy0 = dy0 - 1 - 2 * squish

        # Contribution from (0, 0) or (1, 1)
        attn = 2 - dx0 * dx0 - dy0 * dy0
        if attn > 0:
            attn *= attn
            i = perm[(perm[xsb & 255] + ysb) & 255] & 14
            value += attn * attn * (grad[i] * dx0 + grad[i + 1] * dy0)

        # Contribution from the extra vertex
        attn = 2 - dx_ext * dx_ext - dy_ext * dy_ext
        if attn > 0:
            attn *= attn
            i = perm[(perm[xsv_ext & 255] + ysv_ext) & 255] & 14
            value += attn * attn * (grad[i] * dx_ext + grad[i + 1] * dy_ext)

        return value / _NORM_2D

    # Old (0.3) method name, kept so either spelling works.
    def noise2d(self, x=0.0, y=0.0):
        return self.noise2(x, y)


# ---------------------------------------------------------------------------
# Module-level helpers (same names as the 0.4 package)
# ---------------------------------------------------------------------------
_default = OpenSimplex(0)


def seed(seed=0):
    global _default
    _default = OpenSimplex(seed)


def random_seed():
    import time
    seed(int(time.time() * 1000))


def noise2(x, y):
    return _default.noise2(x, y)
