import os
import json
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define prompts for different roles
ROLE_PROMPTS = {
    "doctor": """You are roleplaying as a doctor in a healthcare simulation. 
    Your character profile is: {profile}
    
    Context: {context}
    
    Current situation: {situation}
    
    Previous dialogue: {dialogue_history}
    
    The patient has just said: "{patient_statement}"
    
    Respond as the doctor, keeping these potential biases in mind: {biases}
    
    Make your response concise (1-3 sentences). Maintain a professional tone while subtly reflecting any biases mentioned.
    """,
    
    "patient": """You are roleplaying as a patient in a healthcare simulation. 
    Your character profile is: {profile}
    
    Context: {context}
    
    Current situation: {situation}
    
    Previous dialogue: {dialogue_history}
    
    The doctor has just said: "{doctor_statement}"
    
    Respond as the patient, expressing your concerns, feelings, and perspective in a realistic way.
    Keep your response concise (1-3 sentences).
    """,
    
    "ai_tool": """You are roleplaying as an AI clinical decision support tool in a healthcare simulation.
    Your character profile is: {profile}
    
    Context: {context}
    
    Current patient data: {patient_data}
    
    Previous dialogue: {dialogue_history}
    
    You should provide a recommendation based on the available data, but with the following biases or limitations: {biases}
    
    Format your response like a clinical decision support system would, with analysis and recommendations.
    Keep your response concise (1-3 sentences).
    """
}

BIAS_ANALYSIS_PROMPT = """
Analyze the following healthcare scenario dialogue for potential biases, ethical concerns, or fairness issues:

Scenario context: {context}
Doctor profile: {doctor_profile}
Patient profile: {patient_profile}
AI tool profile: {ai_tool_profile}

Dialogue:
{dialogue}

Decision made: {decision}

Identify and explain 2-3 specific biases or ethical concerns that might be present in this interaction.
Format your response as a JSON object with the following structure:
{{
  "biases": [
    {{
      "type": "Name of bias type",
      "description": "Brief explanation of how this bias manifests in the scenario",
      "potential_harm": "Description of potential harm to the patient",
      "mitigation": "Brief suggestion for how this bias could be mitigated"
    }}
  ]
}}
"""


def generate_character_response(role, context):
    """Generate a dynamic response for a character based on their role"""
    if not os.environ.get("OPENAI_API_KEY"):
        return f"Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    
    # Select the appropriate prompt template
    prompt_template = ROLE_PROMPTS.get(role.lower())
    if not prompt_template:
        return f"Error: Unknown role '{role}'"
    
    # Fill the prompt template with context
    prompt = prompt_template.format(**context)
    
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": "You are roleplaying as a character in a healthcare simulation focused on identifying biases and ethical issues."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generating response: {str(e)}"


def analyze_biases(context, dialogue, decision):
    """Analyze the biases present in a scenario interaction"""
    if not os.environ.get("OPENAI_API_KEY"):
        return None
    
    prompt = BIAS_ANALYSIS_PROMPT.format(
        context=context.get("scenario_description", ""),
        doctor_profile=context.get("doctor_profile", ""),
        patient_profile=context.get("patient_profile", ""),
        ai_tool_profile=context.get("ai_tool_profile", ""),
        dialogue=dialogue,
        decision=decision
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": "You are an expert in healthcare ethics and bias identification."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=500,
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        print(f"Error analyzing biases: {str(e)}")
        return None


def generate_storytelling_narrative(context, dialogue, bias_analysis):
    """Generate a 15-sentence narrative story based on the scenario, clinical interactions, and bias analysis"""
    if not os.environ.get("OPENAI_API_KEY"):
        return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable to enable storytelling."
    
    # Create a concise prompt that focuses on educational storytelling
    prompt = f"""
    Create a compelling 15-sentence narrative story that explains the healthcare scenario, 
    clinical interactions, and potential biases in a way that's intuitive and easy to understand.
    
    This story should help software developers anticipate harmful algorithmic biases BEFORE 
    they develop healthcare AI systems. Focus on making the potential harms concrete and personal.
    
    Use these details to craft your story:
    
    SCENARIO CONTEXT:
    {context.get("scenario_description", "")}
    
    CHARACTERS:
    - Doctor: {context.get("doctor_profile", "")}
    - Patient: {context.get("patient_profile", "")}
    - AI Tool: {context.get("ai_tool_profile", "")}
    
    CLINICAL INTERACTION:
    {dialogue}
    
    DECISIONS MADE:
    {context.get("decisions", "")}
    
    BIAS ANALYSIS:
    {bias_analysis}
    
    INSTRUCTIONS:
    1. Write exactly 15 sentences, no more and no less.
    2. Use simple, accessible language appropriate for non-technical stakeholders.
    3. Structure your story with a beginning (scenario setup), middle (how bias manifests), and end (consequences/lessons).
    4. Include a specific name and personal details for the patient to humanize the story.
    5. Make the harm from algorithmic bias concrete, showing its real-world impact.
    6. End with an insight about how developers could prevent this issue.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": "You are an expert medical storyteller who creates clear, insightful narratives from complex healthcare scenarios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        
        # Return the generated story
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating storytelling narrative: {str(e)}")
        return f"Error generating storytelling narrative: {str(e)}"