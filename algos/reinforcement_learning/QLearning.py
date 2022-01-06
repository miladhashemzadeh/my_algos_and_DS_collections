from games.fucking_elevator.elevator import Elevator
import random
import numpy as np


class Q:

    def __init__(self, elevator=Elevator(floor_size=10, current_position=5), epsilon=0.1, gamma=0.6, alpha=0.1) -> None:
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.elevator = self.init_elevator_for_train(elevator)
        self.table = np.zeros([elevator.get_number_states(), 3])
        # late inits
        self.step = 0
        self.done = False

    def init_elevator_for_train(self, elevator) -> Elevator:
        elevator.add_neighbor(3)
        elevator.add_neighbor(4)
        elevator.add_neighbor(7)
        elevator.add_neighbor(7)
        return elevator

    def solve(self):
        actions = [Elevator.ACTION_UP, Elevator.ACTION_DOWN, Elevator.ACTION_WAIT]
        while not self.done:
            state = self.elevator.get_state()
            uniform = random.uniform(0, 1)
            if uniform < self.epsilon:
                action = random.choice(actions)
            else:
                action = np.argmax(self.table[state])
            reward, done = self.elevator.make_action(action)
            self.done = done
            new_state = self.elevator.get_state()
            new_state_max = np.max(self.table[new_state])
            self.table[state, action] = (1 - self.alpha) * self.table[state, action] + self.alpha * (
                    reward + self.gamma * new_state_max - self.table[state, action])
            self.step += 1

    def smart_reset(self):
        self.step = 0
        self.elevator = self.init_elevator_for_train(elevator=Elevator(floor_size=10, current_position=5))
        # late inits
        self.done = False


if __name__ == "__main__":
    qleraning = Q(alpha=0.1, epsilon=0.4, gamma=0.6)
    counter = 0
    for _ in range(0, 10):
        qleraning.solve()
        counter += qleraning.step
        qleraning.smart_reset()
    qleraning.solve()
    print(" \n after train steps:%d".format(qleraning.step))
    qleraning.smart_reset()
    print(" \n Total steps:%d".format(counter / 10))
