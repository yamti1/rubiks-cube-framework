import numpy as np

CUBE_FACE_COUNT = 6
TOP_FACE = "Top"
FRONT_FACE = "Front"
LEFT_FACE = "Left"
RIGHT_FACE = "Right"
BACK_FACE = "Back"
BOTTOM_FACE = "Bottom"

def _get_face(i, n):
    return np.array([[i for _ in range(n)] for _ in range(n)], np.int32)

class RubiksCube:
    def __init__(self, n):
        self.top, self.front, self.left, self.right, self.back, self.bottom = [
            _get_face(i, n) for i in range(CUBE_FACE_COUNT)
        ]

        self.FACE_NAME_MAP = {
            TOP_FACE: self.top,
            FRONT_FACE: self.front,
            LEFT_FACE: self.left,
            RIGHT_FACE: self.right,
            BACK_FACE: self.back,
            BOTTOM_FACE: self.bottom,
        }

    def u(self, i=0):
        np.rot90(self.top, 1)
        self.front[i], self.left[i], self.back[i], self.right[i] = \
            self.right[i].copy(), self.front[i].copy(), self.left[i].copy(), self.back[i].copy()

    def __str__(self):
        return "\n".join(
            ["{}:\n{}".format(name, face) for name, face in self.FACE_NAME_MAP.items()]
        )

if __name__ == '__main__':
    cube = RubiksCube(3)
    cube.u()
    print(cube)
