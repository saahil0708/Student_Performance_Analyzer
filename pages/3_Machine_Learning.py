import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from ml_models.trainer import train_models, predict_risk



st.title("🤖 Predictive Analytics & ML")

if st.session_state.df is not None:
    df = st.session_state.df
    
    # Check if models are already trained in session state
    if "ml_data" not in st.session_state:
        st.session_state.ml_data = None
        
    st.write("Train Machine Learning models to predict student success (Pass/Fail) based on historical data, attendance, and study hours.")
    
    if st.button("Train Models Now", type="primary"):
        with st.spinner("Training Logistic Regression, Decision Tree, Random Forest, and KNN..."):
            ml_data, msg = train_models(df)
            if ml_data:
                st.session_state.ml_data = ml_data
                st.success("Models trained successfully!")
            else:
                st.error(f"Failed to train models: {msg}")
                
    if st.session_state.ml_data is not None:
        ml_data = st.session_state.ml_data
        
        st.markdown("---")
        
        # --- Model Accuracy Comparison ---
        st.subheader("📊 Model Accuracy Comparison")
        acc_df = pd.DataFrame(list(ml_data["results"].items()), columns=["Model", "Accuracy"])
        acc_df["Accuracy"] = acc_df["Accuracy"] * 100
        
        fig = px.bar(acc_df, x="Accuracy", y="Model", orientation='h', 
                     title="Model Accuracy (%)", color="Accuracy", color_continuous_scale="Viridis")
        fig.update_layout(xaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
        
        # --- Feature Importance (Random Forest) ---
        st.subheader("🔍 Feature Importance")
        st.write("Which factors contribute most to a student passing?")
        
        rf_model = ml_data["models"].get("Random Forest")
        if rf_model:
            importance = rf_model.feature_importances_
            feat_df = pd.DataFrame({"Feature": ml_data["features"], "Importance": importance})
            feat_df = feat_df.sort_values("Importance", ascending=True)
            
            fig2 = px.bar(feat_df, x="Importance", y="Feature", orientation='h',
                          title="Feature Importance (Random Forest)", color="Importance", color_continuous_scale="Reds")
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("---")
        
        # --- Risk Detection Simulator ---
        st.subheader("⚠️ Risk Detection Simulator")
        st.write("Tweak parameters to see if the student is at risk of failing.")
        
        scol1, scol2, scol3 = st.columns(3)
        with scol1:
            sim_study = st.slider("Study Hours/week", 0, 40, 15)
            sim_att = st.slider("Attendance (%)", 0, 100, 75)
        with scol2:
            sim_prev = st.slider("Previous Semester (%)", 0, 100, 60)
            sim_math = st.slider("Math Score", 0, 100, 50)
        with scol3:
            sim_sci = st.slider("Science Score", 0, 100, 50)
            sim_eng = st.slider("English Score", 0, 100, 50)
            sim_hist = st.slider("History Score", 0, 100, 50)
            
        sim_data = pd.DataFrame([{
            "Study Hours": sim_study, "Attendance (%)": sim_att, "Previous Semester (%)": sim_prev,
            "Math Score": sim_math, "Science Score": sim_sci, "English Score": sim_eng, "History Score": sim_hist
        }])
        
        selected_model = st.selectbox("Select Model for Prediction", list(ml_data["models"].keys()))
        
        at_risk = predict_risk(sim_data, ml_data["models"], ml_data["scaler"], ml_data["features"], selected_model)
        
        if at_risk:
            st.error("🚨 **High Risk of Failing!** Based on these parameters, the model predicts the student will FAIL.")
        else:
            st.success("✅ **Safe!** Based on these parameters, the model predicts the student will PASS.")
            
        # --- Student Clustering (Unsupervised Learning) ---
        st.markdown("---")
        st.subheader("🎯 Student Behavioral Segments (K-Means Clustering)")
        st.write("Using unsupervised learning to group students based on their Study Hours and Attendance.")
        
        from ml_models.trainer import run_clustering
        clustered_df = run_clustering(df)
        
        if clustered_df is not None:
            fig3 = px.scatter(clustered_df, x="Study Hours", y="Attendance (%)", color="Student Segment",
                              hover_data=["Name", "Percentage"],
                              title="Student Segments by Engagement",
                              color_discrete_sequence=["#ef553b", "#00cc96", "#636efa"])
            st.plotly_chart(fig3, use_container_width=True)
            
            st.info("💡 **Insight:** You can use these segments to create targeted improvement programs. For example, mandatory study halls for the 'Low Engagement' segment.")
            
else:
    st.info("👈 Please load a dataset from the Dashboard first to access ML features.")
