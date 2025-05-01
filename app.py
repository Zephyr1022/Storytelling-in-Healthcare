import streamlit as st
import json
import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from simulation import run_simulation, get_role_icon
from scenarios import load_scenarios, get_scenario_description
from visualization import visualize_decision_tree
from utils import apply_custom_styles
from characters import get_character_profiles
from data.speculative_scenarios import add_speculative_scenarios_to_data
from data.clinical_decision_support_scenarios import add_cdss_scenarios_to_data

# Page configuration
st.set_page_config(
    page_title="Healthcare Storytelling Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'dialogue_history' not in st.session_state:
    st.session_state.dialogue_history = []
if 'decisions_made' not in st.session_state:
    st.session_state.decisions_made = []
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None
if 'selected_character' not in st.session_state:
    st.session_state.selected_character = None
if 'biases_identified' not in st.session_state:
    st.session_state.biases_identified = []
if 'narrative_story' not in st.session_state:
    st.session_state.narrative_story = None
if 'story_generated' not in st.session_state:
    st.session_state.story_generated = False
if 'bias_analysis_result' not in st.session_state:
    st.session_state.bias_analysis_result = None
if 'username' not in st.session_state:
    st.session_state.username = "Guest"
if 'db_user_id' not in st.session_state:
    st.session_state.db_user_id = None
if 'db_session_id' not in st.session_state:
    st.session_state.db_session_id = None
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "simulation"  # "simulation", "analytics", or "character_profiles"

# Add speculative scenarios and clinical decision support scenarios to the data file
add_speculative_scenarios_to_data()
add_cdss_scenarios_to_data()

# Load scenarios (now including speculative ones)
scenarios = load_scenarios()
character_profiles = get_character_profiles()

# Apply some custom styles
apply_custom_styles()

# Sidebar for application navigation
with st.sidebar:
    st.title("Healthcare Storytelling")
    
    # User login/profile section
    st.markdown("### User Profile")
    username = st.text_input("Username", value=st.session_state.username)
    
    if username != st.session_state.username:
        # Create/get user in database
        from database import db_manager
        user_id = db_manager.create_user(username, "user")
        
        # Update session state
        st.session_state.username = username
        st.session_state.db_user_id = user_id
        st.rerun()
    
    # Role selection (researcher, healthcare_professional, student)
    user_role_options = ["Researcher", "Healthcare Professional", "Student", "Patient Advocate"]
    user_role = st.selectbox("Your professional role", user_role_options)
    
    # View mode selection
    view_modes = {
        "simulation": "Interactive Simulation",
        "analytics": "Analytics Dashboard",
        "character_profiles": "Character Profiles"
    }
    
    selected_view = st.radio("View Mode", list(view_modes.values()))
    
    # Update view mode in session state
    for mode_key, mode_label in view_modes.items():
        if mode_label == selected_view:
            if st.session_state.view_mode != mode_key:
                st.session_state.view_mode = mode_key
                st.rerun()
    
    # If in simulation mode, show scenario options
    if st.session_state.view_mode == "simulation":
        st.markdown("### Explore Scenarios")
        
        # Scenario selection
        scenario_names = [scenario["title"] for scenario in scenarios]
        selected_scenario = st.selectbox("Choose a scenario", scenario_names)
        
        # Find selected scenario data
        for scenario in scenarios:
            if scenario["title"] == selected_scenario:
                st.session_state.current_scenario = scenario
        
        # Role selection for simulation
        st.markdown("### Select Your Role in Simulation")
        roles = ["Doctor", "Patient", "AI Tool", "Observer"]
        selected_role = st.radio("Choose your role in the simulation", roles)
        
        if selected_role != st.session_state.selected_role:
            st.session_state.selected_role = selected_role
            st.session_state.current_step = 0
            st.session_state.dialogue_history = []
            st.session_state.decisions_made = []
            st.session_state.biases_identified = []
            
            # Reset storytelling variables when changing roles
            st.session_state.narrative_story = None
            st.session_state.story_generated = False
            st.session_state.bias_analysis_result = None
            
            # If we have a user ID, start a new database session
            if st.session_state.db_user_id:
                # End previous session if it exists
                if st.session_state.db_session_id:
                    from database import db_manager
                    db_manager.end_session(st.session_state.db_session_id)
                
                # Create new session
                from database import db_manager
                scenario_id = st.session_state.current_scenario.get("id", st.session_state.current_scenario.get("title"))
                use_gpt = st.session_state.get("use_dynamic_responses", False)
                
                session_id = db_manager.start_session(
                    st.session_state.db_user_id,
                    scenario_id,
                    selected_role,
                    use_gpt
                )
                
                st.session_state.db_session_id = session_id
        
        # Dynamic responses checkbox
        st.markdown("### GPT-Enhanced Experience")
        use_dynamic = st.checkbox("Use GPT for dynamic character responses", 
                                value=st.session_state.get("use_dynamic_responses", False))
        
        if "use_dynamic_responses" not in st.session_state or use_dynamic != st.session_state.use_dynamic_responses:
            st.session_state.use_dynamic_responses = use_dynamic
            st.rerun()
        
        # Reset button
        if st.button("Reset Simulation"):
            # End previous session if it exists
            if st.session_state.db_session_id:
                from database import db_manager
                db_manager.end_session(st.session_state.db_session_id)
                st.session_state.db_session_id = None
            
            # Reset all simulation state variables
            st.session_state.current_step = 0
            st.session_state.dialogue_history = []
            st.session_state.decisions_made = []
            st.session_state.biases_identified = []
            
            # Reset storytelling variables
            st.session_state.narrative_story = None
            st.session_state.story_generated = False
            st.session_state.bias_analysis_result = None
            
            st.rerun()
    
    # Educational section on biases in healthcare
    with st.expander("📚 Common Biases in Healthcare", expanded=False):
        st.markdown("### Common Biases in Healthcare")
        st.markdown("""
        **Anchoring Bias**: Relying too heavily on the first piece of information received.
        
        **Confirmation Bias**: Seeking information that confirms pre-existing beliefs.
        
        **Automation Bias**: Over-reliance on automated systems or AI recommendations.
        
        **Demographic Bias**: Making assumptions based on age, gender, race, or socioeconomic status.
        
        **Representativeness Bias**: Judging the probability of a diagnosis based on how similar a patient's presentation is to the typical case.
        
        **Algorithm Bias**: AI systems trained on non-representative data that perpetuate or amplify existing inequities.
        """)
    
    # Ethical considerations section
    with st.expander("⚖️ Ethical Considerations", expanded=False):
        st.markdown("### Ethical Considerations in AI Healthcare")
        st.markdown("""
        **Justice & Fairness**: Ensuring equitable distribution of benefits and harms across different patient populations.
        
        **Non-maleficence**: Preventing harm from algorithmic decisions or recommendations.
        
        **Transparency**: Making the basis for AI recommendations understandable to clinicians and patients.
        
        **Human Oversight**: Maintaining meaningful human control over AI systems in critical decisions.
        
        **Accountability**: Clearly defining responsibility when AI systems contribute to decisions.
        
        **Patient Autonomy**: Respecting patients' right to make informed decisions about their care.
        """)

# Main content area
st.title("Healthcare Interactive Storytelling Platform")

# Switch between simulation, analytics, and character profiles modes
if st.session_state.view_mode == "analytics":
    # Import and run analytics dashboard
    from analytics import run_analytics
    run_analytics()
elif st.session_state.view_mode == "character_profiles":
    # Character Profiles Management
    from characters import create_custom_character, delete_custom_character
    
    st.markdown("## Character Profiles")
    st.markdown("View and customize character profiles for different roles in the simulation. Select from existing profiles or create your own characters with unique backgrounds and perspectives.")
    
    # Role tabs for viewing/editing different character types
    roles = ["Doctor", "Patient", "AI Tool", "Observer"]
    selected_role_tab = st.tabs(roles)
    
    # Process each role in its tab
    for i, role in enumerate(roles):
        with selected_role_tab[i]:
            st.markdown(f"### {role} Profiles")
            
            # Get profiles for this role
            role_profiles = character_profiles.get(role, {})
            role_description = role_profiles.get('description', f"No description available for {role} role.")
            st.markdown(f"**Role Description**: {role_description}")
            
            # Show responsibilities
            if 'responsibilities' in role_profiles:
                st.markdown("**Responsibilities**:")
                for resp in role_profiles['responsibilities']:
                    st.markdown(f"- {resp}")
            
            # Character backgrounds
            if 'backgrounds' in role_profiles and role_profiles['backgrounds']:
                st.markdown("---")
                st.markdown("### Available Character Backgrounds")
                
                # Create 2 columns for character cards
                col1, col2 = st.columns(2)
                
                # Display character cards
                for idx, background in enumerate(role_profiles['backgrounds']):
                    with col1 if idx % 2 == 0 else col2:
                        with st.container():
                            # Card styling
                            st.markdown("""
                            <style>
                            .character-card {
                                border: 1px solid #ccc;
                                border-radius: 5px;
                                padding: 10px;
                                margin-bottom: 10px;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # Badge for custom characters
                            custom_badge = "🔹 CUSTOM" if background.get('is_custom', False) else ""
                            
                            # Character name and badge
                            st.markdown(f"<div class='character-card'><h4>{background.get('name', 'Unknown')} {custom_badge}</h4>", unsafe_allow_html=True)
                            
                            # Display different fields based on role
                            if role == "Doctor":
                                st.markdown(f"**Specialty**: {background.get('specialty', 'Unknown')}")
                                st.markdown(f"**Years Experience**: {background.get('years_experience', 'Unknown')}")
                            elif role == "Patient":
                                st.markdown(f"**Age**: {background.get('age', 'Unknown')}")
                                st.markdown(f"**Conditions**: {background.get('conditions', 'None noted')}")
                            elif role == "AI Tool":
                                st.markdown(f"**Training Data**: {background.get('training_data', 'Unknown')}")
                            elif role == "Observer":
                                st.markdown(f"**Specialty**: {background.get('specialty', 'Unknown')}")
                            
                            # Common fields for all
                            st.markdown(f"**Perspective**: {background.get('perspective', 'No perspective information')}")
                            st.markdown(f"**Bias Tendencies**: {background.get('biases', 'No bias information')}")
                            
                            # Select button
                            character_id = background.get('id', background.get('name', 'unknown').replace(' ', '_').lower())
                            if st.button(f"Select this {role}", key=f"select_{character_id}"):
                                st.session_state.selected_character = background
                                st.success(f"Selected {background.get('name', 'character')} as your {role}!")
                                
                            # Delete button for custom characters
                            if background.get('is_custom', False):
                                if st.button(f"Delete", key=f"delete_{character_id}"):
                                    if delete_custom_character(role, character_id):
                                        st.success(f"Deleted custom character {background.get('name', 'Unknown')}")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete custom character")
                            
                            st.markdown("</div>", unsafe_allow_html=True)
            
            # Create new character form
            st.markdown("---")
            with st.expander("➕ Create a New Custom Character", expanded=False):
                st.markdown(f"### Create a Custom {role}")
                
                name = st.text_input(f"{role} Name", key=f"new_{role}_name")
                
                # Role-specific fields
                if role == "Doctor":
                    specialty = st.text_input("Medical Specialty", key=f"new_{role}_specialty")
                    years_experience = st.number_input("Years of Experience", min_value=1, max_value=50, value=10, key=f"new_{role}_years")
                    
                    perspective = st.text_area("Professional Perspective", 
                                          placeholder="Describe their approach to medicine and technology...",
                                          key=f"new_{role}_perspective")
                    biases = st.text_area("Potential Biases", 
                                     placeholder="Describe any biases or preferences this doctor might have...",
                                     key=f"new_{role}_biases")
                    
                    if st.button("Create Custom Doctor"):
                        if name and specialty and perspective:
                            new_char = {
                                "name": name,
                                "specialty": specialty,
                                "years_experience": years_experience,
                                "perspective": perspective,
                                "biases": biases
                            }
                            if create_custom_character(role, new_char):
                                st.success(f"Created custom doctor: {name}")
                                st.rerun()
                            else:
                                st.error("Failed to create custom character")
                        else:
                            st.warning("Please fill in all required fields")
                
                elif role == "Patient":
                    age = st.number_input("Age", min_value=1, max_value=110, value=45, key=f"new_{role}_age")
                    conditions = st.text_input("Medical Conditions", key=f"new_{role}_conditions")
                    
                    perspective = st.text_area("Patient Perspective", 
                                          placeholder="Describe their attitude toward healthcare and treatment...",
                                          key=f"new_{role}_perspective")
                    biases = st.text_area("Potential Biases", 
                                     placeholder="Describe any biases or healthcare preferences this patient might have...",
                                     key=f"new_{role}_biases")
                    
                    if st.button("Create Custom Patient"):
                        if name and conditions and perspective:
                            new_char = {
                                "name": name,
                                "age": age,
                                "conditions": conditions,
                                "perspective": perspective,
                                "biases": biases
                            }
                            if create_custom_character(role, new_char):
                                st.success(f"Created custom patient: {name}")
                                st.rerun()
                            else:
                                st.error("Failed to create custom character")
                        else:
                            st.warning("Please fill in all required fields")
                
                elif role == "AI Tool":
                    training_data = st.text_area("Training Data Description", 
                                            placeholder="Describe the data used to train this AI...",
                                            key=f"new_{role}_training")
                    
                    perspective = st.text_area("AI System Perspective", 
                                          placeholder="Describe how this AI approaches healthcare decisions...",
                                          key=f"new_{role}_perspective")
                    biases = st.text_area("Potential Biases", 
                                     placeholder="Describe any algorithmic biases or limitations this AI might have...",
                                     key=f"new_{role}_biases")
                    
                    if st.button("Create Custom AI Tool"):
                        if name and training_data and perspective:
                            new_char = {
                                "name": name,
                                "training_data": training_data,
                                "perspective": perspective,
                                "biases": biases
                            }
                            if create_custom_character(role, new_char):
                                st.success(f"Created custom AI tool: {name}")
                                st.rerun()
                            else:
                                st.error("Failed to create custom character")
                        else:
                            st.warning("Please fill in all required fields")
                
                elif role == "Observer":
                    specialty = st.text_input("Observer Specialty", key=f"new_{role}_specialty")
                    
                    perspective = st.text_area("Observer Perspective", 
                                          placeholder="Describe their approach to analyzing healthcare interactions...",
                                          key=f"new_{role}_perspective")
                    biases = st.text_area("Potential Biases", 
                                     placeholder="Describe any biases this observer might bring to their analysis...",
                                     key=f"new_{role}_biases")
                    
                    if st.button("Create Custom Observer"):
                        if name and specialty and perspective:
                            new_char = {
                                "name": name,
                                "specialty": specialty,
                                "perspective": perspective,
                                "biases": biases
                            }
                            if create_custom_character(role, new_char):
                                st.success(f"Created custom observer: {name}")
                                st.rerun()
                            else:
                                st.error("Failed to create custom character")
                        else:
                            st.warning("Please fill in all required fields")
else:
    # Simulation mode
    st.markdown("### Observe decision-making processes and identify potential biases")
    
    # Display current scenario description
    if st.session_state.current_scenario:
        scenario_desc_col, character_col = st.columns([3, 1])
        
        with scenario_desc_col:
            st.subheader(f"Scenario: {st.session_state.current_scenario['title']}")
            st.markdown(get_scenario_description(st.session_state.current_scenario))
        
        with character_col:
            if st.session_state.selected_role:
                st.subheader("Your Role")
                role_icon = get_role_icon(st.session_state.selected_role)
                st.markdown(f"### {role_icon} {st.session_state.selected_role}")
                
                # Display character profile
                if st.session_state.selected_role in character_profiles:
                    st.markdown(f"**Profile**: {character_profiles[st.session_state.selected_role]['description']}")

        # Run the simulation
        simulation_container = st.container()
        with simulation_container:
            run_simulation(
                st.session_state.current_scenario,
                st.session_state.selected_role
            )
    
    # Decision path visualization and analysis
    if st.session_state.decisions_made:
        st.markdown("---")
        st.subheader("Decision Path Analysis")
        
        viz_col, analysis_col = st.columns([1, 1])
        
        with viz_col:
            st.markdown("### Decision Tree Visualization")
            visualize_decision_tree(
                st.session_state.current_scenario,
                st.session_state.decisions_made
            )
        
        with analysis_col:
            st.markdown("### Bias Identification")
            st.markdown("Potential biases identified in the current scenario:")
            
            if st.session_state.current_scenario.get("biases"):
                bias_df = pd.DataFrame(st.session_state.current_scenario["biases"])
                st.dataframe(bias_df, hide_index=True)
            else:
                st.info("No biases have been identified in this scenario yet.")
            
            # Allow users to add new biases they've identified
            with st.expander("Identify a new bias"):
                bias_type = st.selectbox(
                    "Type of bias",
                    ["Anchoring bias", "Confirmation bias", "Gender bias", "Age bias", 
                     "Racial bias", "Socioeconomic bias", "Other"]
                )
                
                bias_description = st.text_area(
                    "Describe the bias you identified",
                    placeholder="Explain how this bias manifested in the scenario..."
                )
                
                if st.button("Submit Bias Identification"):
                    if bias_description:
                        new_bias = {
                            "type": bias_type,
                            "description": bias_description,
                            "step": st.session_state.current_step
                        }
                        st.session_state.biases_identified.append(new_bias)
                        st.success("Bias identification recorded!")
                        st.rerun()
            
            # Display user-identified biases
            if st.session_state.biases_identified:
                st.markdown("### Your Identified Biases")
                for i, bias in enumerate(st.session_state.biases_identified):
                    st.markdown(f"**{bias['type']}** (at step {bias['step']})")
                    st.markdown(f"_{bias['description']}_")
                    st.markdown("---")
            
            # Add AI-powered ethical analysis
            if st.session_state.dialogue_history and os.environ.get("OPENAI_API_KEY"):
                with st.expander("🔍 AI-Powered Ethical Analysis", expanded=False):
                    st.markdown("### Potential Ethical Harms Analysis")
                    st.markdown("Use AI to analyze the dialogue and decisions for potential ethical concerns and biases.")
                    
                    if st.button("Generate Ethical Analysis"):
                        from openai_integration import analyze_biases
                        
                        # Prepare context for analysis
                        dialogue_text = "\n".join([f"{entry['role']}: {entry['text']}" for entry in st.session_state.dialogue_history])
                        decision_text = ", ".join(st.session_state.decision_text) if hasattr(st.session_state, 'decision_text') else "No decisions made yet"
                        
                        # Context for analysis
                        analysis_context = {
                            "scenario_description": st.session_state.current_scenario.get("description", ""),
                            "doctor_profile": st.session_state.current_scenario.get("characters", {}).get("doctor", {}).get("background", ""),
                            "patient_profile": st.session_state.current_scenario.get("characters", {}).get("patient", {}).get("background", ""),
                            "ai_tool_profile": st.session_state.current_scenario.get("characters", {}).get("ai_tool", {}).get("background", "")
                        }
                        
                        with st.spinner("Analyzing dialogue and decisions for ethical concerns..."):
                            analysis_result = analyze_biases(analysis_context, dialogue_text, decision_text)
                            
                            if analysis_result and "biases" in analysis_result:
                                for bias in analysis_result["biases"]:
                                    with st.container():
                                        st.markdown(f"**{bias.get('type', 'Unspecified Bias')}**")
                                        st.markdown(f"*{bias.get('description', '')}*")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.warning(f"**Potential Harm**: {bias.get('potential_harm', '')}")
                                        with col2:
                                            st.success(f"**Mitigation Strategy**: {bias.get('mitigation', '')}")
                                        
                                        st.markdown("---")
                            else:
                                st.info("No significant ethical concerns were identified in this interaction.")
    else:
        st.info("Please select a scenario from the sidebar to begin.")

# Footer
st.markdown("---")
st.markdown(
    "This interactive platform helps healthcare professionals understand and identify "
    "biases in clinical decision-making through role-playing scenarios."
)
