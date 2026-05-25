import pandas as pd
import numpy as np

def generate_data(num_students=200):
    np.random.seed(42)
    
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Riya", "Aanya", "Diya", "Myra", "Ananya", "Kavya", "Sana", "Isha", "Neha", "Rahul", "Rohan", "Vikram", "Neha", "Priya"]
    last_names = ["Sharma", "Patel", "Singh", "Kumar", "Das", "Bose", "Gupta", "Verma", "Jain", "Mehta", "Chawla", "Desai", "Joshi", "Bhat", "Rao", "Nair", "Pillai", "Reddy", "Choudhury", "Bansal"]
    
    names = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(num_students)]
    roll_nos = [f"R{str(i).zfill(3)}" for i in range(1, num_students + 1)]
    
    # Generate features
    study_hours = np.random.normal(loc=15, scale=5, size=num_students)
    study_hours = np.clip(study_hours, 5, 30) # 5 to 30 hours per week
    
    attendance = np.random.normal(loc=80, scale=10, size=num_students)
    attendance = np.clip(attendance, 50, 100) # 50% to 100%
    
    prev_performance = np.random.normal(loc=75, scale=12, size=num_students)
    prev_performance = np.clip(prev_performance, 40, 100)
    
    # Generate marks based on study hours, attendance and prev performance with some noise
    base_score = (study_hours / 30) * 30 + (attendance / 100) * 30 + (prev_performance / 100) * 40
    
    math_score = base_score + np.random.normal(loc=0, scale=10, size=num_students)
    math_score = np.clip(math_score, 0, 100)
    
    science_score = base_score + np.random.normal(loc=0, scale=8, size=num_students)
    science_score = np.clip(science_score, 0, 100)
    
    english_score = base_score + np.random.normal(loc=0, scale=7, size=num_students)
    english_score = np.clip(english_score, 0, 100)
    
    history_score = base_score + np.random.normal(loc=0, scale=9, size=num_students)
    history_score = np.clip(history_score, 0, 100)
    
    # Calculate percentage
    percentage = (math_score + science_score + english_score + history_score) / 4
    
    # Pass/Fail (Target for ML)
    # Pass if percentage >= 40 and all subjects >= 35
    pass_fail = []
    for m, s, e, h, p in zip(math_score, science_score, english_score, history_score, percentage):
        if p >= 40 and m >= 35 and s >= 35 and e >= 35 and h >= 35:
            pass_fail.append("Pass")
        else:
            pass_fail.append("Fail")
            
    # Calculate Grade
    grades = []
    for p in percentage:
        if p >= 90: grades.append("A")
        elif p >= 80: grades.append("B")
        elif p >= 70: grades.append("C")
        elif p >= 60: grades.append("D")
        elif p >= 40: grades.append("E")
        else: grades.append("F")
        
    df = pd.DataFrame({
        "Roll No": roll_nos,
        "Name": names,
        "Study Hours": np.round(study_hours, 1),
        "Attendance (%)": np.round(attendance, 1),
        "Previous Semester (%)": np.round(prev_performance, 1),
        "Math Score": np.round(math_score, 0),
        "Science Score": np.round(science_score, 0),
        "English Score": np.round(english_score, 0),
        "History Score": np.round(history_score, 0),
        "Percentage": np.round(percentage, 2),
        "Grade": grades,
        "Status": pass_fail
    })
    
    df.to_csv("sample_students.csv", index=False)
    print("Generated sample_students.csv successfully.")

if __name__ == "__main__":
    generate_data()
