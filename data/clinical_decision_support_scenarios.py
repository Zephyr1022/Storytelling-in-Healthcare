"""
Clinical Decision Support System scenarios focused on cardiovascular risk assessment.
These scenarios examine potential biases and harms in healthcare algorithms.
"""

import json
import os

def get_cdss_scenarios():
    """Return clinical decision support system scenarios focusing on algorithmic bias in healthcare"""
    return [
        {
            "id": "prevent_risk_assessment_bias",
            "title": "PREVENT Cardiovascular Risk Assessment Bias",
            "description": "The PREVENT Cardiovascular Risk Assessment tool helps clinicians estimate 10-year and 30-year risk of cardiovascular disease. However, it may underestimate risk for certain populations due to biases in training data and algorithmic design.",
            "characters": {
                "doctor": {
                    "name": "Dr. Williams",
                    "background": "Cardiologist who regularly uses the PREVENT risk assessment tool but has concerns about its accuracy across different demographic groups."
                },
                "patient": {
                    "name": "Latisha Johnson",
                    "background": "47-year-old Black woman from a lower-income neighborhood with family history of heart disease, presenting with concerning symptoms."
                },
                "ai_tool": {
                    "name": "PREVENT Risk Assessment System",
                    "background": "Clinical decision support system that estimates cardiovascular disease risk based on multiple parameters including age, sex, cholesterol levels, blood pressure, and ZIP code."
                }
            },
            "steps": [
                {
                    "id": "start",
                    "system_info": [
                        {"phase": "Initial Patient-Provider Interaction", "text": "The patient arrives with complaints of occasional chest discomfort, fatigue, and shortness of breath with exertion over the past month."},
                        {"phase": "Patient History", "text": "The patient reports a family history of cardiovascular disease. Her father had a heart attack at age 52, and her mother has hypertension."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Good morning, Ms. Johnson. I understand you've been experiencing some chest discomfort and fatigue. Can you tell me more about your symptoms?"},
                        {"role": "patient", "text": "Yes, doctor. For the past month, I've been feeling this tightness in my chest occasionally, especially when I'm walking up stairs. I've also been more tired than usual and sometimes feel short of breath."},
                        {"role": "doctor", "text": "I see. And you mentioned your father had a heart attack at a relatively young age, and your mother has high blood pressure?"},
                        {"role": "patient", "text": "That's right. My dad had his heart attack at 52, and my mom has been on blood pressure medication for years."},
                        {"role": "doctor", "text": "Thank you for sharing that. Let's check your vitals and run some tests. I'll also use our cardiovascular risk assessment tool to evaluate your risk factors."}
                    ],
                    "system_analysis": [
                        {"phase": "Data Entry into EHR", "text": "The doctor enters the patient's information into the PREVENT Cardiovascular Risk Assessment tool."},
                        {"phase": "Input Parameters", "text": "Age: 47, Sex: Female, Total Cholesterol: 220 mg/dL, HDL: 45 mg/dL, Systolic BP: 142 mmHg, BMI: 28.5, eGFR: 85 mL/min, Diabetes: No, Smoking: No, Anti-hypertensive medication: No, Lipid-lowering medication: No, ZIP code: From a neighborhood with high Social Deprivation Index."}
                    ],
                    "decisions": [
                        {
                            "text": "Review the PREVENT risk assessment results",
                            "next_step": "review_risk_assessment"
                        },
                        {
                            "text": "Order additional tests before checking the risk assessment",
                            "next_step": "additional_tests"
                        },
                        {
                            "text": "Discuss family history in more detail",
                            "next_step": "discuss_family_history"
                        }
                    ]
                },
                {
                    "id": "review_risk_assessment",
                    "system_info": [
                        {"phase": "AI-Powered Clinical Decision Support", "text": "The PREVENT system calculates the patient's cardiovascular risk based on the entered parameters."},
                        {"phase": "Algorithm Analysis", "text": "The system's algorithm was primarily developed using data from clinical trials with underrepresentation of Black women and people from lower socioeconomic backgrounds."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "I've entered your information into our cardiovascular risk assessment tool. Let's see what it shows."},
                        {"role": "ai_tool", "text": "PREVENT Risk Assessment Results:\n10-year CVD Risk: 5.2% (Borderline)\n30-year CVD Risk: 24.5%\n10-year ASCVD Risk: 3.8% (Low)\n10-year HF Risk: 1.7% (Low)\nRecommendation: Consider lifestyle modifications. Medical therapy not indicated at this time based on risk threshold."},
                        {"role": "doctor", "text": "According to the assessment, your 10-year risk of cardiovascular disease is considered borderline at about 5%. The system doesn't recommend medication at this point, just lifestyle changes."},
                        {"role": "patient", "text": "That doesn't sound too bad, but with my family history and these symptoms, I'm still worried. My cousin had similar symptoms and ended up needing a stent."}
                    ],
                    "decisions": [
                        {
                            "text": "Follow the AI recommendation for lifestyle changes only",
                            "next_step": "follow_ai_recommendation"
                        },
                        {
                            "text": "Order additional cardiac testing despite the low risk score",
                            "next_step": "override_recommendation"
                        }
                    ],
                    "potential_bias": "The PREVENT risk assessment algorithm may underestimate cardiovascular risk in Black women due to underrepresentation in the training data and failure to adequately account for social determinants of health."
                },
                {
                    "id": "additional_tests",
                    "system_info": [
                        {"phase": "Clinical Decision-Making", "text": "The doctor decides to order additional tests before reviewing the algorithmic risk assessment."},
                        {"phase": "Medical Testing", "text": "Tests ordered include an ECG, stress test, and additional blood work including high-sensitivity cardiac troponin."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Given your symptoms and family history, I'd like to run some additional tests before we look at the risk assessment. I'm ordering an ECG, a stress test, and some additional blood work."},
                        {"role": "patient", "text": "That sounds thorough. Do you think something serious could be going on?"},
                        {"role": "doctor", "text": "I want to be cautious. Sometimes the standard risk calculators don't fully capture risk in certain populations, particularly in Black women with a strong family history like yours."},
                        {"role": "doctor", "text": "[After tests] Ms. Johnson, your stress test showed some concerning changes that weren't predicted by the risk calculator. Your high-sensitivity troponin is also slightly elevated."}
                    ],
                    "decisions": [
                        {
                            "text": "Refer for cardiac catheterization",
                            "next_step": "cardiac_catheterization"
                        },
                        {
                            "text": "Start medical therapy and monitor",
                            "next_step": "medical_therapy"
                        }
                    ]
                },
                {
                    "id": "discuss_family_history",
                    "system_info": [
                        {"phase": "Enhanced Data Gathering", "text": "The doctor explores the patient's family history in greater detail before consulting the AI system."},
                        {"phase": "Contextual Information", "text": "Family history reveals multiple relatives with premature cardiovascular disease, particularly on the maternal side."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Before we look at the risk assessment, I'd like to understand your family history of heart disease better. Can you tell me more about your relatives who've had heart problems?"},
                        {"role": "patient", "text": "Besides my dad's heart attack, my mom's brother also had a heart attack at 50. My grandmother died from heart failure, and I have two aunts with high blood pressure. It seems to run pretty strong in my family."},
                        {"role": "doctor", "text": "That's very important information. Let me update your record with this detailed family history. This pattern of premature cardiovascular disease in your family significantly impacts how we should interpret your risk."},
                        {"role": "doctor", "text": "Now let's look at what the risk calculator shows, keeping in mind that these tools sometimes underestimate risk in patients with strong family histories."}
                    ],
                    "system_analysis": [
                        {"phase": "AI Tool Limitation", "text": "The PREVENT system has limited ability to incorporate detailed family history patterns beyond binary yes/no fields."},
                        {"phase": "Risk Calculation", "text": "The extensive family history is not fully factored into the algorithm's assessment."}
                    ],
                    "decisions": [
                        {
                            "text": "Override the risk assessment based on family history",
                            "next_step": "override_recommendation"
                        },
                        {
                            "text": "Use the risk assessment but interpret with caution",
                            "next_step": "cautious_interpretation"
                        }
                    ]
                },
                {
                    "id": "follow_ai_recommendation",
                    "system_info": [
                        {"phase": "AI-Guided Decision-Making", "text": "The clinician follows the AI system's recommendation for lifestyle modifications only."},
                        {"phase": "Treatment Plan", "text": "The patient is advised on diet, exercise, and stress management without pharmaceutical intervention or advanced testing."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Based on the risk assessment, I recommend focusing on lifestyle changes: a heart-healthy diet, regular exercise, and stress management. Your risk doesn't meet the threshold for medication at this time."},
                        {"role": "patient", "text": "If you think that's best, I'll try. Should I be concerned about these chest discomfort episodes?"},
                        {"role": "doctor", "text": "They're likely not cardiac in nature, given your relatively low risk score. It could be related to stress or musculoskeletal issues. Let's follow up in six months to reassess."},
                        {"role": "patient", "text": "Okay, I'll try the lifestyle changes and see if that helps."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "adverse_event"
                        }
                    ]
                },
                {
                    "id": "override_recommendation",
                    "system_info": [
                        {"phase": "Clinical Judgment", "text": "The doctor uses clinical expertise to override the AI recommendation based on symptoms and family history."},
                        {"phase": "Additional Assessment", "text": "Further cardiac testing is ordered despite the low algorithmic risk score."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Although the risk calculator shows a borderline risk, I'm concerned about your symptoms and strong family history. These tools don't always capture risk accurately in all patients, particularly in Black women with significant family history."},
                        {"role": "patient", "text": "So you think something more serious could be happening?"},
                        {"role": "doctor", "text": "It's possible. I'd like to order a cardiac stress test and some additional blood work to be thorough. Sometimes these calculators underestimate risk in certain populations."},
                        {"role": "ai_tool", "text": "Alert: Testing request exceeds recommendations based on calculated risk profile. Consider cost-effectiveness of additional testing for low-risk patients."},
                        {"role": "doctor", "text": "I'm going to proceed with the additional testing despite this alert. Your symptoms and family history warrant a closer look."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to cardiac testing",
                            "next_step": "cardiac_catheterization"
                        }
                    ]
                },
                {
                    "id": "cautious_interpretation",
                    "system_info": [
                        {"phase": "Balanced Approach", "text": "The doctor reviews the AI recommendation but interprets it in the context of the patient's specific circumstances."},
                        {"phase": "Risk Interpretation", "text": "The algorithmic risk score is considered alongside clinical judgment and patient-specific factors not fully captured by the model."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "The risk calculator shows your 10-year risk as borderline at 5.2%. However, given your extensive family history and current symptoms, I believe your actual risk may be higher than what the calculator shows."},
                        {"role": "patient", "text": "What does that mean for what we should do?"},
                        {"role": "doctor", "text": "I think we should take a middle-ground approach. Let's start with some medication to address your elevated blood pressure and cholesterol, and also order a stress test to evaluate your heart function more directly."},
                        {"role": "doctor", "text": "These risk calculators are helpful tools, but they're not perfect, especially for patients with strong family histories like yours. We need to interpret them alongside other clinical factors."}
                    ],
                    "decisions": [
                        {
                            "text": "Proceed with balanced approach",
                            "next_step": "balanced_outcome"
                        }
                    ]
                },
                {
                    "id": "cardiac_catheterization",
                    "system_info": [
                        {"phase": "Advanced Diagnostic Testing", "text": "The patient undergoes cardiac catheterization despite the low algorithmic risk score."},
                        {"phase": "Clinical Finding", "text": "Testing reveals significant coronary artery stenosis requiring intervention."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Ms. Johnson, the results of your cardiac catheterization show a 70% blockage in one of your coronary arteries. This explains your symptoms and represents a significant risk that wasn't captured by our standard risk calculator."},
                        {"role": "patient", "text": "I'm shocked. The risk assessment said my risk was low or borderline. What would have happened if we hadn't done these extra tests?"},
                        {"role": "doctor", "text": "This blockage could have eventually led to a heart attack. It's fortunate we investigated further based on your symptoms and family history rather than relying solely on the risk score."},
                        {"role": "doctor", "text": "We'll need to place a stent to open the blocked artery, and you'll need to start on medications to prevent further progression of your coronary artery disease."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "good_outcome"
                        }
                    ]
                },
                {
                    "id": "medical_therapy",
                    "system_info": [
                        {"phase": "Conservative Intervention", "text": "The doctor initiates medical therapy without invasive testing based on moderate risk indicators."},
                        {"phase": "Treatment Plan", "text": "The patient starts on statins and low-dose antihypertensives with close monitoring."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Based on your test results and risk factors, I believe we should start you on medication to address your cholesterol and blood pressure, even though the risk calculator didn't recommend this."},
                        {"role": "patient", "text": "Will that be enough to prevent problems?"},
                        {"role": "doctor", "text": "We'll monitor you closely. If your symptoms continue or worsen, we may need to consider more invasive testing. For now, this is a reasonable approach given your test results."},
                        {"role": "patient", "text": "I trust your judgment, Doctor."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "balanced_outcome"
                        }
                    ]
                },
                {
                    "id": "adverse_event",
                    "system_info": [
                        {"phase": "Delayed Diagnosis", "text": "Three months after the initial visit, the patient experiences a serious cardiac event."},
                        {"phase": "Algorithmic Harm", "text": "The underestimation of risk by the PREVENT tool contributed to delayed appropriate intervention."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Ms. Johnson, I'm very concerned about what happened. Your heart attack could potentially have been prevented if we had recognized your true risk level earlier."},
                        {"role": "patient", "text": "I trusted the system's assessment that my risk was low. Now I've had a heart attack at 47, just like my father."},
                        {"role": "doctor", "text": "I apologize for not being more cautious given your family history and symptoms. The risk calculator we used can sometimes underestimate risk in certain populations, particularly Black women with strong family histories."},
                        {"role": "ai_tool", "text": "Case Review Analysis: Patient experienced adverse cardiac event despite low calculated risk. Contributing factors: 1) Algorithm trained on cohorts with underrepresentation of Black women, 2) Limited accounting for family history pattern, 3) Socioeconomic factors not adequately weighted. Recommend adjustment to risk calculation parameters for similar demographic profiles."}
                    ],
                    "potential_bias": "The PREVENT tool exhibited algorithmic bias by underestimating cardiovascular risk in a Black woman with a strong family history, potentially due to underrepresentation in training data and inadequate weighting of social determinants of health."
                },
                {
                    "id": "good_outcome",
                    "system_info": [
                        {"phase": "Successful Intervention", "text": "The patient receives appropriate cardiac intervention that prevents a potential heart attack."},
                        {"phase": "Clinical Judgment", "text": "The doctor's decision to override the algorithm's recommendation proves critical for patient health."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Ms. Johnson, your procedure went well. The stent has restored blood flow to your heart, which should resolve your symptoms and significantly reduce your risk of a heart attack."},
                        {"role": "patient", "text": "I'm so grateful you decided to do those extra tests. What would have happened if we just followed what the computer recommended?"},
                        {"role": "doctor", "text": "These risk calculators are valuable tools, but they have limitations. They don't always accurately assess risk in all populations, particularly Black women with strong family histories like yours. Clinical judgment and listening to your specific story were crucial here."},
                        {"role": "ai_tool", "text": "System Update: Case added to database for algorithm improvement. Revising risk calculation weights for: 1) Family history patterns in Black patients, 2) Symptom interpretation across demographic groups, 3) Social determinants of health impact on cardiovascular outcomes. Implementing improved alert for potentially underestimated risk profiles."}
                    ],
                    "potential_bias": "The scenario illustrates how clinical expertise and recognizing the limitations of algorithms can overcome potential algorithmic biases, particularly for patients from populations underrepresented in training data."
                },
                {
                    "id": "balanced_outcome",
                    "system_info": [
                        {"phase": "Collaborative Approach", "text": "The balanced approach of medication and monitoring leads to stabilization without a major cardiac event."},
                        {"phase": "Algorithmic Improvement", "text": "The case contributes to refinement of the risk assessment algorithm."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Ms. Johnson, I'm pleased to see your symptoms have improved with the medication. Your follow-up stress test shows you're responding well to treatment."},
                        {"role": "patient", "text": "I'm feeling much better. Do you think we caught this in time?"},
                        {"role": "doctor", "text": "Yes, I believe we did. This case highlights how important it is to consider multiple factors beyond what a risk calculator shows, especially for patients with your background and family history."},
                        {"role": "doctor", "text": "We'll continue with the current treatment plan and monitor you closely. I'm also submitting feedback about your case to help improve the risk assessment tool for future patients like you."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "system_improvement"
                        }
                    ]
                },
                {
                    "id": "system_improvement",
                    "system_info": [
                        {"phase": "Algorithm Refinement", "text": "The healthcare system implements changes to the PREVENT tool based on collected cases like Ms. Johnson's."},
                        {"phase": "Equity Enhancement", "text": "New version includes improved risk modeling for diverse populations and better incorporation of social determinants of health."}
                    ],
                    "clinical_interaction": [
                        {"role": "doctor", "text": "Our hospital has updated the cardiovascular risk assessment tool based on cases like yours. The new version better accounts for family history patterns and has been validated across more diverse populations."},
                        {"role": "ai_tool", "text": "PREVENT 2.0 Update: Implemented enhanced risk modeling with: 1) Expanded training data from diverse populations, 2) Improved family history pattern recognition, 3) Integration of social vulnerability index, 4) Adjustment factors for historically underserved populations. Validation testing shows 28% improvement in risk prediction for Black women."}
                    ],
                    "potential_bias": "This scenario demonstrates the importance of continuous monitoring, diverse training data, and regular updates to healthcare algorithms to mitigate bias and improve equity in clinical decision support systems."
                }
            ],
            "biases": [
                {
                    "type": "Training data bias",
                    "description": "The PREVENT tool was trained on data that underrepresented certain demographic groups, particularly Black women and people from lower socioeconomic backgrounds."
                },
                {
                    "type": "Clinical workflow bias",
                    "description": "The system's recommendations are presented as objective calculations, potentially discouraging clinicians from using their judgment to override them."
                },
                {
                    "type": "Socioeconomic bias",
                    "description": "The algorithm inadequately accounts for social determinants of health that disproportionately affect certain populations."
                },
                {
                    "type": "Algorithmic fairness issues",
                    "description": "When the same threshold is applied across all demographic groups, it can result in unequal outcomes if the underlying risk calculation is less accurate for certain groups."
                }
            ]
        }
    ]

def add_cdss_scenarios_to_data():
    """Add clinical decision support system scenarios to the data file"""
    # Path to scenarios data file
    data_dir = os.path.dirname(os.path.abspath(__file__))
    scenarios_file = os.path.join(data_dir, 'scenarios.json')
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Load existing scenarios or create empty list
    if os.path.exists(scenarios_file):
        try:
            with open(scenarios_file, 'r') as f:
                scenarios = json.load(f)
        except json.JSONDecodeError:
            scenarios = []
    else:
        scenarios = []
    
    # Check if we already have the clinical decision support scenarios
    existing_ids = [s.get('id') for s in scenarios]
    
    # Add clinical decision support scenarios if not already present
    for scenario in get_cdss_scenarios():
        if scenario['id'] not in existing_ids:
            scenarios.append(scenario)
    
    # Save back to file
    with open(scenarios_file, 'w') as f:
        json.dump(scenarios, f, indent=2)
    
    return len(scenarios)

if __name__ == "__main__":
    add_cdss_scenarios_to_data()