try:
    from .bee import Bee
except:
    from bee import Bee
from itertools import zip_longest
import uuid


class HoneyComb:
    """
    Honeycomb class to model how the bees are positioned inside it. The bee position could be different from its position
    inside the honeycomb, since the honeycomb is the one that controls its size. The moves of the honeycomb can be iterated
    one by one, or can be requested all at once.
    """

    def __init__(self, bees: [Bee] = [], last_coordinate: int = 0) -> None:
        super().__init__()
        self.__id = str(uuid.uuid4())
        if not self.__validate_attributes__(bees, last_coordinate + 1):
            raise Exception(f'The attributes of the Honeycomb are not correct')
        self.__bees = {}
        self.__banned_bees = []
        self.__last_moves = {}
        for bee in bees:
            self.add_bee(bee)
        self.__size = last_coordinate + 1

    def __str__(self) -> str:
        return super().__str__()

    def __validate_attributes__(self, bees: [Bee] = [], last_coordinate: int = 0):
        return isinstance(bees, list) and False not in [isinstance(bee, Bee) for bee in bees] \
               and isinstance(last_coordinate, int) and last_coordinate > 0

    def __validate_position__(self, position):
        return 0 <= position[0] < self.__size and 0 <= position[1] < self.__size

    def simulate_next(self):
        bee_moves_generators = [bee_gen.make_next_move() for bee_gen in self.__bees.values()]
        for bee_moves in zip_longest(*bee_moves_generators):
            current_moves = {}
            bee_moves = dict(x for x in bee_moves if x is not None)
            for bee_uuid, bee_move in bee_moves.items():
                # First must check whether the bee is banned,
                # otherwise it could be possible the bee fell from the honeycomb and then came back
                if bee_uuid in self.__banned_bees:
                    current_moves[bee_uuid] = None
                # Validate the position of the bee. If is out of range, add it to banned list
                elif not self.__validate_position__(bee_move[0]):
                    self.__banned_bees.append(bee_uuid)
                    current_moves[bee_uuid] = None
                else:
                    current_moves[bee_uuid] = bee_move
            # Merge last moves with current ones to keep state of the bees that didn't move
            self.__last_moves = {**self.__last_moves, **current_moves}
            yield self.__last_moves
        return None

    def simulate_all(self):
        bee_moves_generators = [bee_gen.make_all_moves() for bee_gen in self.__bees.values()]
        all_moves = []
        for bee_moves in zip_longest(*bee_moves_generators):
            current_moves = {}
            bee_moves = (x for x in bee_moves if x is not None)
            for bee_uuid, bee_move in dict(bee_moves).items():
                # First must check whether the bee is banned,
                # otherwise it could be possible the bee fell from the honeycomb and then came back
                if bee_uuid in self.__banned_bees:
                    current_moves[bee_uuid] = None
                # Validate the position of the bee. If is out of range, add it to banned list
                elif not self.__validate_position__(bee_move[0]):
                    self.__banned_bees.append(bee_uuid)
                    current_moves[bee_uuid] = None
                else:
                    current_moves[bee_uuid] = bee_move
            self.__last_moves = {**self.__last_moves, **current_moves}
            all_moves.append(self.__last_moves)
        return all_moves

    def add_bee(self, bee: Bee):
        if not self.__validate_position__(bee.get_position()[0]):
            self.__banned_bees.append(bee.get_id())
            self.__last_moves[bee.get_id()] = None
        else:
            self.__last_moves[bee.get_id()] = bee.get_position()
        self.__bees[bee.get_id()] = bee
        return bee.get_id()

    def delete_bee(self, uuid: str):
        try:
            self.__banned_bees.remove(bee.get_id())
        except Exception:
            pass
        if self.__bees.pop(uuid, None) is None:
            raise Exception(f'The bee with id {uuid} is not in the Honeycomb')

    def get_bees(self):
        return self.__bees

    def get_bee_position(self, uuid):
        if uuid not in self.__bees.keys():
            raise Exception(f'There is no bee with uuid: {uuid} in the honeycomb')
        return None if uuid in self.__banned_bees else self.__bees[uuid].get_position()

    def get_id(self):
        return self.__id

    def get_size(self):
        return self.__size

    def reset(self):
        for bee in self.__bees.values():
            bee.reset()
        self.__banned_bees = []
        self.__last_moves = {}


if __name__ == '__main__':
    with open('./honeycomb_description.txt', 'r') as description:
        print(*[line for line in description.readlines()])
    print('Now please enter the upper-right coordinates of the honeycomb (starting from 0 to coordinate inclusive),\n\r'
          'For example: 5 5.')
    invalid_input = True
    while invalid_input:
        try:
            coordinates_input = str(input()).strip().split(' ')
            x, y = int(coordinates_input[0]), int(coordinates_input[1])
            if x != y:
                raise Exception("The x and y coordinates are not equals")
            invalid_input = False
        except:
            print('Oops it seems you added a wrong input. Please try again')

    print('It\'s time to specify the bees of the honeycomb:\n\r Two lines per bee:\n\r '
          '1st line indicates the initial position and heading where the bee is initially placed \n\r'
          '2nd line indicates a stream of instructions to guide the bee.\r\n'
          'When you are finished with the bees, please enter the input "end"')

    finished = False
    honeycomb = HoneyComb([], x)
    while not finished:
        invalid_input = True
        while invalid_input:
            try:
                position_input = str(input()).strip().split(' ')
                x, y, orientation = int(position_input[0]), int(position_input[1]), position_input[2]
                moves_input = str(input()).strip()
                bee = Bee(x, y, orientation, moves_input)
                honeycomb.add_bee(bee)
                invalid_input = False
            except:
                if position_input[0].lower() == "end":
                    finished = True
                    break
                else:
                    print('Oops it seems you added a wrong input. Please try again')
    honeycomb.simulate_all()
    for bee_uuid, bee in honeycomb.get_bees().items():
        bee_pos = honeycomb.get_bee_position(bee_uuid)
        if bee_pos is None:
            print('This bee has fallen from the honeycomb')
        else:
            print(bee)
