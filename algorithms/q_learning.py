
import random
import numpy as np


class QLearningAgent:

    def __init__(
        self,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=0.2
    ):

        # Learning parameters
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

        # Three optimization actions
        self.actions = [
            0.03,   # Low mutation
            0.08,   # Medium mutation
            0.18    # High mutation
        ]

        # Two possible states:
        # 0 = Search is improving
        # 1 = Search is stagnating

        self.q_table = np.zeros((2, 3))

    def choose_action(self, state):

        # Exploration
        if random.random() < self.epsilon:
            return random.randint(0, 2)

        # Exploitation
        return int(np.argmax(self.q_table[state]))

    def update(self, state, action, reward, next_state):

        current_q = self.q_table[state, action]

        best_next_q = np.max(self.q_table[next_state])

        # Q-Learning update equation
        new_q = current_q + self.alpha * (
            reward
            + self.gamma * best_next_q
            - current_q
        )

        self.q_table[state, action] = new_q

    def get_mutation_rate(self, action):

        return self.actions[action]

    def get_q_table(self):

        return self.q_table


if __name__ == "__main__":

    agent = QLearningAgent()

    print("Q-Learning Agent Created")
    print("Available mutation rates:", agent.actions)

    state = 0

    action = agent.choose_action(state)

    print("Selected action:", action)
    print(
        "Selected mutation rate:",
        agent.get_mutation_rate(action)
    )

    # Simulate a positive reward
    reward = 1.0
    next_state = 0

    agent.update(
        state,
        action,
        reward,
        next_state
    )

    print("\nUpdated Q-Table:")
    print(agent.get_q_table())
