import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_processing import load_data, get_class_stats



st.title("📊 Real-Time Analytics Dashboard")

# File Upload Section
st.sidebar.header("📁 Data Management")
uploaded_file = st.sidebar.file_uploader("Upload Student Data (CSV/Excel)", type=["csv", "xlsx", "xls"])

if st.sidebar.button("Load Default Sample Data"):
    try:
        df = load_data(open("sample_students.csv", "rb"))
        df.name = "sample_students.csv" # mock name
        st.session_state.df = df
        st.sidebar.success("Loaded sample dataset!")
    except FileNotFoundError:
        st.sidebar.error("Sample dataset not found. Please run data_generator.py first.")

if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.session_state.df = df
        st.sidebar.success(f"Loaded {uploaded_file.name} successfully!")

df = st.session_state.df

if df is not None:
    # --- Top KPIs ---
    stats = get_class_stats(df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", stats.get("total_students", len(df)))
    with col2:
        st.metric("Class Average", f"{stats.get('avg_percentage', 0):.2f}%")
    with col3:
        st.metric("Pass Rate", f"{stats.get('pass_rate', 0):.1f}%")
    with col4:
        st.metric("Top Score", f"{df['Percentage'].max():.2f}%")
        
    st.markdown("---")
    
    # --- Visualizations ---
    st.subheader("📈 Performance Insights")
    
    vcol1, vcol2 = st.columns(2)
    
    with vcol1:
        # Grade Distribution (Plotly Pie)
        if "Grade" in df.columns:
            grade_counts = df["Grade"].value_counts().reset_index()
            grade_counts.columns = ["Grade", "Count"]
            # Sort grades logically
            grade_order = ["A", "B", "C", "D", "E", "F"]
            grade_counts['Grade'] = pd.Categorical(grade_counts['Grade'], categories=grade_order, ordered=True)
            grade_counts = grade_counts.sort_values("Grade")
            
            fig = px.pie(grade_counts, values="Count", names="Grade", title="Grade Distribution", 
                         color="Grade", color_discrete_sequence=px.colors.sequential.Tealgrn)
            st.plotly_chart(fig, use_container_width=True)
            
    with vcol2:
        # Pass/Fail Ratio (Seaborn/Matplotlib)
        if "Status" in df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x="Status", ax=ax, palette="Set2")
            ax.set_title("Pass/Fail Count")
            st.pyplot(fig)
            
    st.markdown("---")
    
    # --- Subject Averages ---
    st.subheader("📚 Subject-wise Analysis")
    subject_cols = [c for c in df.columns if "Score" in c]
    if subject_cols:
        subj_avgs = df[subject_cols].mean().reset_index()
        subj_avgs.columns = ["Subject", "Average Score"]
        fig2 = px.bar(subj_avgs, x="Subject", y="Average Score", title="Class Average per Subject",
                      color="Average Score", color_continuous_scale="Blues")
        st.plotly_chart(fig2, use_container_width=True)
        
    # --- Correlation Heatmap ---
    st.subheader("🔍 Correlation Heatmap")
    st.write("Understand relationships between study hours, attendance, and scores.")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax3)
    st.pyplot(fig3)
    
    # --- Toppers and Low Performers ---
    st.subheader("🏆 Top & Bottom Performers")
    tcol1, tcol2 = st.columns(2)
    with tcol1:
        st.write("**Top 5 Students**")
        st.dataframe(df.nlargest(5, "Percentage")[["Roll No", "Name", "Percentage", "Grade"]], hide_index=True)
    with tcol2:
        st.write("**Needs Attention (Bottom 5)**")
        st.dataframe(df.nsmallest(5, "Percentage")[["Roll No", "Name", "Percentage", "Grade"]], hide_index=True)
        
else:
    st.info("👈 Please upload a dataset or load the sample data from the sidebar to view analytics.")
