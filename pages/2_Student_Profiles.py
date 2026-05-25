import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



st.title("🧑‍🎓 Student Profiles & Analysis")

if st.session_state.df is not None:
    df = st.session_state.df
    
    # Search and Filter
    st.sidebar.header("🔍 Search Student")
    search_query = st.sidebar.text_input("Enter Name or Roll No:")
    
    if search_query:
        # Filter dataframe based on search
        filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False) | 
                         df["Roll No"].str.contains(search_query, case=False, na=False)]
    else:
        filtered_df = df
        
    if not filtered_df.empty:
        # Select a student from the filtered list
        student_list = filtered_df["Name"] + " (" + filtered_df["Roll No"] + ")"
        selected_student_str = st.selectbox("Select a Student:", student_list)
        
        # Extract Roll No
        roll_no = selected_student_str.split("(")[1].replace(")", "")
        student = df[df["Roll No"] == roll_no].iloc[0]
        
        st.markdown("---")
        
        # --- Profile Card ---
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image("https://api.dicebear.com/7.x/initials/svg?seed=" + student["Name"], width=150)
        with col2:
            st.header(student["Name"])
            st.subheader(f"Roll No: {student['Roll No']}")
            st.write(f"**Status:** {student['Status']} | **Grade:** {student['Grade']}")
        with col3:
            st.metric("Overall Percentage", f"{student['Percentage']}%", 
                      delta=f"{student['Percentage'] - student['Previous Semester (%)']:.1f}% from last sem")
            
        st.markdown("---")
        
        # --- Detailed Performance ---
        pcol1, pcol2 = st.columns(2)
        
        subject_cols = [c for c in df.columns if "Score" in c]
        student_scores = student[subject_cols].to_dict()
        
        with pcol1:
            st.subheader("Radar Chart: Subject Strengths")
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=list(student_scores.values()),
                theta=[s.replace(" Score", "") for s in student_scores.keys()],
                fill='toself',
                name='Student'
            ))
            
            # Add class average
            class_avgs = df[subject_cols].mean().tolist()
            fig.add_trace(go.Scatterpolar(
                r=class_avgs,
                theta=[s.replace(" Score", "") for s in subject_cols],
                fill='toself',
                name='Class Avg'
            ))
            
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
        with pcol2:
            st.subheader("Attendance vs Marks")
            st.write(f"**Attendance:** {student['Attendance (%)']}%")
            st.write(f"**Study Hours:** {student['Study Hours']} hrs/week")
            
            # Gauge chart for attendance
            fig2 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = student['Attendance (%)'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Attendance"},
                gauge = {'axis': {'range': [None, 100]},
                         'bar': {'color': "darkblue"},
                         'steps': [
                             {'range': [0, 50], 'color': "red"},
                             {'range': [50, 75], 'color': "yellow"},
                             {'range': [75, 100], 'color': "lightgreen"}]}
            ))
            st.plotly_chart(fig2, use_container_width=True)
            
        # --- AI/Smart Analysis Suggestions ---
        st.subheader("💡 Personalized Feedback & Recommendations")
        
        weak_subjects = [s for s, v in student_scores.items() if v < 40]
        strong_subjects = [s for s, v in student_scores.items() if v >= 80]
        
        feedback = []
        if student['Attendance (%)'] < 75:
            feedback.append("⚠️ **Critical:** Attendance is below 75%. Improvement in attendance strongly correlates with better grades.")
        if student['Study Hours'] < 10:
            feedback.append("⚠️ **Warning:** Low study hours reported. Recommend increasing self-study time to at least 15 hours/week.")
            
        if weak_subjects:
            feedback.append(f"📉 **Needs Focus:** Requires extra attention in {', '.join([s.replace(' Score', '') for s in weak_subjects])}. Consider remedial classes.")
        if strong_subjects:
            feedback.append(f"🌟 **Strengths:** Excellent performance in {', '.join([s.replace(' Score', '') for s in strong_subjects])}. Keep it up!")
            
        if not feedback:
            feedback.append("✅ **On Track:** Consistent performance across all metrics. Maintain current study habits.")
            
        for f in feedback:
            st.info(f)
            
    else:
        st.warning("No students found matching your search.")
else:
    st.info("👈 Please load a dataset from the Dashboard first.")
