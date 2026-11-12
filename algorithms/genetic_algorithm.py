
import random
import pandas as pd

from data.dataset import DAYS, TIME_SLOTS, create_dataset
from utils.fitness import evaluate_timetable

# STEP 1: Convert courses into individual lecture sessions
def create_lectures(courses_df):

    lectures = []

    for _, course in courses_df.iterrows():

        for number in range(course["lectures_per_week"]):

            lectures.append({
                "course_id": course["course_id"],
                "subject": course["subject"],
                "faculty_id": course["faculty_id"],
                "section_id": course["section_id"],
                "lecture_no": number + 1
            })

    return lectures

# STEP 2: Check whether an assignment creates hard conflicts
def has_conflict(lecture, assignment, scheduled):

    for other in scheduled:

        same_slot = (
            assignment["day"] == other["day"]
            and assignment["time"] == other["time"]
        )

        if not same_slot:
            continue

        if lecture["faculty_id"] == other["faculty_id"]:
            return True

        if lecture["section_id"] == other["section_id"]:
            return True

        if assignment["room_id"] == other["room_id"]:
            return True

    return False

# STEP 3: Repair a timetable to remove hard conflicts
def repair_timetable(lectures, assignments, rooms):

    repaired = [None] * len(lectures)

    order = list(range(len(lectures)))
    random.shuffle(order)

    for index in order:

        lecture = lectures[index]
        preferred = assignments[index].copy()

        candidates = [preferred]

        alternatives = [
            {
                "day": day,
                "time": time,
                "room_id": room
            }
            for day in DAYS
            for time in TIME_SLOTS
            for room in rooms
        ]

        random.shuffle(alternatives)

        candidates.extend(alternatives)

        selected = None

        for candidate in candidates:

            if not has_conflict(
                lecture,
                candidate,
                [
                    {
                        **lectures[j],
                        **repaired[j]
                    }
                    for j in range(len(lectures))
                    if repaired[j] is not None
                ]
            ):

                selected = candidate.copy()
                break

        if selected is None:
            raise RuntimeError(
                "Unable to repair timetable. "
                "Check available resources."
            )

        repaired[index] = selected

    return repaired

# STEP 4: Generate a random timetable
def generate_chromosome(lectures, rooms):

    assignments = []

    for _ in lectures:

        assignments.append({
            "day": random.choice(DAYS),
            "time": random.choice(TIME_SLOTS),
            "room_id": random.choice(rooms)
        })

    return repair_timetable(lectures, assignments, rooms)

# STEP 5: Convert chromosome into a timetable
def build_timetable(lectures, chromosome):

    return [
        {**lecture, **assignment}
        for lecture, assignment in zip(lectures, chromosome)
    ]

# STEP 6: Calculate fitness
def calculate_fitness(lectures, chromosome):

    timetable = build_timetable(lectures, chromosome)

    return evaluate_timetable(timetable)

# STEP 7: Tournament selection
def selection(population, lectures):

    candidates = random.sample(
        population,
        min(3, len(population))
    )

    return max(
        candidates,
        key=lambda chromosome: calculate_fitness(
            lectures, chromosome
        )["fitness"]
    )

# STEP 8: Crossover
def crossover(parent1, parent2, lectures, rooms):

    point = random.randint(1, len(parent1) - 1)

    child = (
        parent1[:point] +
        parent2[point:]
    )

    return repair_timetable(lectures, child, rooms)

# STEP 9: Mutation
def mutation(chromosome, lectures, rooms, mutation_rate=0.08):

    mutated = [gene.copy() for gene in chromosome]

    for gene in mutated:

        if random.random() < mutation_rate:

            gene["day"] = random.choice(DAYS)
            gene["time"] = random.choice(TIME_SLOTS)
            gene["room_id"] = random.choice(rooms)

    return repair_timetable(lectures, mutated, rooms)

# STEP 10: Main Genetic Algorithm
def run_genetic_algorithm(
    population_size=40,
    generations=100,
    mutation_rate=0.08,
    seed=42
):

    random.seed(seed)

    courses_df, faculty_df, rooms_df, timeslots_df = (
        create_dataset()
    )

    lectures = create_lectures(courses_df)

    rooms = rooms_df["room_id"].tolist()

    print("Total lecture sessions:", len(lectures))

    # Create initial population
    population = [
        generate_chromosome(lectures, rooms)
        for _ in range(population_size)
    ]

    best_chromosome = None
    best_fitness = -1

    fitness_history = []

    # Evolution process
    for generation in range(generations):

        population.sort(
            key=lambda chromosome: calculate_fitness(
                lectures, chromosome
            )["fitness"],
            reverse=True
        )

        current_best = population[0]

        current_result = calculate_fitness(
            lectures, current_best
        )

        if current_result["fitness"] > best_fitness:

            best_fitness = current_result["fitness"]

            best_chromosome = [
                gene.copy() for gene in current_best
            ]

        fitness_history.append(best_fitness)

        # Elitism: preserve the best solutions
        new_population = [
            [gene.copy() for gene in chromosome]
            for chromosome in population[:2]
        ]

        # Generate new offspring
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
                mutation_rate
            )

            new_population.append(child)

        population = new_population

        if (generation + 1) % 10 == 0:

            print(
                f"Generation {generation + 1}: "
                f"Best Fitness = {best_fitness:.6f}"
            )

    # Final result
    final_timetable = build_timetable(
        lectures,
        best_chromosome
    )

    result = evaluate_timetable(final_timetable)

    timetable_df = pd.DataFrame(final_timetable)

    timetable_df["day"] = pd.Categorical(
        timetable_df["day"],
        categories=DAYS,
        ordered=True
    )

    timetable_df["time"] = pd.Categorical(
        timetable_df["time"],
        categories=TIME_SLOTS,
        ordered=True
    )

    timetable_df = timetable_df.sort_values(
        ["day", "time", "section_id"]
    )

    print("\nGENETIC ALGORITHM RESULTS")
    print("-------------------------")
    print("Hard Violations:", result["hard_violations"])
    print("Soft Violations:", result["soft_violations"])
    print("Fitness Score:", result["fitness"])

    return timetable_df, fitness_history, result

if __name__ == "__main__":

    timetable, history, result = run_genetic_algorithm()

    print("\nGENERATED TIMETABLE")
    print(timetable.to_string(index=False))

    timetable.to_csv(
        "genetic_algorithm_timetable.csv",
        index=False
    )

    print("\nTimetable saved successfully!")