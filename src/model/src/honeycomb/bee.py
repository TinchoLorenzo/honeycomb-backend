from collections import deque
import uuid

class Bee:
    """
    Class bee to manage the position and moves inside the Honeycomb. This contains the logic to move forward and rotate
    inside a honeycomb by a bee.
    """

    __valid_moves = ['L', 'R', 'M']
    __valid_orientations = ['N', 'E', 'S', 'W']
    __move_forward = {
        'N': [0, 1],
        'W': [-1, 0],
        'S': [0, -1],
        'E': [1, 0],
    }

    def __init__(self, x: int = 0, y: int = 0, orientation: str = 'N', moves: str = '') -> None:
        super().__init__()
        self.__orientation = deque(Bee.__valid_orientations)
        self.__uuid = str(uuid.uuid4())
        self.__moves_index = 0
        if self.__validate_position__(x, y, orientation, moves):
            self.__location = [x, y]
            # Rotate the orientation deque until the first element is the given orientation
            while self.__orientation[0] != orientation:
                self.__orientation.rotate(1)
            self.__moves = moves
            self.__init_values = {
                'location': [x, y],
                'orientation': orientation,
                'moves': moves
            }
        else:
            raise Exception("The values provided are not correct")

    def __str__(self) -> str:
        return f'{self.__location[0]} {self.__location[1]} {self.__orientation[0]}'

    def get_id(self):
        return self.__uuid

    def get_position(self):
        return self.__location, self.__orientation[0]

    def get_moves(self):
        return self.__moves

    def set_location(self, x: int = 0, y: int = 0):
        if self.__validate_position__(x = x, y = y):
            self.__location = [x, y]
        else:
            raise Exception("The coordinates provided are not correct. x and y must be > 0")

    def set_orientation(self, orientation: str = 'N'):
        if self.__validate_position__(orientation = orientation):
            # Rotate the orientation deque until the first element is the given orientation
            while self.__orientation[0] != orientation:
                self.__orientation.rotate(1)
        else:
            raise Exception(f"The orientation given is not correct. The valid orientations are {Bee.__valid_orientations}")

    def set_moves(self, moves: str = ''):
        if self.__validate_position__(moves = moves):
            self.__moves = moves
            self.__moves_index = 0
        else:
            raise Exception("The coordinates provided are not correct. x and y must be > 0")

    def reset(self):
        self.set_location(*self.__init_values['location'])
        self.set_moves(self.__init_values['moves'])
        self.set_orientation(self.__init_values['orientation'])

    def __validate_position__(self, x: int = 0, y: int = 0, orientation: str = 'N', moves: str = '') -> bool:
        return isinstance(x, int) and isinstance(y, int) and isinstance(orientation, str) and isinstance(moves, str) \
               and orientation in Bee.__valid_orientations and not False in ([char in Bee.__valid_moves for char in moves])

    def make_next_move(self) -> []:
        while self.__moves_index < len(self.__moves):
            move = self.__moves[self.__moves_index]
            if move == 'M':
                self.__location = [x + y for x, y in zip(self.__location, Bee.__move_forward[self.__orientation[0]])]
            elif move == 'L':
                self.__orientation.rotate(1)
            else:
                self.__orientation.rotate(-1)
            self.__moves_index += 1
            yield (self.__uuid, (self.__location, self.__orientation[0]))
        return (self.__uuid, (self.__location, self.__orientation[0]))

    def make_all_moves(self) -> []:
        moves = []
        while self.__moves_index < len(self.__moves):
            move = self.__moves[self.__moves_index]
            if move == 'M':
                self.__location = [x + y for x, y in zip(self.__location, Bee.__move_forward[self.__orientation[0]])]
            elif move == 'L':
                self.__orientation.rotate(1)
            else:
                self.__orientation.rotate(-1)
            self.__moves_index += 1
            moves.append((self.__uuid, (self.__location, self.__orientation[0])))
        return moves
