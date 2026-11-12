# IntelliSchedule
### A Hybrid Metaheuristic-Reinforcement Learning Framework for Adaptive Academic Timetable Optimization

## Project Overview

IntelliSchedule is an academic timetable optimization system that combines Genetic Algorithms (GA) with Reinforcement Learning (RL) to generate conflict-free academic timetables.

The system uses a Genetic Algorithm to optimize lecture scheduling and a Q-Learning agent to adapt mutation rates during the optimization process.

## Objectives

- Automatically generate academic timetables.
- Minimize faculty scheduling conflicts.
- Prevent classroom double-booking.
- Prevent section scheduling conflicts.
- Reduce unnecessary gaps between lectures.
- Adapt optimization parameters using Reinforcement Learning.
- Provide an interactive dashboard for timetable generation and analysis.

## Technologies Used

- Python
- Streamlit
- NumPy
- Pandas
- Matplotlib
- Genetic Algorithm
- Q-Learning

## Dataset

The project uses an academic scheduling dataset containing:

| Component | Quantity |
|---|---:|
| Courses | 12 |
| Faculty | 10 |
| Classrooms | 6 |
| Available time slots | 30 |
| Total lecture sessions | 24 |

The dataset is maintained in the project's data module.

## Methodology

### 1. Genetic Algorithm

The Genetic Algorithm uses:
- Population initialization
- Fitness evaluation
- Selection
- Crossover
- Mutation
- Iterative optimization

### 2. Reinforcement Learning

A Q-Learning agent selects among three mutation rates:

- Low: 0.03
- Medium: 0.08
- High: 0.18

The agent updates its Q-table based on optimization rewards.

### 3. Hybrid GA-RL

The hybrid framework combines Genetic Algorithm optimization with adaptive mutation selection using Q-Learning.

## Fitness Evaluation

The timetable is evaluated using hard and soft constraint violations.

The fitness function is:

Fitness = 1 / (1 + Total Penalty)

The current penalty function assigns:
- 1000 points per hard constraint violation.
- 10 points per soft constraint violation.

## Project Structure

```text
IntelliSchedule/
│
├── algorithms/
├── data/
├── utils/
├── app.py
├── requirements.txt
├── .gitignore
├── genetic_algorithm_timetable.csv
├── hybrid_timetable.csv
└── hybrid_training_history.csv
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/rahulkumar2005-web/IntelliSchedule.git
```

### 2. Navigate to the project

```bash
cd IntelliSchedule
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Results

The current test runs produced:

| Metric | Genetic Algorithm | Hybrid GA-RL |
|---|---:|---:|
| Hard Violations | 0 | 0 |
| Soft Violations | 0 | 0 |
| Fitness | 1.0 | 1.0 |

These are observed results from the current test runs, not averages across multiple experiments.

## Future Enhancements

- Faculty availability constraints.
- Classroom capacity validation.
- Multiple-seed performance evaluation.
- Improved adaptive reward strategies.
- Enhanced timetable visualization.
- Additional optimization techniques.

## Author

Rahul Kumar

## License

To be determined.
