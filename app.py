
import streamlit as st
import pandas as pd

from data.dataset import create_dataset
from algorithms.genetic_algorithm import run_genetic_algorithm
from algorithms.hybrid_optimizer import run_hybrid_optimizer

st.set_page_config(
    page_title="IntelliSchedule",
    page_icon="📅",
    layout="wide"
)

st.title("IntelliSchedule")
st.subheader("Adaptive Academic Timetable Optimization")
st.caption("A Hybrid Metaheuristic-Reinforcement Learning Framework")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Dataset",
        "Genetic Algorithm",
        "Hybrid GA-RL",
        "Comparison",
        "Timetable"
    ]
)

if "ga_results" not in st.session_state:
    st.session_state.ga_results = None

if "hybrid_results" not in st.session_state:
    st.session_state.hybrid_results = None

st.sidebar.divider()

population_size = st.sidebar.slider(
    "Population Size",
    10,
    100,
    40
)

generations = st.sidebar.slider(
    "Generations",
    10,
    200,
    100
)

courses, faculty, rooms, slots = create_dataset()

if page == "Dashboard":

    st.header("Project Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Courses", len(courses))
    col2.metric("Faculty", len(faculty))
    col3.metric("Classrooms", len(rooms))
    col4.metric("Time Slots", len(slots))

    st.divider()

    st.markdown("### Project Overview")

    st.write(
        "IntelliSchedule automatically generates academic "
        "timetables using Genetic Algorithm and Reinforcement "
        "Learning techniques."
    )

    st.markdown("### Optimization Techniques")

    col1, col2 = st.columns(2)

    with col1:
        st.info("Genetic Algorithm")
        st.write(
            "Uses selection, crossover, mutation and "
            "fitness evaluation to optimize timetables."
        )

    with col2:
        st.success("Hybrid GA-RL")
        st.write(
            "Uses a Q-Learning agent to adapt the mutation "
            "rate based on optimization progress."
        )

elif page == "Dataset":

    st.header("Academic Dataset")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Courses", "Faculty", "Classrooms", "Time Slots"]
    )

    with tab1:
        st.dataframe(courses, use_container_width=True)

    with tab2:
        st.dataframe(faculty, use_container_width=True)

    with tab3:
        st.dataframe(rooms, use_container_width=True)

    with tab4:
        st.dataframe(slots, use_container_width=True)

elif page == "Genetic Algorithm":

    st.header("Genetic Algorithm Optimization")

    st.write(
        "Generate an academic timetable using the Genetic Algorithm."
    )

    if st.button("Run Genetic Algorithm", type="primary"):

        with st.spinner("Generating timetable..."):

            timetable, history, result = run_genetic_algorithm(
                population_size=population_size,
                generations=generations
            )

            st.session_state.ga_results = {
                "timetable": timetable,
                "history": history,
                "result": result
            }

    if st.session_state.ga_results is not None:

        data = st.session_state.ga_results

        result = data["result"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Fitness", f"{result['fitness']:.4f}")
        col2.metric("Hard Violations", result["hard_violations"])
        col3.metric("Soft Violations", result["soft_violations"])

        st.subheader("Fitness Progress")

        st.line_chart(
            pd.DataFrame({
                "Generation": range(1, len(data["history"]) + 1),
                "Fitness": data["history"]
            }).set_index("Generation")
        )

        st.subheader("Generated Timetable")

        st.dataframe(
            data["timetable"],
            use_container_width=True
        )

        st.download_button(
            "Download GA Timetable",
            data["timetable"].to_csv(index=False),
            "genetic_algorithm_timetable.csv",
            "text/csv"
        )

elif page == "Hybrid GA-RL":

    st.header("Hybrid GA-RL Optimization")

    st.write(
        "Generate a timetable using the adaptive "
        "Genetic Algorithm and Q-Learning agent."
    )

    if st.button("Run Hybrid GA-RL", type="primary"):

        with st.spinner("Running hybrid optimization..."):

            timetable, fitness, rewards, q_table, result = (
                run_hybrid_optimizer(
                    population_size=population_size,
                    generations=generations
                )
            )

            st.session_state.hybrid_results = {
                "timetable": timetable,
                "fitness": fitness,
                "rewards": rewards,
                "q_table": q_table,
                "result": result
            }

    if st.session_state.hybrid_results is not None:

        data = st.session_state.hybrid_results

        result = data["result"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Fitness", f"{result['fitness']:.4f}")
        col2.metric("Hard Violations", result["hard_violations"])
        col3.metric("Soft Violations", result["soft_violations"])

        st.subheader("Fitness Progress")

        st.line_chart(
            pd.DataFrame({
                "Generation": range(1, len(data["fitness"]) + 1),
                "Fitness": data["fitness"]
            }).set_index("Generation")
        )

        st.subheader("Reward Progress")

        st.line_chart(
            pd.DataFrame({
                "Generation": range(1, len(data["rewards"]) + 1),
                "Reward": data["rewards"]
            }).set_index("Generation")
        )

        st.subheader("Learned Q-Table")

        st.dataframe(
            pd.DataFrame(
                data["q_table"],
                index=["Improving", "Stagnating"],
                columns=["Low Mutation", "Medium Mutation", "High Mutation"]
            )
        )

        st.subheader("Generated Timetable")

        st.dataframe(
            data["timetable"],
            use_container_width=True
        )

        st.download_button(
            "Download Hybrid Timetable",
            data["timetable"].to_csv(index=False),
            "hybrid_timetable.csv",
            "text/csv"
        )

elif page == "Comparison":

    st.header("Algorithm Comparison")

    ga = st.session_state.ga_results
    hybrid = st.session_state.hybrid_results

    if ga is None or hybrid is None:

        st.warning(
            "Run both Genetic Algorithm and Hybrid GA-RL "
            "before viewing the comparison."
        )

    else:

        comparison = pd.DataFrame({
            "Algorithm": ["Genetic Algorithm", "Hybrid GA-RL"],
            "Fitness": [
                ga["result"]["fitness"],
                hybrid["result"]["fitness"]
            ],
            "Hard Violations": [
                ga["result"]["hard_violations"],
                hybrid["result"]["hard_violations"]
            ],
            "Soft Violations": [
                ga["result"]["soft_violations"],
                hybrid["result"]["soft_violations"]
            ]
        })

        st.dataframe(comparison, use_container_width=True)

        st.subheader("Fitness Comparison")

        chart = pd.DataFrame({
            "Genetic Algorithm": ga["history"],
            "Hybrid GA-RL": hybrid["fitness"]
        })

        st.line_chart(chart)

        st.info(
            "Both algorithms use the same dataset and fitness "
            "evaluation. Compare multiple random seeds for "
            "a more reliable experimental conclusion."
        )

elif page == "Timetable":

    st.header("Generated Academic Timetable")

    ga = st.session_state.ga_results
    hybrid = st.session_state.hybrid_results

    algorithm = st.selectbox(
        "Select Algorithm",
        ["Genetic Algorithm", "Hybrid GA-RL"]
    )

    selected = ga if algorithm == "Genetic Algorithm" else hybrid

    if selected is None:

        st.warning("Run the selected algorithm first.")

    else:

        timetable = selected["timetable"].copy()

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]

        for day in days:

            st.subheader(day)

            daily = timetable[
                timetable["day"].astype(str) == day
            ]

            st.dataframe(
                daily,
                use_container_width=True,
                hide_index=True
            )

        st.download_button(
            "Download Selected Timetable",
            timetable.to_csv(index=False),
            "academic_timetable.csv",
            "text/csv"
        )

st.sidebar.divider()

st.sidebar.caption("IntelliSchedule | Academic Timetable Optimization")
