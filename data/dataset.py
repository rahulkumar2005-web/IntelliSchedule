
import pandas as pd
from pathlib import Path

# Working days and time slots
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

TIME_SLOTS = [
    "09:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
    "12:00-13:00",
    "14:00-15:00",
    "15:00-16:00"
]

# Faculty information
FACULTY = [
    {"faculty_id": "F01", "name": "Dr. Kumar"},
    {"faculty_id": "F02", "name": "Ms. Priya"},
    {"faculty_id": "F03", "name": "Mr. Arjun"},
    {"faculty_id": "F04", "name": "Dr. Meera"},
    {"faculty_id": "F05", "name": "Mr. Rahul"},
    {"faculty_id": "F06", "name": "Ms. Sneha"},
    {"faculty_id": "F07", "name": "Dr. Ravi"},
    {"faculty_id": "F08", "name": "Mr. Kiran"},
    {"faculty_id": "F09", "name": "Ms. Divya"},
    {"faculty_id": "F10", "name": "Dr. Anil"}
]

# Classroom information
CLASSROOMS = [
    {"room_id": "R101", "capacity": 60},
    {"room_id": "R102", "capacity": 60},
    {"room_id": "R103", "capacity": 50},
    {"room_id": "R104", "capacity": 50},
    {"room_id": "R105", "capacity": 40},
    {"room_id": "R106", "capacity": 40}
]

# Academic courses
COURSES = [
    {"course_id": "C01", "subject": "Python Programming",
     "faculty_id": "F01", "section_id": "A", "lectures_per_week": 2},

    {"course_id": "C02", "subject": "Data Structures",
     "faculty_id": "F02", "section_id": "A", "lectures_per_week": 2},

    {"course_id": "C03", "subject": "Database Management",
     "faculty_id": "F03", "section_id": "A", "lectures_per_week": 2},

    {"course_id": "C04", "subject": "Machine Learning",
     "faculty_id": "F04", "section_id": "A", "lectures_per_week": 2},

    {"course_id": "C05", "subject": "Artificial Intelligence",
     "faculty_id": "F05", "section_id": "B", "lectures_per_week": 2},

    {"course_id": "C06", "subject": "Computer Networks",
     "faculty_id": "F06", "section_id": "B", "lectures_per_week": 2},

    {"course_id": "C07", "subject": "Operating Systems",
     "faculty_id": "F07", "section_id": "B", "lectures_per_week": 2},

    {"course_id": "C08", "subject": "Deep Learning",
     "faculty_id": "F08", "section_id": "B", "lectures_per_week": 2},

    {"course_id": "C09", "subject": "Natural Language Processing",
     "faculty_id": "F09", "section_id": "C", "lectures_per_week": 2},

    {"course_id": "C10", "subject": "Computer Vision",
     "faculty_id": "F10", "section_id": "C", "lectures_per_week": 2},

    {"course_id": "C11", "subject": "Software Engineering",
     "faculty_id": "F01", "section_id": "C", "lectures_per_week": 2},

    {"course_id": "C12", "subject": "Theory of Computation",
     "faculty_id": "F02", "section_id": "C", "lectures_per_week": 2}
]


def create_dataset():

    courses_df = pd.DataFrame(COURSES)
    faculty_df = pd.DataFrame(FACULTY)
    rooms_df = pd.DataFrame(CLASSROOMS)

    # Create all available day and time combinations
    timeslots_df = pd.DataFrame([
        {
            "day": day,
            "time": time,
            "slot_id": f"{day[:3]}_{i+1}"
        }
        for day in DAYS
        for i, time in enumerate(TIME_SLOTS)
    ])

    return courses_df, faculty_df, rooms_df, timeslots_df


def save_dataset():

    courses, faculty, rooms, timeslots = create_dataset()

    output_dir = Path(__file__).parent

    courses.to_csv(output_dir / "courses.csv", index=False)
    faculty.to_csv(output_dir / "faculty.csv", index=False)
    rooms.to_csv(output_dir / "classrooms.csv", index=False)
    timeslots.to_csv(output_dir / "timeslots.csv", index=False)

    print("IntelliSchedule dataset created successfully!")

    print("\nCourses:", len(courses))
    print("Faculty:", len(faculty))
    print("Classrooms:", len(rooms))
    print("Available time slots:", len(timeslots))


if __name__ == "__main__":
    save_dataset()
