import json
import os
import streamlit as st

# Default character profiles
DEFAULT_PROFILES = {
    "Doctor": {
        "description": "As a doctor, you make clinical decisions based on patient information and system recommendations. You must balance relying on technology with your own medical judgment.",
        "responsibilities": [
            "Gather patient information",
            "Use clinical decision support systems appropriately",
            "Make final treatment decisions",
            "Be aware of potential biases in your decision-making"
        ],
        "backgrounds": [
            {
                "name": "Dr. Williams",
                "specialty": "Cardiology",
                "years_experience": 15,
                "perspective": "Technology enthusiast who relies heavily on clinical decision support tools",
                "biases": "Tends to favor technology-driven solutions over traditional approaches"
            },
            {
                "name": "Dr. Rodriguez",
                "specialty": "Primary Care",
                "years_experience": 25,
                "perspective": "Cautious about new technology, prefers established clinical guidelines",
                "biases": "Sometimes skeptical of AI recommendations, may dismiss novel approaches"
            },
            {
                "name": "Dr. Chen",
                "specialty": "Internal Medicine",
                "years_experience": 8,
                "perspective": "Balanced approach, validates AI recommendations with clinical experience",
                "biases": "May spend more time with tech-savvy patients who engage with health apps"
            },
            {
                "name": "Dr. Washington",
                "specialty": "Emergency Medicine",
                "years_experience": 12,
                "perspective": "Quick decision-maker who uses AI as a safety check",
                "biases": "Under time pressure, may over-rely on algorithmic recommendations"
            }
        ]
    },
    "Patient": {
        "description": "As a patient, you experience symptoms and communicate with healthcare providers. Your perspective may differ from clinical assessments, and you may need to advocate for yourself.",
        "responsibilities": [
            "Communicate symptoms clearly",
            "Ask questions about diagnoses and treatments",
            "Share relevant health information",
            "Express concerns when you feel unheard"
        ],
        "backgrounds": [
            {
                "name": "Maria Garcia",
                "age": 58,
                "conditions": "Hypertension, pre-diabetes",
                "perspective": "Trusts doctors completely, hesitant to question medical advice",
                "biases": "May withhold information that seems unimportant or embarrassing"
            },
            {
                "name": "James Thompson",
                "age": 42,
                "conditions": "Chronic back pain, anxiety",
                "perspective": "Researches extensively online, comes prepared with questions",
                "biases": "Sometimes distrusts conventional medicine, prefers alternative therapies"
            },
            {
                "name": "Aisha Johnson",
                "age": 35,
                "conditions": "Asthma, migraines",
                "perspective": "Active self-advocate, monitors symptoms with health apps",
                "biases": "May be skeptical of diagnoses that don't match her own research"
            },
            {
                "name": "Robert Kim",
                "age": 67,
                "conditions": "Cardiovascular disease, type 2 diabetes",
                "perspective": "Traditional view of doctor-patient relationship, doesn't like technology",
                "biases": "May not disclose use of complementary therapies or non-adherence"
            }
        ]
    },
    "AI Tool": {
        "description": "As an AI clinical decision support system, you provide recommendations based on available data. Your suggestions are influenced by your training data and may contain biases.",
        "responsibilities": [
            "Process patient data",
            "Generate treatment recommendations",
            "Identify potential risks",
            "Update assessments based on new information"
        ],
        "backgrounds": [
            {
                "name": "PREVENT Cardiovascular Risk Assessment Tool",
                "training_data": "Large dataset of cardiovascular outcomes, primarily from urban research hospitals",
                "perspective": "Prioritizes population-level statistics over individual variations",
                "biases": "May underestimate risk in populations underrepresented in training data"
            },
            {
                "name": "PainAssess AI",
                "training_data": "Pain reports correlated with measurable physiological indicators",
                "perspective": "Emphasizes objective measures over subjective patient reports",
                "biases": "May underestimate pain in groups with different pain expressions or communication styles"
            },
            {
                "name": "MediGuide Decision Support",
                "training_data": "Comprehensive clinical guidelines and thousands of patient cases",
                "perspective": "Balances cost-effectiveness with clinical efficacy",
                "biases": "May prioritize common presentations over rare conditions"
            },
            {
                "name": "DiagnosticPartner AI",
                "training_data": "Diagnostic imaging with confirmed outcomes from multiple health systems",
                "perspective": "Conservative approach that prioritizes sensitivity over specificity",
                "biases": "May recommend excessive testing to avoid missing conditions"
            }
        ]
    },
    "Observer": {
        "description": "As an observer, you analyze the interactions between doctors, patients, and AI systems. You identify potential biases and ethical considerations in healthcare decision-making.",
        "responsibilities": [
            "Watch for biases in clinical decisions",
            "Analyze how AI recommendations influence care",
            "Consider ethical implications of healthcare decisions", 
            "Identify opportunities for system improvement"
        ],
        "backgrounds": [
            {
                "name": "Ethics Researcher",
                "specialty": "Medical Ethics",
                "perspective": "Focuses on patient autonomy and informed consent",
                "biases": "May prioritize ethical principles over practical constraints"
            },
            {
                "name": "Health Equity Advocate",
                "specialty": "Social Determinants of Health",
                "perspective": "Analyzes how socioeconomic factors influence care quality",
                "biases": "Particularly sensitive to disparities affecting marginalized groups"
            },
            {
                "name": "AI Safety Engineer",
                "specialty": "Algorithm Auditing",
                "perspective": "Evaluates how AI systems perform across diverse populations",
                "biases": "May focus more on technical aspects than interpersonal dynamics"
            },
            {
                "name": "Clinical Quality Improvement Specialist",
                "specialty": "Healthcare Operations",
                "perspective": "Examines how workflow and systems affect decision quality",
                "biases": "May emphasize efficiency and standardization over personalization"
            }
        ]
    }
}

# Path to store custom profiles
CUSTOM_PROFILES_PATH = 'data/custom_character_profiles.json'

def save_custom_profiles(profiles):
    """Save custom character profiles to a JSON file"""
    try:
        os.makedirs('data', exist_ok=True)
        with open(CUSTOM_PROFILES_PATH, 'w') as f:
            json.dump(profiles, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving custom profiles: {e}")
        return False

def load_custom_profiles():
    """Load custom character profiles from JSON file"""
    if not os.path.exists(CUSTOM_PROFILES_PATH):
        return {}
    
    try:
        with open(CUSTOM_PROFILES_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading custom profiles: {e}")
        return {}

def get_character_profiles():
    """Return character profiles for different roles, including custom ones"""
    # Load custom profiles and merge with defaults
    custom_profiles = load_custom_profiles()
    
    # Create a deep copy of default profiles
    merged_profiles = {role: profile.copy() for role, profile in DEFAULT_PROFILES.items()}
    
    # Add custom backgrounds to each role
    for role, profile in custom_profiles.items():
        if role in merged_profiles:
            if 'custom_backgrounds' in profile:
                if 'backgrounds' not in merged_profiles[role]:
                    merged_profiles[role]['backgrounds'] = []
                
                # Add custom backgrounds, marking them as custom
                for bg in profile['custom_backgrounds']:
                    bg['is_custom'] = True
                    merged_profiles[role]['backgrounds'].append(bg)
    
    return merged_profiles

def create_custom_character(role, character_data):
    """Create a custom character for a specific role"""
    if role not in DEFAULT_PROFILES:
        return False
    
    # Load existing custom profiles
    custom_profiles = load_custom_profiles()
    
    # Initialize the role if it doesn't exist
    if role not in custom_profiles:
        custom_profiles[role] = {"custom_backgrounds": []}
    
    # Add the new character, with an ID
    character_data['id'] = f"custom_{len(custom_profiles[role]['custom_backgrounds']) + 1}"
    custom_profiles[role]['custom_backgrounds'].append(character_data)
    
    # Save the updated profiles
    return save_custom_profiles(custom_profiles)

def delete_custom_character(role, character_id):
    """Delete a custom character by ID"""
    custom_profiles = load_custom_profiles()
    
    if role in custom_profiles and 'custom_backgrounds' in custom_profiles[role]:
        # Find and remove the character with the matching ID
        custom_profiles[role]['custom_backgrounds'] = [
            char for char in custom_profiles[role]['custom_backgrounds'] 
            if char.get('id') != character_id
        ]
        
        # Save the updated profiles
        return save_custom_profiles(custom_profiles)
    
    return False
