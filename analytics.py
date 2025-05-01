"""
Analytics module for the Healthcare Storytelling Platform.
Provides visualizations and insights from the database.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import db_manager
import datetime
from sqlalchemy import func, desc, and_
from sqlalchemy.orm import aliased

def run_analytics():
    """Run the analytics dashboard"""
    st.title("Healthcare Storytelling Analytics")
    st.markdown("### Insights from simulation sessions")
    
    # Get database session
    db_session = db_manager.get_session()
    
    # Display analytics sections
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Session Statistics")
            display_session_stats(db_session)
        
        with col2:
            st.subheader("User Engagement")
            display_user_engagement(db_session)
    
    st.markdown("---")
    
    # Bias analytics
    st.subheader("Bias Identification Analytics")
    display_bias_analytics(db_session)
    
    st.markdown("---")
    
    # Decision analytics
    st.subheader("Decision Path Analytics")
    display_decision_analytics(db_session)
    
    # Close the database session
    db_session.close()

def display_session_stats(db_session):
    """Display general session statistics"""
    from database import Session, User, DialogueEntry, Decision, BiasIdentification
    
    # Count total sessions
    total_sessions = db_session.query(func.count(Session.id)).scalar()
    
    # Count completed sessions
    completed_sessions = db_session.query(func.count(Session.id)).filter(Session.completed == True).scalar()
    
    # Count sessions with GPT enabled
    gpt_sessions = db_session.query(func.count(Session.id)).filter(Session.gpt_enabled == True).scalar()
    
    # Get average session duration for completed sessions
    duration_query = db_session.query(
        func.avg(func.julianday(Session.end_time) - func.julianday(Session.start_time)) * 24 * 60
    ).filter(Session.completed == True)
    
    avg_duration = duration_query.scalar() or 0
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Sessions", total_sessions)
        st.metric("Completed Sessions", completed_sessions)
    
    with col2:
        st.metric("GPT-Enhanced Sessions", gpt_sessions)
        st.metric("Avg. Duration (minutes)", f"{avg_duration:.1f}")
    
    # Display recent sessions
    st.markdown("#### Recent Sessions")
    
    recent_sessions = db_session.query(
        Session.id, 
        Session.scenario_id,
        Session.selected_role,
        Session.start_time,
        Session.completed,
        User.username
    ).join(User).order_by(desc(Session.start_time)).limit(5).all()
    
    if recent_sessions:
        df = pd.DataFrame(recent_sessions, 
                         columns=["ID", "Scenario", "Role", "Start Time", "Completed", "User"])
        df["Start Time"] = df["Start Time"].dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(df)
    else:
        st.info("No sessions recorded yet.")

def display_user_engagement(db_session):
    """Display user engagement metrics"""
    from database import Session, User, DialogueEntry, Decision, BiasIdentification
    
    # Get user session counts
    user_counts = db_session.query(
        User.username,
        func.count(Session.id).label("session_count")
    ).join(Session).group_by(User.id).order_by(desc("session_count")).limit(10).all()
    
    if user_counts:
        # Convert to DataFrame
        df = pd.DataFrame(user_counts, columns=["Username", "Sessions"])
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot.bar(x="Username", y="Sessions", ax=ax)
        plt.title("User Engagement")
        plt.xlabel("User")
        plt.ylabel("Number of Sessions")
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.info("No user data available yet.")
    
    # Role distribution
    role_counts = db_session.query(
        Session.selected_role,
        func.count(Session.id).label("count")
    ).group_by(Session.selected_role).all()
    
    if role_counts:
        st.markdown("#### Role Selection Distribution")
        
        # Convert to DataFrame
        df = pd.DataFrame(role_counts, columns=["Role", "Count"])
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(df["Count"], labels=df["Role"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
        
        st.pyplot(fig)
    else:
        st.info("No role selection data available yet.")

def display_bias_analytics(db_session):
    """Display analytics about bias identification"""
    from database import BiasIdentification, Session
    
    # Get bias type distribution
    bias_counts = db_session.query(
        BiasIdentification.bias_type,
        func.count(BiasIdentification.id).label("count")
    ).group_by(BiasIdentification.bias_type).order_by(desc("count")).all()
    
    if bias_counts:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Bias Type Distribution")
            
            # Convert to DataFrame
            df = pd.DataFrame(bias_counts, columns=["Bias Type", "Count"])
            
            # Create horizontal bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            df.plot.barh(x="Bias Type", y="Count", ax=ax)
            plt.title("Identified Bias Types")
            plt.xlabel("Count")
            plt.tight_layout()
            
            st.pyplot(fig)
        
        with col2:
            st.markdown("#### User vs AI Bias Identification")
            
            # Compare user vs AI identified biases
            source_counts = db_session.query(
                BiasIdentification.is_ai_generated,
                func.count(BiasIdentification.id).label("count")
            ).group_by(BiasIdentification.is_ai_generated).all()
            
            if source_counts:
                # Convert to DataFrame
                df = pd.DataFrame(source_counts, columns=["AI Generated", "Count"])
                df["Source"] = df["AI Generated"].apply(lambda x: "AI Identified" if x else "User Identified")
                
                # Create pie chart
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(df["Count"], labels=df["Source"], autopct="%1.1f%%", startangle=90)
                ax.axis("equal")
                
                st.pyplot(fig)
            else:
                st.info("No bias source data available.")
    else:
        st.info("No bias identification data available yet.")
    
    # Show recent bias identifications
    st.markdown("#### Recent Bias Identifications")
    recent_biases = db_session.query(
        BiasIdentification.bias_type,
        BiasIdentification.description,
        BiasIdentification.timestamp,
        BiasIdentification.is_ai_generated,
        Session.scenario_id
    ).join(Session).order_by(desc(BiasIdentification.timestamp)).limit(5).all()
    
    if recent_biases:
        df = pd.DataFrame(recent_biases, 
                        columns=["Bias Type", "Description", "Timestamp", "AI Generated", "Scenario"])
        df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        df["Source"] = df["AI Generated"].apply(lambda x: "AI" if x else "User")
        df = df.drop(columns=["AI Generated"])
        st.dataframe(df)
    else:
        st.info("No bias identifications recorded yet.")

def display_decision_analytics(db_session):
    """Display analytics about user decisions"""
    from database import Decision, Session
    
    # Analyze most common decisions
    decision_counts = db_session.query(
        Decision.decision_text,
        func.count(Decision.id).label("count")
    ).group_by(Decision.decision_text).order_by(desc("count")).limit(10).all()
    
    if decision_counts:
        st.markdown("#### Most Common Decisions")
        
        # Convert to DataFrame
        df = pd.DataFrame(decision_counts, columns=["Decision", "Count"])
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot.barh(x="Decision", y="Count", ax=ax)
        plt.title("Top Decisions Made")
        plt.xlabel("Count")
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.info("No decision data available yet.")
    
    # Analyze decision patterns
    st.markdown("#### Decision Patterns by Role")
    
    role = st.selectbox("Select Role", ["Doctor", "Patient", "AI Tool", "Observer"])
    
    role_decisions = db_session.query(
        Decision.decision_text,
        func.count(Decision.id).label("count")
    ).join(Session).filter(Session.selected_role == role).group_by(Decision.decision_text).order_by(desc("count")).limit(5).all()
    
    if role_decisions:
        # Convert to DataFrame
        df = pd.DataFrame(role_decisions, columns=["Decision", "Count"])
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 4))
        df.plot.barh(x="Decision", y="Count", ax=ax)
        plt.title(f"Top Decisions Made by {role}s")
        plt.xlabel("Count")
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.info(f"No decision data available for {role} role.")

if __name__ == "__main__":
    run_analytics()