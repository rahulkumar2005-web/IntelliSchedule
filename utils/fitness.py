
def evaluate_timetable(timetable):

    hard_violations = 0
    soft_violations = 0

    faculty_schedule = set()
    section_schedule = set()
    room_schedule = set()
    subject_schedule = set()

    section_day_slots = {}

    time_order = {
        "09:00-10:00": 0,
        "10:00-11:00": 1,
        "11:00-12:00": 2,
        "12:00-13:00": 3,
        "14:00-15:00": 4,
        "15:00-16:00": 5
    }

    for lecture in timetable:

        day = lecture["day"]
        time = lecture["time"]
        faculty = lecture["faculty_id"]
        section = lecture["section_id"]
        room = lecture["room_id"]
        subject = lecture["subject"]

        slot = (day, time)

        # Faculty conflict
        faculty_key = (faculty, slot)

        if faculty_key in faculty_schedule:
            hard_violations += 1
        else:
            faculty_schedule.add(faculty_key)

        # Section conflict
        section_key = (section, slot)

        if section_key in section_schedule:
            hard_violations += 1
        else:
            section_schedule.add(section_key)

        # Classroom conflict
        room_key = (room, slot)

        if room_key in room_schedule:
            hard_violations += 1
        else:
            room_schedule.add(room_key)

        # Same subject twice in one day
        subject_key = (section, subject, day)

        if subject_key in subject_schedule:
            soft_violations += 1
        else:
            subject_schedule.add(subject_key)

        # Track section's daily schedule
        section_day_key = (section, day)

        section_day_slots.setdefault(
            section_day_key, []
        )

        if time in time_order:
            section_day_slots[section_day_key].append(
                time_order[time]
            )

    # Penalize unnecessary gaps between classes
    for slots in section_day_slots.values():

        if len(slots) >= 2:

            sorted_slots = sorted(slots)

            gaps = (
                sorted_slots[-1]
                - sorted_slots[0]
                + 1
                - len(sorted_slots)
            )

            soft_violations += gaps

    total_penalty = (
        1000 * hard_violations
        + 10 * soft_violations
    )

    fitness = 1 / (1 + total_penalty)

    return {
        "hard_violations": hard_violations,
        "soft_violations": soft_violations,
        "total_penalty": total_penalty,
        "fitness": fitness
    }


if __name__ == "__main__":

    sample_timetable = [
        {
            "course_id": "C01",
            "subject": "Python Programming",
            "faculty_id": "F01",
            "section_id": "A",
            "room_id": "R101",
            "day": "Monday",
            "time": "09:00-10:00"
        },
        {
            "course_id": "C02",
            "subject": "Data Structures",
            "faculty_id": "F02",
            "section_id": "A",
            "room_id": "R102",
            "day": "Monday",
            "time": "11:00-12:00"
        }
    ]

    print(evaluate_timetable(sample_timetable))
