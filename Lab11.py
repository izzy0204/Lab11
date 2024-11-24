import os
import matplotlib.pyplot as plt


class CourseData:
    def __init__(self):
        self.students = {}  # {student_id: student_name}
        self.assignments = {}  # {assignment_id: (name, points)}
        self.submissions = []  # list of (student_id, assignment_id, percentage)
        self.load_data()

    def load_data(self):
        with open('data/students.txt', 'r') as f:
            for line in f:
                line = line.strip()
                # Extract first 3 characters as ID, rest is name
                student_id = line[:3]
                student_name = line[3:]
                self.students[student_id] = student_name

        with open('data/assignments.txt', 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                name = lines[i].strip()
                assignment_id = lines[i + 1].strip()
                points = int(lines[i + 2].strip())
                self.assignments[assignment_id] = (name, points)
                i += 3

        # load submissions from all files in submissions directory
        submissions_dir = 'data/submissions'
        for filename in os.listdir(submissions_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(submissions_dir, filename), 'r') as f:
                    line = f.read().strip()
                    student_id, assignment_id, percentage = line.split('|')
                    self.submissions.append((student_id, assignment_id, float(percentage)))

    def get_student_id(self, student_name):
        """Helper method to find student ID from name"""
        for student_id, name in self.students.items():
            if name.lower() == student_name.lower():
                return student_id
        return None

    def get_assignment_id(self, assignment_name):
        """Helper method to find assignment ID from name"""
        for assignment_id, (name, _) in self.assignments.items():
            if name.lower() == assignment_name.lower():
                return assignment_id
        return None

    def get_student_grade(self, student_name):
        student_id = self.get_student_id(student_name)
        if student_id is None:
            return None

        total_earned = 0
        total_possible = 0

        # calculate total points earned and possible
        for submission in self.submissions:
            if submission[0] == student_id:  # if this submission is from our student
                assignment_points = self.assignments[submission[1]][1]  # get points possible for this assignment
                percentage = submission[2]
                points_earned = (percentage / 100) * assignment_points
                total_earned += points_earned
                total_possible += assignment_points

        if total_possible == 0:
            return 0

        return round((total_earned / total_possible) * 100)

    def get_assignment_stats(self, assignment_name):
        assignment_id = self.get_assignment_id(assignment_name)
        if assignment_id is None:
            return None

        scores = []
        for submission in self.submissions:
            if submission[1] == assignment_id:  # if this submission is for our assignment
                scores.append(submission[2])  # add the percentage score

        if not scores:
            return None

        return {
            'min': min(scores),
            'avg': int(sum(scores) / len(scores)),  # Added round() here
            'max': max(scores)
        }

        scores = []
        for submission in self.submissions:
            if submission[1] == assignment_id:  # if this submission is for our assignment
                scores.append(submission[2])  # add the percentage score

        if not scores:
            return None

        return {
            'min': min(scores),
            'avg': sum(scores) / len(scores),
            'max': max(scores)
        }

    def show_assignment_graph(self, assignment_name):
        assignment_id = self.get_assignment_id(assignment_name)
        if assignment_id is None:
            return False

        scores = []
        for submission in self.submissions:
            if submission[1] == assignment_id:  # if this submission is for our assignment
                scores.append(submission[2])  # add the percentage score

        if not scores:
            return False

        plt.hist(scores, bins=[0, 25, 50, 75, 100])
        plt.title(f'Score Distribution for {assignment_name}')
        plt.xlabel('Score (%)')
        plt.ylabel('Number of Students')
        plt.show()
        return True


def main():
    course = CourseData()

    print("\n1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print("\nEnter your selection:", end=" ")

    choice = input()

    if choice == "1":
        student_name = input("What is the student's name: ")
        grade = course.get_student_grade(student_name)
        if grade is None:
            print("Student not found")
        else:
            print(f"{grade}%")

    elif choice == "2":
        assignment_name = input("What is the assignment name: ")
        stats = course.get_assignment_stats(assignment_name)
        if stats is None:
            print("Assignment not found")
        else:
            print(f"Min: {stats['min']:.0f}%")
            print(f"Avg: {stats['avg']:.0f}%")
            print(f"Max: {stats['max']:.0f}%")

    elif choice == "3":
        assignment_name = input("What is the assignment name: ")
        if not course.show_assignment_graph(assignment_name):
            print("Assignment not found")


if __name__ == "__main__":
    main()