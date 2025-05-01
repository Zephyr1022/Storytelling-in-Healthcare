import streamlit as st
import time
import random
import json
import os
from openai_integration import generate_character_response, analyze_biases

def get_role_icon(role):
    """Get an icon for each role"""
    icons = {
        "Doctor": "👩‍⚕️",
        "Patient": "🧑",
        "AI Tool": "🤖",
        "Observer": "👁️"
    }
    return icons.get(role, "👤")

def find_step_by_id(scenario, step_id):
    """Find a step in the scenario by its ID"""
    for step in scenario.get("steps", []):
        if step.get("id") == step_id:
            return step
    return None

def get_dialogue_history_text(dialogue_history):
    """Convert dialogue history to a formatted text for the prompt"""
    history_text = ""
    for entry in dialogue_history:
        role = entry.get("role", "")
        text = entry.get("text", "")
        if "Decision" not in text:  # Skip decision entries
            history_text += f"{role}: {text}\n"
    return history_text

def run_simulation(scenario, user_role):
    """Run the interactive simulation based on the selected scenario and role"""
    if not scenario:
        return
    
    # Get current step
    current_step_id = "start"
    if st.session_state.decisions_made:
        current_step_id = st.session_state.decisions_made[-1]
    
    current_step = find_step_by_id(scenario, current_step_id)
    
    if not current_step:
        st.error("Error: Could not find the current step in the scenario.")
        return
        
    # Display selected character profile if one is chosen
    if 'selected_character' in st.session_state and st.session_state.selected_character:
        character = st.session_state.selected_character
        with st.expander("👤 Your Character Profile", expanded=False):
            st.markdown(f"### {character.get('name', 'Your Character')}")
            
            # Display different fields based on role
            if user_role == "Doctor":
                if 'specialty' in character:
                    st.markdown(f"**Specialty**: {character.get('specialty')}")
                if 'years_experience' in character:
                    st.markdown(f"**Years Experience**: {character.get('years_experience')}")
            elif user_role == "Patient":
                if 'age' in character:
                    st.markdown(f"**Age**: {character.get('age')}")
                if 'conditions' in character:
                    st.markdown(f"**Conditions**: {character.get('conditions')}")
            elif user_role == "AI Tool":
                if 'training_data' in character:
                    st.markdown(f"**Training Data**: {character.get('training_data')}")
            elif user_role == "Observer":
                if 'specialty' in character:
                    st.markdown(f"**Specialty**: {character.get('specialty')}")
            
            # Common fields for all roles
            if 'perspective' in character:
                st.markdown(f"**Perspective**: {character.get('perspective')}")
            if 'biases' in character:
                st.markdown(f"**Bias Tendencies**: {character.get('biases')}")
    
    # Initialize dynamic response toggle if it doesn't exist
    if 'use_dynamic_responses' not in st.session_state:
        st.session_state.use_dynamic_responses = False
    
    # Display system information if available (for clinical decision support scenarios)
    if "system_info" in current_step:
        with st.expander("📋 Clinical Information", expanded=True):
            for info in current_step["system_info"]:
                st.markdown(f"**{info['phase']}**: {info['text']}")
    
    # Display system analysis if available
    if "system_analysis" in current_step:
        with st.expander("⚙️ AI System Analysis", expanded=True):
            for analysis in current_step["system_analysis"]:
                st.markdown(f"**{analysis['phase']}**: {analysis['text']}")
    
    # Display dialogue
    st.markdown("---")
    st.subheader("Clinical Interaction")
    
    # Add a toggle for dynamic responses using OpenAI
    st.session_state.use_dynamic_responses = st.checkbox(
        "Use GPT for dynamic character responses", 
        value=st.session_state.use_dynamic_responses,
        help="When enabled, characters will generate dynamic responses using OpenAI GPT instead of using predefined dialogue."
    )
    
    dialogue_container = st.container()
    
    with dialogue_container:
        # Display existing dialogue history
        for entry in st.session_state.dialogue_history:
            role = entry["role"]
            text = entry["text"]
            
            role_icon = get_role_icon(role.capitalize())
            
            # Format differently based on role
            if role.lower() == "narrator":
                st.markdown(f"*{text}*")
            else:
                st.markdown(f"{role_icon} **{role.capitalize()}**: {text}")
        
        # Add current step dialogue if not already in history
        current_dialogue_keys = set([d["key"] for d in st.session_state.dialogue_history if "key" in d])
        
        # Prepare context for dynamic responses
        if st.session_state.use_dynamic_responses:
            dialogue_history_text = get_dialogue_history_text(st.session_state.dialogue_history)
            scenario_description = scenario.get('description', '')
            
            # Get character profiles
            characters = scenario.get('characters', {})
            potential_biases = []
            
            # Get potential biases from the current step and previous steps
            if current_step.get('potential_bias'):
                potential_biases.append(current_step.get('potential_bias'))
            
            for bias in scenario.get('biases', []):
                if bias.get('step') == current_step_id:
                    potential_biases.append(f"{bias.get('type')}: {bias.get('description')}")
            
            biases_text = "; ".join(potential_biases) if potential_biases else "None identified"
            
            # System info context for clinical decision support
            system_info_text = ""
            if "system_info" in current_step:
                system_info_text = "Clinical context:\n"
                for info in current_step["system_info"]:
                    system_info_text += f"- {info['phase']}: {info['text']}\n"
        
        # Handle both dialogue formats: traditional and clinical_interaction
        dialogue_entries = []
        
        # Check which dialogue format is being used
        if "dialogue" in current_step and isinstance(current_step["dialogue"], dict):
            # Traditional format: convert dict to list format
            for speaker, text in current_step["dialogue"].items():
                dialogue_entries.append({
                    "role": speaker,
                    "text": text,
                    "key": f"{current_step_id}_{speaker}"
                })
        elif "dialogue" in current_step and isinstance(current_step["dialogue"], list):
            # List format
            for i, entry in enumerate(current_step["dialogue"]):
                entry["key"] = f"{current_step_id}_{i}"
                dialogue_entries.append(entry)
        elif "clinical_interaction" in current_step:
            # Clinical interaction format
            for i, entry in enumerate(current_step["clinical_interaction"]):
                entry["key"] = f"{current_step_id}_{i}"
                dialogue_entries.append(entry)
        
        # Process all dialogue entries
        for entry in dialogue_entries:
            speaker = entry["role"]
            text = entry["text"]
            dialogue_key = entry["key"]
            
            if dialogue_key not in current_dialogue_keys:
                # Wait a bit for a more natural conversation flow (only in visual display)
                if st.session_state.dialogue_history:  # Don't wait for the first message
                    time.sleep(0.5)  
                
                # Generate dynamic response if enabled, otherwise use predefined text
                if st.session_state.use_dynamic_responses and os.environ.get("OPENAI_API_KEY"):
                    # Construct context for the character's response
                    # Use custom character profile if available for the current role
                    custom_profile = ""
                    if speaker.lower() == user_role.lower() and 'selected_character' in st.session_state and st.session_state.selected_character:
                        char = st.session_state.selected_character
                        custom_profile = f"Name: {char.get('name', '')}\n"
                        
                        if speaker.lower() == "doctor":
                            custom_profile += f"Specialty: {char.get('specialty', '')}\n"
                            custom_profile += f"Years Experience: {char.get('years_experience', '')}\n"
                        elif speaker.lower() == "patient":
                            custom_profile += f"Age: {char.get('age', '')}\n"
                            custom_profile += f"Conditions: {char.get('conditions', '')}\n"
                        elif speaker.lower() == "ai_tool":
                            custom_profile += f"Training Data: {char.get('training_data', '')}\n"
                        elif speaker.lower() == "observer":
                            custom_profile += f"Specialty: {char.get('specialty', '')}\n"
                            
                        custom_profile += f"Perspective: {char.get('perspective', '')}\n"
                        custom_profile += f"Biases: {char.get('biases', '')}"
                    
                    character_context = {
                        "profile": custom_profile if custom_profile else characters.get(speaker.lower(), {}).get("background", ""),
                        "context": scenario_description,
                        "situation": f"You are at step '{current_step_id}' in the scenario.",
                        "dialogue_history": dialogue_history_text,
                        "biases": biases_text,
                        "clinical_context": system_info_text if 'system_info_text' in locals() else ""
                    }
                    
                    # Add role-specific context
                    if speaker.lower() == "doctor":
                        patient_statement = next((e["text"] for e in dialogue_entries if e["role"].lower() == "patient"), "")
                        character_context["patient_statement"] = patient_statement
                    elif speaker.lower() == "patient":
                        doctor_statement = next((e["text"] for e in dialogue_entries if e["role"].lower() == "doctor"), "")
                        character_context["doctor_statement"] = doctor_statement
                    elif speaker.lower() == "ai_tool":
                        character_context["patient_data"] = f"Patient: {characters.get('patient', {}).get('background', '')}"
                    
                    # Generate the response
                    try:
                        dynamic_text = generate_character_response(speaker.lower(), character_context)
                        if dynamic_text:
                            text = dynamic_text
                    except Exception as e:
                        st.error(f"Error generating dynamic response: {str(e)}")
                
                # Display the dialogue
                role_icon = get_role_icon(speaker.capitalize())
                
                if speaker.lower() == "narrator":
                    st.markdown(f"*{text}*")
                else:
                    st.markdown(f"{role_icon} **{speaker.capitalize()}**: {text}")
                
                # Add to history
                st.session_state.dialogue_history.append({
                    "role": speaker,
                    "text": text,
                    "key": dialogue_key
                })
                
                # Save to database if tracking is enabled
                if "db_session_id" in st.session_state and st.session_state.db_session_id:
                    from database import db_manager
                    
                    # Record the dialogue entry in the database
                    db_manager.add_dialogue_entry(
                        st.session_state.db_session_id,
                        current_step_id,
                        speaker,
                        text,
                        is_gpt_generated=st.session_state.use_dynamic_responses
                    )
    
    # Display decisions if there are any
    decisions = current_step.get("decisions", [])
    
    if decisions:
        st.markdown("---")
        st.subheader("What would you do?")
        
        # Show decision options based on user role
        decision_col1, decision_col2 = st.columns(2)
        
        # Show appropriate decisions based on user role
        if user_role.lower() == "doctor":
            for i, decision in enumerate(decisions):
                if i % 2 == 0:
                    with decision_col1:
                        if st.button(decision["text"], key=f"decision_{i}"):
                            make_decision(decision["next_step"], decision["text"])
                else:
                    with decision_col2:
                        if st.button(decision["text"], key=f"decision_{i}"):
                            make_decision(decision["next_step"], decision["text"])
        else:
            # If user is not the doctor, show what decision the doctor makes
            # Allow a moment for the dialogue to be read
            time.sleep(1)
            
            # Non-doctor roles observe the decision rather than make it
            if "observer" in user_role.lower() or "patient" in user_role.lower() or "ai" in user_role.lower():
                st.info("As an observer, you're watching how the doctor makes decisions...")
                
                # Auto-select a decision after a short delay
                decision = decisions[0]  # Default to first decision
                
                # Display the decision being made
                st.markdown(f"👩‍⚕️ **Doctor** decides: {decision['text']}")
                
                # Add to dialogue history
                st.session_state.dialogue_history.append({
                    "role": "Doctor",
                    "text": f"[Decision: {decision['text']}]",
                    "key": f"{current_step_id}_decision"
                })
                
                # Make the decision automatically after a short delay
                make_decision(decision["next_step"], decision["text"])
    
    # If there are no decisions, it's the end of the scenario
    elif current_step_id not in ["conclusion_good", "conclusion_bad", "good_outcome", "adverse_event", "delayed_intervention"]:
        # Find a conclusion if available
        conclusion_steps = [s for s in scenario.get("steps", []) 
                          if s.get("id", "").startswith("conclusion") or 
                          s.get("id") in ["good_outcome", "adverse_event", "delayed_intervention"]]
        
        if conclusion_steps:
            conclusion = conclusion_steps[0]
            make_decision(conclusion["id"], "Continue to conclusion")
        else:
            st.markdown("---")
            st.success("Scenario complete. You've reached the end of this narrative.")
            
            # Reflection prompt
            st.subheader("Reflection")
            st.text_area("What biases or ethical considerations did you observe in this scenario?", 
                        key="reflection_input")
            
            if st.button("Submit Reflection"):
                st.session_state.current_step = 0
                st.session_state.dialogue_history = []
                st.success("Thank you for your reflection! Choose another scenario or role to continue exploring.")
    
    # Show bias information if this is the last step or observer role
    if (not decisions or user_role.lower() == "observer") and current_step.get("potential_bias"):
        st.markdown("---")
        st.subheader("Potential Bias Analysis")
        
        bias_info = current_step.get("potential_bias")
        st.info(f"**Potential Bias at this step**: {bias_info}")
        
        # Add additional context for observers
        if user_role.lower() == "observer":
            st.markdown("As an observer, consider:")
            st.markdown("1. How did this bias affect the clinical decision-making?")
            st.markdown("2. What systems or processes could prevent this bias?")
            st.markdown("3. How could the AI tool be improved to address this bias?")
        
        # Add Storytelling section to help developers understand potential harm
        if st.session_state.dialogue_history and os.environ.get("OPENAI_API_KEY"):
            st.markdown("---")
            st.subheader("🧩 Storytelling for Developers")
            st.markdown("This narrative story illustrates the potential real-world impact of algorithmic bias in this scenario.")
            
            if 'story_generated' not in st.session_state or not st.session_state.story_generated:
                if st.button("Generate 15-Sentence Story"):
                    from openai_integration import generate_storytelling_narrative, analyze_biases
                    
                    # Prepare context for storytelling
                    dialogue_text = "\n".join([f"{entry['role']}: {entry['text']}" for entry in st.session_state.dialogue_history])
                    decision_text = ", ".join(st.session_state.decision_text) if hasattr(st.session_state, 'decision_text') else "No decisions made yet"
                    
                    # Context for the narrative
                    storytelling_context = {
                        "scenario_description": scenario.get("description", ""),
                        "doctor_profile": scenario.get("characters", {}).get("doctor", {}).get("background", ""),
                        "patient_profile": scenario.get("characters", {}).get("patient", {}).get("background", ""),
                        "ai_tool_profile": scenario.get("characters", {}).get("ai_tool", {}).get("background", ""),
                        "decisions": decision_text
                    }
                    
                    # Get bias analysis if it doesn't exist
                    if 'bias_analysis_result' not in st.session_state or not st.session_state.bias_analysis_result:
                        with st.spinner("Analyzing biases..."):
                            bias_analysis = analyze_biases(storytelling_context, dialogue_text, decision_text)
                            st.session_state.bias_analysis_result = bias_analysis
                    else:
                        bias_analysis = st.session_state.bias_analysis_result
                    
                    # Format bias analysis for storytelling
                    bias_analysis_text = ""
                    if bias_analysis and "biases" in bias_analysis:
                        for bias in bias_analysis["biases"]:
                            bias_analysis_text += f"Type: {bias.get('type', '')}\n"
                            bias_analysis_text += f"Description: {bias.get('description', '')}\n"
                            bias_analysis_text += f"Potential harm: {bias.get('potential_harm', '')}\n"
                            bias_analysis_text += f"Mitigation: {bias.get('mitigation', '')}\n\n"
                    
                    # Generate the story
                    with st.spinner("Creating an intuitive narrative story..."):
                        story = generate_storytelling_narrative(storytelling_context, dialogue_text, bias_analysis_text)
                        st.session_state.narrative_story = story
                        st.session_state.story_generated = True
                        st.rerun()
            
            # Display the generated story
            if 'narrative_story' in st.session_state and st.session_state.narrative_story:
                story_container = st.container()
                with story_container:
                    st.markdown("### Narrative Story")
                    st.markdown(st.session_state.narrative_story)
                    
                    # Add buttons to copy the story or regenerate
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Copy Story to Clipboard"):
                            st.markdown(
                                f"""
                                <script>
                                    navigator.clipboard.writeText(`{st.session_state.narrative_story}`);
                                </script>
                                """,
                                unsafe_allow_html=True
                            )
                            st.success("Story copied to clipboard!")
                    
                    with col2:
                        if st.button("Regenerate Story"):
                            st.session_state.story_generated = False
                            if 'narrative_story' in st.session_state:
                                del st.session_state.narrative_story
                            st.rerun()

def make_decision(next_step_id, decision_text):
    """Process a decision and move to the next step"""
    # Record the decision
    if "decision_text" not in st.session_state:
        st.session_state.decision_text = []
    
    st.session_state.decision_text.append(decision_text)
    st.session_state.decisions_made.append(next_step_id)
    
    # Save to database if tracking is enabled
    if "db_session_id" in st.session_state and st.session_state.db_session_id:
        from database import db_manager
        
        # Get current step ID
        current_step_id = "start"
        if len(st.session_state.decisions_made) > 1:
            current_step_id = st.session_state.decisions_made[-2]  # The previous decision
        
        # Record the decision in the database
        db_manager.add_decision(
            st.session_state.db_session_id,
            current_step_id,
            decision_text,
            next_step_id
        )
    
    # Increment step counter
    st.session_state.current_step += 1
    
    # Force a rerun to update the interface
    st.rerun()
