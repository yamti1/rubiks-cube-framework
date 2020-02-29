from dataclasses import dataclass
import numpy as np

CUBE_FACE_COUNT = 6
CUBE_AXIS_COUNT = 3
TOP = "top"
FRONT = "front"
LEFT = "left"
RIGHT = "right"
BACK = "back"
BOTTOM = "bottom"

UD_AXIS = 0  # Up-Down axis
LR_AXIS = 1  # Left-Right axis
FB_AXIS = 2  # Front-Back axis


class RubiksCube:
    """
                TOP: [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]
    LEFT:[      FRONT: [    RIGHT: [    BACK: [
    [2, 2, 2],  [1, 1, 1],  [3, 3, 3],  [4, 4, 4],
    [2, 2, 2],  [1, 1, 1],  [3, 3, 3],  [4, 4, 4],
    [2, 2, 2]]  [1, 1, 1]]  [3, 3, 3]]  [4, 4, 4]]
                BOTTOM: [
                [5, 5, 5],
                [5, 5, 5],
                [5, 5, 5]]
    """

    @dataclass
    class Rotation:
        face: str
        axis: int

    MAJOR_AXIS = 0
    MINOR_AXIS = 1

    def __init__(self, n):
        self.n = n
        self.top, self.front, self.left, self.right, self.back, self.bottom = [
            self._get_face(i, n) for i in range(CUBE_FACE_COUNT)
        ]

        self.axis_to_faces_map = {
            UD_AXIS: [TOP, BOTTOM],
            FB_AXIS: [FRONT, BACK],
            LR_AXIS: [LEFT, RIGHT]
        }

        self.rotations = {
            UD_AXIS: [
                self.Rotation(self.front, self.MAJOR_AXIS),
                self.Rotation(self.left, self.MAJOR_AXIS),
                self.Rotation(self.back, self.MAJOR_AXIS),
                self.Rotation(self.right, self.MAJOR_AXIS),
            ],
            FB_AXIS: [
                self.Rotation(self.top, self.MAJOR_AXIS),
                self.Rotation(self.right, self.MINOR_AXIS),
                self.Rotation(self.bottom, self.MAJOR_AXIS),
                self.Rotation(self.left, self.MINOR_AXIS),
            ],
            LR_AXIS: [
                self.Rotation(self.top, self.MINOR_AXIS),
                self.Rotation(self.back, self.MINOR_AXIS),
                self.Rotation(self.bottom, self.MINOR_AXIS),
                self.Rotation(self.front, self.MINOR_AXIS),
            ]
        }

    @property
    def faces(self):
        return {
            TOP: self.top,
            FRONT: self.front,
            LEFT: self.left,
            RIGHT: self.right,
            BACK: self.back,
            BOTTOM: self.bottom,
        }

    @staticmethod
    def _get_face(i, n):
        return np.array([[i for _ in range(n)] for _ in range(n)], np.int32)

    @staticmethod
    def __get_face_slice(rotation, layer_index):
        face_slice = [slice(None)] * len(rotation.face.shape)
        face_slice[rotation.axis] = layer_index
        return tuple(face_slice)

    def __get_face_by_layer(self, axis, layer_index):
        if layer_index in (0, -self.n):
            return self.axis_to_faces_map[axis][0]

        if layer_index in (-1, self.n-1):
            return self.axis_to_faces_map[axis][-1]

        raise ValueError(f"Layer at index {layer_index} has no outer face")

    def __rotate_face(self, rotation_axis, layer_index, rotate_by):
        try:
            face_name = self.__get_face_by_layer(rotation_axis, layer_index)
        except ValueError:
            return
        face = self.faces[face_name]

        # Numpy rotates counter-clockwise by default,
        # while the Rubik's Cube standard is clockwise.
        # That's why `rotate_by` is negated.
        setattr(self, face_name, np.rot90(face, -rotate_by))

    def _rotate_layer(self, rotation_axis, layer_index, rotate_by):
        self.__rotate_face(rotation_axis, layer_index, rotate_by)

        rotations = self.rotations[rotation_axis]

        layer = []
        for rotation in rotations:
            face_slice = self.__get_face_slice(rotation, layer_index)
            layer.append(rotation.face[face_slice].copy())

        rotated_layer = np.roll(layer, rotate_by, axis=0)

        for rotation, new_layer_slice in zip(rotations, rotated_layer):
            face_slice = self.__get_face_slice(rotation, layer_index)
            rotation.face[face_slice] = new_layer_slice

    def rotate_ud(self, layer_index=0, rotate_by=1):
        self._rotate_layer(UD_AXIS, layer_index, rotate_by)

    def rotate_fb(self, layer_index=0, rotate_by=1):
        self._rotate_layer(FB_AXIS, layer_index, rotate_by)

    def rotate_lr(self, layer_index=0, rotate_by=1):
        self._rotate_layer(LR_AXIS, layer_index, rotate_by)

    def __str__(self):
        return "\n".join(
            [f"{name}:\n{face}" for name, face in self.faces.items()]
        )

if __name__ == '__main__':
    cube = RubiksCube(3)
    cube.left[0,0] = 10
    cube.left[2,2] = 11
    cube.rotate_lr()
    print(cube)
