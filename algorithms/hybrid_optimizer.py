
import random
import numpy as np
import pandas as pd

from data.dataset import create_dataset
from algorithms.genetic_algorithm import (
    create_lectures,
    generate_chromosome,
    calculate_fitness,
    selection,
    crossover,
    mutation,
    build_timetable
)

from algorithms.q_learning import QLearningAgent


def run_hybrid_optimizer(
    population_size=40,
    generations=100,
    seed=42
):

    random.seed(seed)
    np.random.seed(seed)

    # Load academic dataset
    courses_df, faculty_df, rooms_df, timeslots_df = (
        create_dataset()
    )

    lectures = create_lectures(courses_df)
    rooms = rooms_df["room_id"].tolist()

    # Initialize RL agent
    agent = QLearningAgent()

    # Generate initial population
    population = [
        generate_chromosome(lectures, rooms)
        for _ in range(population_size)
    ]

    best_chromosome = None
    best_fitness = -1

    fitness_history = []
    reward_history = []
    action_history = []

    previous_best = 0
    stagnation = 0

    print("Starting Hybrid GA-RL Optimization")
    print("Total lecture sessions:", len(lectures))

    for generation in range(generations):

        # Evaluate population
        population.sort(
            key=lambda chromosome: calculate_fitness(
                lectures, chromosome
            )["fitness"],
            reverse=True
        )

        current_best = population[0]

        current_fitness = calculate_fitness(
            lectures, current_best
        )["fitness"]

        # Update global best
        if current_fitness > best_fitness:

            best_fitness = current_fitness

            best_chromosome = [
                gene.copy() for gene in current_best
            ]

        # Detect search progress
        if best_fitness > previous_best:
            state = 0
            stagnation = 0
        else:
            state = 1
            stagnation += 1

        previous_best = best_fitness

        # RL selects mutation rate
        action = agent.choose_action(state)

        adaptive_mutation_rate = agent.get_mutation_rate(
            action
        )

        # Preserve best solutions
        new_population = [
            [gene.copy() for gene in chromosome]
            for chromosome in population[:2]
        ]

        while len(new_population) < population_size:

            parent1 = selection(population, lectures)
            parent2 = selection(population, lectures)

            child = crossover(
                parent1,
                parent2,
                lectures,
                rooms
            )

            child = mutation(
                child,
                lectures,
                rooms,
                adaptive_mutation_rate
            )

            new_population.append(child)

        population = new_population

        # Evaluate the updated population
        population.sort(
            key=lambda chromosome: calculate_fitness(
                lectures, chromosome
            )["fitness"],
            reverse=True
        )

        new_best = population[0]

        new_fitness = calculate_fitness(
            lectures, new_best
        )["fitness"]

        # Calculate reward
        improvement = new_fitness - current_fitness

        if improvement > 1e-9:
         reward = 1.0
         next_state = 0
        elif improvement < -1e-9:
         reward = -0.5
         next_state = 1
        else:
         reward = -0.05
         next_state = 1

        # Update Q-table
        agent.update(
            state,
            action,
            reward,
            next_state
        )

        # Update best solution
        if new_fitness > best_fitness:

            best_fitness = new_fitness

            best_chromosome = [
                gene.copy() for gene in new_best
            ]

        fitness_history.append(best_fitness)
        reward_history.append(reward)
        action_history.append(action)

        # Gradually reduce exploration
        agent.epsilon = max(
            0.02,
            agent.epsilon * 0.995
        )

        if (generation + 1) % 10 == 0:

            print(
                f"Generation {generation + 1} | "
                f"Fitness: {best_fitness:.6f} | "
                f"Mutation: {adaptive_mutation_rate} | "
                f"Reward: {reward}"
            )

    # Generate final timetable
    final_timetable = build_timetable(
        lectures,
        best_chromosome
    )

    timetable_df = pd.DataFrame(final_timetable)

    result = calculate_fitness(
        lectures,
        best_chromosome
    )

    print("\nHYBRID GA-RL RESULTS")
    print("--------------------")
    print("Hard Violations:", result["hard_violations"])
    print("Soft Violations:", result["soft_violations"])
    print("Fitness Score:", result["fitness"])

    print("\nLearned Q-Table:")
    print(agent.get_q_table())

    print("\nAction Selection Counts:")
    print({
        "Low Mutation": action_history.count(0),
        "Medium Mutation": action_history.count(1),
        "High Mutation": action_history.count(2)
    })

    # Save outputs
    timetable_df.to_csv(
        "hybrid_timetable.csv",
        index=False
    )

    pd.DataFrame({
        "generation": range(1, generations + 1),
        "best_fitness": fitness_history,
        "reward": reward_history,
        "selected_action": action_history
    }).to_csv(
        "hybrid_training_history.csv",
        index=False
    )

    print("\nHybrid timetable saved successfully!")

    return (
        timetable_df,
        fitness_history,
        reward_history,
        agent.get_q_table(),
        result
    )


if __name__ == "__main__":

    run_hybrid_optimizer()
