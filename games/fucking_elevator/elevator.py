import numpy as np


class Elevator:
    ACTION_DOWN = 0
    ACTION_UP = 1
    ACTION_WAIT = 2
    WRONG_DIRECTION = -1
    RIGHT_DIRECTION = 1
    OUT_OF_LIMIT_DIRECTION = 3
    GAME_ENDED = 100

    def __init__(self, floor_size=5, current_position=5, is_waiting=True):
        self._is_waiting = is_waiting
        self._current_position = current_position
        self._floor_size = floor_size+1
        # lateinit vars
        self._floor_to_getout = np.zeros(floor_size)

    def add_neighbor(self, desired_position):
        self._floor_to_getout[desired_position] += 1

    # this method is for Qlearning uses
    def get_number_states(self):
        return self._floor_size*self._floor_to_getout.size*2

    # this method is for Qlearning uses
    def get_state(self):
        state = self._current_position*self._floor_to_getout.size*2
        try:
            state += self._find_nearest(self._floor_to_getout, self._current_position) * 2
        except TypeError as e:
            if self._floor_to_getout.size <= self._current_position or self._current_position >= 0:
                state += self.OUT_OF_LIMIT_DIRECTION * 2
            else:
                state += self.RIGHT_DIRECTION * 2
        state += 1 if self._is_waiting else 0
        return state

    def make_action(self, action_number) -> tuple:
        if action_number == self.ACTION_DOWN:
            self._is_waiting = False
            direction_verify = self._make_distance(self._floor_to_getout, self._current_position, -1)
            if self._current_position <= 0 and direction_verify == self.OUT_OF_LIMIT_DIRECTION:
                return -20, False
            elif self._current_position > self._floor_size:
                return -20, False
            elif direction_verify == self.OUT_OF_LIMIT_DIRECTION:
                return -20, False
            elif direction_verify == self.GAME_ENDED:
                self._current_position += 1
                return 20, True
            elif direction_verify == self.RIGHT_DIRECTION:
                self._current_position += 1
                return 1, False
            elif direction_verify == self.WRONG_DIRECTION:
                self._current_position += 1
                return -1, False
        elif action_number == self.ACTION_UP:
            self._is_waiting = False
            direction_verify = self._make_distance(self._floor_to_getout, self._current_position, 1)
            if self._current_position <= 0:
                return -20, False
            elif self._current_position > self._floor_size or direction_verify == self.OUT_OF_LIMIT_DIRECTION:
                return -20, False
            elif direction_verify == self.OUT_OF_LIMIT_DIRECTION:
                return -20, False
            elif direction_verify == self.GAME_ENDED:
                self._current_position -= 1
                return 20, True
            elif direction_verify == self.RIGHT_DIRECTION:
                self._current_position -= 1
                return 1, False
            elif direction_verify == self.WRONG_DIRECTION:
                self._current_position -= 1
                return -1, False
        else:
            self._is_waiting = True
            try:
                if self._floor_to_getout[self._current_position] != 0:
                    self._floor_to_getout[self._current_position] = 0
                    if self._floor_to_getout.max() == 0:
                        return 20, True
                    else:
                        return 10, False
                else:
                    return -20, False
            except IndexError:
                return -20, False

    def _make_distance(self, floor_to_getout, current_position, direction) -> int:
        maxFloor = floor_to_getout.max()
        nearest = self._find_nearest(floor_to_getout, current_position)
        rdirection = current_position - direction
        ldirection = current_position + direction
        try:
            decision = abs(nearest - rdirection) < abs(nearest - ldirection)
        except TypeError as e:
            return self.OUT_OF_LIMIT_DIRECTION
        if maxFloor == 0:
            return self.GAME_ENDED
        else:
            return self.RIGHT_DIRECTION if decision else self.WRONG_DIRECTION

    def _find_nearest(self, floor_to_getout, current_position):
        minimum = 0
        getout_size = floor_to_getout.size
        max_pointer = current_position
        min_pointer = current_position
        while max_pointer <= getout_size-1 or min_pointer <= minimum:
            if floor_to_getout[max_pointer] != 0:
                return max_pointer
            max_pointer += 1 if max_pointer < getout_size - 1 else 0
            if floor_to_getout[min_pointer] != 0:
                return min_pointer
            min_pointer -= 1 if min_pointer > 0 else 0


if __name__ == "__main__":
    el = Elevator(floor_size=10, current_position=5)
    el.add_neighbor(3)
    el.add_neighbor(3)
    el.add_neighbor(6)
    el.add_neighbor(7)
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_WAIT))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_UP))
    print(el.make_action(el.ACTION_WAIT))
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_DOWN))
    print(el.make_action(el.ACTION_WAIT))

