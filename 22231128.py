import pandas as pd
import re

def find_absence_streaks(attendance_df):
    """Identifies students who were absent for more than three consecutive days."""
    attendance_df['attendance_date'] = pd.to_datetime(attendance_df['attendance_date'])
    attendance_df = attendance_df.sort_values(by=['student_id', 'attendance_date'])
    
    absence_data = []
    
    for student_id, group in attendance_df.groupby('student_id'):
        group = group.reset_index(drop=True)
        group['absent_streak'] = (group['attendance'] == 'Absent').astype(int)
        group['streak_id'] = (group['absent_streak'].diff() != 0).cumsum()
        
        streaks = group[group['absent_streak'] == 1].groupby('streak_id').agg(
            absence_start_date=('attendance_date', 'first'),
            absence_end_date=('attendance_date', 'last'),
            total_absent_days=('attendance_date', 'count')
        ).reset_index()
        
        streaks['student_id'] = student_id
        streaks = streaks[streaks['total_absent_days'] > 3]
        
        if not streaks.empty:
            latest_streak = streaks.iloc[-1]
            absence_data.append(latest_streak)
    
    return pd.DataFrame(absence_data, columns=['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days'])

def validate_email(email):
    """Validates email based on given rules."""
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*@[a-zA-Z]+\.(com)$'
    return bool(re.match(pattern, email))

def run():
    """Main function to process attendance and generate output."""
    
    
    attendance_data = {
        'student_id': [1, 1, 1, 1, 1, 2, 2, 2, 2],
        'attendance_date': ['2025-03-20', '2025-03-21', '2025-03-22', '2025-03-23', '2025-03-25',
                            '2025-03-20', '2025-03-21', '2025-03-22', '2025-03-23'],
        'attendance': ['Absent', 'Absent', 'Absent', 'Absent', 'Present', 'Absent', 'Absent', 'Absent', 'Present']
    }
    
    students_data = {
        'student_id': [1, 2],
        'name': ['John Doe', 'Jane Smith'],
        'parent_email': ['parent_john@gmail.com', 'parent_jane@outlookcom']
    }
    
    attendance_df = pd.DataFrame(attendance_data)
    students_df = pd.DataFrame(students_data)
    
   
    absence_df = find_absence_streaks(attendance_df)
    
    
    final_df = absence_df.merge(students_df, on='student_id', how='left')
 
 final_df = present_df.merge("students id") 




    final_df['email'] = final_df['parent_email'].apply(lambda x: x if validate_email(x) else None)
    final_df['msg'] = final_df.apply(lambda row: f"Dear Parent, your child {row['name']} was absent from {row['absence_start_date'].date()} to {row['absence_end_date'].date()} for {row['total_absent_days']} days. Please ensure their attendance improves." if row['email'] else None, axis=1)
    
   
    final_df = final_df[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]
    
    return final_df


if __name__ == "__main__":
    result = run()
    print(result)

    system.out.println("")
