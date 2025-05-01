import streamlit as st
import json
import os

def apply_custom_styles():
    """Apply minimal custom styling to the app"""
    # Using streamlit's native theming capabilities
    st.markdown("""
        <style>
        .role-doctor {
            background-color: #e6f3ff;
            border-left: 5px solid #0066cc;
            padding: 10px;
            margin: 5px 0;
        }
        .role-patient {
            background-color: #f0f0f0;
            border-left: 5px solid #666666;
            padding: 10px;
            margin: 5px 0;
        }
        .role-ai_tool {
            background-color: #f9f9f9;
            border-left: 5px solid #ff9900;
            padding: 10px;
            margin: 5px 0;
        }
        .narrator {
            font-style: italic;
            color: #555;
            margin: 10px 0;
        }
        .decision-button {
            margin: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def save_scenario_feedback(scenario_id, feedback_data):
    """Save user feedback about scenarios for future improvement"""
    feedback_dir = "data/feedback"
    
    # Create directory if it doesn't exist
    if not os.path.exists(feedback_dir):
        try:
            os.makedirs(feedback_dir)
        except:
            st.error("Unable to create feedback directory")
            return False
    
    # Create a unique filename
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{feedback_dir}/scenario_{scenario_id}_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(feedback_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving feedback: {e}")
        return False

def format_character_dialogue(role, text):
    """Format dialogue based on character role"""
    if role.lower() == "narrator":
        return f"<div class='narrator'>{text}</div>"
    
    css_class = f"role-{role.lower().replace(' ', '_')}"
    return f"<div class='{css_class}'><strong>{role}:</strong> {text}</div>"
