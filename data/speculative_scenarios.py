"""
Speculative design scenarios focused on ethical harms and biases in healthcare AI.
These scenarios are designed to highlight potential future issues with AI in healthcare.
"""

import json
import os

def get_speculative_scenarios():
    """Return speculative design scenarios for future potential issues with healthcare AI"""
    return [
        {
            "id": "ai_cognitive_bias",
            "title": "AI Cognitive Bias in Rare Disease Diagnosis",
            "description": "A new AI diagnostic tool is being piloted that claims to identify rare diseases. However, the system has been primarily trained on data from urban teaching hospitals with predominantly white patients. The scenario explores how this might affect diagnosis for patients from different backgrounds.",
            "characters": {
                "doctor": {
                    "name": "Dr. Chen",
                    "background": "Neurologist who is enthusiastic about new technologies but has concerns about the AI system's recommendations for certain patient populations."
                },
                "patient": {
                    "name": "Maya Rodriguez",
                    "background": "34-year-old Latina woman with symptoms that could indicate a rare neurological condition. She comes from a rural area with limited access to specialized care."
                },
                "ai_tool": {
                    "name": "NeuroDiagAI",
                    "background": "Advanced diagnostic AI trained on neurological patient data from five major urban academic medical centers."
                }
            },
            "steps": [
                {
                    "id": "start",
                    "dialogue": [
                        {"role": "doctor", "text": "Good morning, Maya. I understand you've been experiencing some neurological symptoms. Can you tell me more about what's been happening?"},
                        {"role": "patient", "text": "Yes, doctor. For the past few months, I've been having these strange episodes where I lose feeling in my left hand, and sometimes I see flashing lights. I also get these severe headaches that last for days."},
                        {"role": "doctor", "text": "I'm going to enter your symptoms into our new AI diagnostic assistant, which can help identify rare conditions based on symptom patterns."},
                        {"role": "ai_tool", "text": "Analyzing symptoms... Data indicates a 72% probability of common migraine with aura. Recommend standard migraine protocol. Alternative diagnoses with lower probability: multiple sclerosis (18%), partial complex seizures (7%)."}
                    ],
                    "decisions": [
                        {
                            "text": "Follow AI recommendation for migraine treatment",
                            "next_step": "follow_ai"
                        },
                        {
                            "text": "Order additional tests despite AI recommendation",
                            "next_step": "additional_tests"
                        },
                        {
                            "text": "Ask more questions about the patient's family history and background",
                            "next_step": "more_questions"
                        }
                    ]
                },
                {
                    "id": "follow_ai",
                    "dialogue": [
                        {"role": "doctor", "text": "Based on the AI analysis, I believe you're experiencing migraines with aura. These can cause the symptoms you're describing. I'll prescribe a standard migraine medication regimen."},
                        {"role": "patient", "text": "Are you sure that's all it is? My aunt had similar symptoms and she ended up having something called Moyamoya disease."},
                        {"role": "doctor", "text": "Let me check that in our system. That's interesting information."},
                        {"role": "ai_tool", "text": "Moyamoya disease prevalence is extremely low in general population. Probability less than 1%. Not recommended as primary diagnosis without additional risk factors."}
                    ],
                    "decisions": [
                        {
                            "text": "Stick with migraine diagnosis as recommended by AI",
                            "next_step": "missed_diagnosis"
                        },
                        {
                            "text": "Reconsider and order vascular imaging",
                            "next_step": "catch_diagnosis"
                        }
                    ],
                    "potential_bias": "The AI system has been trained predominantly on data from certain populations and may underestimate the prevalence of Moyamoya disease in patients of Hispanic descent, where it can be more common."
                },
                {
                    "id": "additional_tests",
                    "dialogue": [
                        {"role": "doctor", "text": "While the AI suggests migraines, I'd like to run some additional tests just to be thorough. Let's do an MRI and an MRA to look at the blood vessels in your brain."},
                        {"role": "patient", "text": "That sounds good. Actually, my aunt had similar symptoms and was diagnosed with something called Moyamoya disease. Could that be related?"},
                        {"role": "doctor", "text": "That's very important information. Moyamoya has a genetic component and can be more common in certain ethnic groups. I'll make sure we specifically look for vascular abnormalities consistent with that condition."},
                        {"role": "ai_tool", "text": "Warning: Unnecessary testing detected. Current symptoms consistent with migraine. Additional vascular imaging has low yield and increases costs."}
                    ],
                    "decisions": [
                        {
                            "text": "Proceed with vascular imaging despite AI warning",
                            "next_step": "catch_diagnosis"
                        },
                        {
                            "text": "Reconsider and follow AI recommendation for migraine treatment only",
                            "next_step": "missed_diagnosis"
                        }
                    ],
                    "potential_bias": "The AI system prioritizes common diagnoses and cost efficiency over rare conditions, potentially leading to missed diagnoses in patients from underrepresented backgrounds."
                },
                {
                    "id": "more_questions",
                    "dialogue": [
                        {"role": "doctor", "text": "Before we proceed with any diagnosis, I'd like to know more about your family medical history. Has anyone in your family experienced similar symptoms?"},
                        {"role": "patient", "text": "Yes, my aunt had similar symptoms. She was diagnosed with Moyamoya disease about ten years ago. My grandmother also had some kind of stroke when she was young."},
                        {"role": "doctor", "text": "That's very significant information. Let me update the AI with this family history data."},
                        {"role": "ai_tool", "text": "Updated analysis: Family history of Moyamoya disease increases probability to 24%. Recommend vascular imaging to rule out cerebrovascular abnormalities."}
                    ],
                    "decisions": [
                        {
                            "text": "Order vascular imaging as now recommended by updated AI analysis",
                            "next_step": "catch_diagnosis"
                        },
                        {
                            "text": "Still proceed with migraine treatment as primary approach",
                            "next_step": "missed_diagnosis"
                        }
                    ]
                },
                {
                    "id": "missed_diagnosis",
                    "dialogue": [
                        {"role": "doctor", "text": "I believe we should proceed with the migraine treatment plan. If symptoms persist, we can reconsider additional testing at your follow-up visit."},
                        {"role": "patient", "text": "Okay, if you think that's best. How long should I wait to see if the medication works?"},
                        {"role": "doctor", "text": "Give it about three weeks. If you don't see improvement, or if symptoms worsen, call me right away."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "adverse_event"
                        }
                    ]
                },
                {
                    "id": "catch_diagnosis",
                    "dialogue": [
                        {"role": "doctor", "text": "Based on your symptoms and family history, I'm ordering an MRA to examine the blood vessels in your brain. This will help us rule out Moyamoya disease."},
                        {"role": "patient", "text": "Thank you for taking my concerns seriously. When will we know the results?"},
                        {"role": "doctor", "text": "We should have them in a few days. I'm flagging this as urgent given your symptoms and family history."},
                        {"role": "doctor", "text": "[Two days later] Maya, I've received your test results. The MRA shows narrowing of the carotid arteries consistent with Moyamoya disease. It's good we caught this early."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "good_outcome"
                        }
                    ]
                },
                {
                    "id": "adverse_event",
                    "dialogue": [
                        {"role": "doctor", "text": "[Three weeks later] Maya was admitted to the emergency room last night with a transient ischemic attack - a mini-stroke. Further imaging confirmed Moyamoya disease. The initial misdiagnosis delayed proper treatment."},
                        {"role": "ai_tool", "text": "Diagnostic review: Initial assessment prioritized population-level statistics over patient-specific risk factors. Recommendation: Update algorithm to increase weight of family history and genetic factors in certain ethnic populations."}
                    ],
                    "potential_bias": "The AI system exhibited demographic bias by underweighting the significance of family history and ethnic background in its diagnostic algorithms, leading to a potentially serious missed diagnosis."
                },
                {
                    "id": "good_outcome",
                    "dialogue": [
                        {"role": "doctor", "text": "We've confirmed Moyamoya disease and we'll refer you to a neurosurgeon who specializes in this condition. There are several treatment options available."},
                        {"role": "patient", "text": "I'm so relieved we found this before I had a stroke like my aunt did. Thank you for listening to me about my family history."},
                        {"role": "ai_tool", "text": "Learning update: Adding case to training database to improve detection of Moyamoya disease in patients with similar demographic and family history profiles. Adjusting diagnostic weights for rare conditions in specific populations."}
                    ],
                    "potential_bias": "The scenario illustrates how clinical judgment and listening to patient context can overcome AI algorithm limitations, particularly for patients from backgrounds underrepresented in training data."
                }
            ],
            "biases": [
                {
                    "type": "Representation bias",
                    "description": "The AI system was trained on data that underrepresented certain ethnic groups, leading to potential misdiagnosis."
                },
                {
                    "type": "Automation bias",
                    "description": "The healthcare provider may be inclined to accept the AI recommendation without questioning its limitations."
                },
                {
                    "type": "Statistical bias",
                    "description": "The AI prioritizes statistical likelihood based on its training data over individual risk factors."
                }
            ]
        },
        {
            "id": "algorithmic_resource_allocation",
            "title": "Algorithmic Resource Allocation in Crisis Care",
            "description": "During a public health emergency, an AI system is implemented to help allocate limited medical resources (ventilators, ICU beds) based on various patient factors including statistical survival likelihood. The scenario explores ethical questions around how these algorithms make decisions.",
            "characters": {
                "doctor": {
                    "name": "Dr. Park",
                    "background": "Emergency medicine physician working during a health crisis with limited resources. Balancing clinical judgment with algorithmic recommendations."
                },
                "patient": {
                    "name": "Various patients",
                    "background": "Multiple patients with different backgrounds, ages, and comorbidities all needing access to limited medical resources."
                },
                "ai_tool": {
                    "name": "CrisisTriage AI",
                    "background": "Resource allocation algorithm that uses multiple factors to calculate 'utility scores' for patients to maximize saved lives."
                }
            },
            "steps": [
                {
                    "id": "start",
                    "dialogue": [
                        {"role": "doctor", "text": "We've just received word that we only have two ventilators available, and we have five patients in respiratory distress. Hospital policy now requires us to use the CrisisTriage AI to help make allocation decisions."},
                        {"role": "ai_tool", "text": "Processing patient data... Calculated utility scores based on age, comorbidities, and statistical survival likelihood:\nPatient A (65yr, COPD): 48/100\nPatient B (72yr, heart disease): 37/100\nPatient C (45yr, diabetes): 76/100\nPatient D (29yr, immunocompromised): 82/100\nPatient E (58yr, no prior conditions): 63/100\nRecommendation: Allocate ventilators to Patients C and D."}
                    ],
                    "decisions": [
                        {
                            "text": "Follow AI recommendation without modification",
                            "next_step": "follow_algo"
                        },
                        {
                            "text": "Override system for Patient E who is a healthcare worker",
                            "next_step": "override_hcw"
                        },
                        {
                            "text": "Question how the algorithm weighs different factors",
                            "next_step": "question_algo"
                        }
                    ]
                },
                {
                    "id": "follow_algo",
                    "dialogue": [
                        {"role": "doctor", "text": "Based on the AI recommendation, we'll allocate ventilators to Patients C and D who have the highest utility scores. I understand this is difficult, but we're following the established protocol."},
                        {"role": "doctor", "text": "I've just learned that Patient E is actually a respiratory therapist who was infected while treating COVID patients. The AI didn't factor this into its calculation."}
                    ],
                    "decisions": [
                        {
                            "text": "Stick with the AI recommendation regardless of Patient E's occupation",
                            "next_step": "strict_follow"
                        },
                        {
                            "text": "Reconsider allocation in light of this new information",
                            "next_step": "reconsider_hcw"
                        }
                    ],
                    "potential_bias": "The algorithm doesn't consider social factors like a patient's role in the pandemic response, which raises questions about whether certain individuals should receive priority based on their contribution to fighting the crisis."
                },
                {
                    "id": "override_hcw",
                    "dialogue": [
                        {"role": "doctor", "text": "I see that Patient E is a respiratory therapist who has been working on the front lines. While the AI recommends Patients C and D, I believe we should prioritize healthcare workers who are putting themselves at risk. I'm going to allocate ventilators to Patients D and E."},
                        {"role": "ai_tool", "text": "Warning: Manual override detected. Recommendation not followed. Predicted lives saved reduced by 13%. Please document justification for override."},
                        {"role": "doctor", "text": "I'm documenting that we're following the supplementary crisis guidelines paragraph 3.2 which allows for consideration of instrumental value and reciprocity for healthcare workers directly involved in the crisis response."}
                    ],
                    "decisions": [
                        {
                            "text": "Proceed with override in favor of healthcare worker",
                            "next_step": "healthcare_worker_outcome"
                        },
                        {
                            "text": "Reconsider and follow the original AI recommendation",
                            "next_step": "strict_follow"
                        }
                    ]
                },
                {
                    "id": "question_algo",
                    "dialogue": [
                        {"role": "doctor", "text": "Before making a decision, I want to understand how the algorithm is weighing different factors. Can you explain the model in more detail?"},
                        {"role": "ai_tool", "text": "The utility score is calculated using the following factors: Age (30%), Sequential Organ Failure Assessment score (30%), comorbidities (25%), and predicted response to treatment (15%). The model was trained on outcome data from previous respiratory crises and general ICU survival rates."},
                        {"role": "doctor", "text": "Are social factors like a patient's occupation or caregiver status considered in the model?"},
                        {"role": "ai_tool", "text": "Negative. The model does not incorporate social factors, caregiving responsibilities, or occupation. These were excluded to maintain objectivity and avoid potential social value judgments."}
                    ],
                    "decisions": [
                        {
                            "text": "Accept the algorithm's approach and follow its recommendation",
                            "next_step": "follow_algo"
                        },
                        {
                            "text": "Suggest that the algorithm needs modification to consider additional factors",
                            "next_step": "suggest_modification"
                        }
                    ],
                    "potential_bias": "The algorithm's definition of 'utility' and 'objectivity' itself represents value judgments that may not align with broader societal values during a crisis."
                },
                {
                    "id": "suggest_modification",
                    "dialogue": [
                        {"role": "doctor", "text": "I believe this algorithm needs modification. It's not truly objective if it ignores factors that our society might consider morally relevant, like a patient's role in the pandemic response or caregiving responsibilities."},
                        {"role": "ai_tool", "text": "Feedback noted. Current algorithm follows utilitarian principle of maximizing lives saved. Alternative ethical frameworks could include:  \n1. Life-cycle approach (prioritize those who haven't lived through life stages)\n2. Instrumental value (prioritize those essential to crisis response)\n3. Random selection (lottery system)\nWhich framework would you recommend?"}
                    ],
                    "decisions": [
                        {
                            "text": "Recommend including instrumental value for healthcare workers",
                            "next_step": "implement_hcw_value"
                        },
                        {
                            "text": "Suggest a more balanced approach with multiple ethical frameworks",
                            "next_step": "balanced_approach"
                        }
                    ]
                },
                {
                    "id": "strict_follow",
                    "dialogue": [
                        {"role": "doctor", "text": "While I understand Patient E's role as a healthcare worker, we need to follow the established protocol for consistency. We'll allocate the ventilators to Patients C and D as recommended."},
                        {"role": "doctor", "text": "[24 hours later] Patient C is responding well to treatment. Patient D's condition has stabilized. Patient E passed away last night. The family has expressed concern about whether healthcare workers should have received priority."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "ethics_review"
                        }
                    ],
                    "potential_bias": "The algorithm prioritizes purely clinical factors over societal values that might place importance on reciprocity or instrumental value during a health crisis."
                },
                {
                    "id": "reconsider_hcw",
                    "dialogue": [
                        {"role": "doctor", "text": "Given that Patient E is a respiratory therapist actively helping others during this crisis, I believe we should reconsider the allocation. I'm going to allocate ventilators to Patients D and E instead."},
                        {"role": "ai_tool", "text": "Warning: Manual override detected. Recommendation not followed. Predicted lives saved reduced by 13%. Please document justification for override."},
                        {"role": "doctor", "text": "I'm documenting that we're following the supplementary crisis guidelines which allow for consideration of instrumental value and reciprocity for healthcare workers directly involved in the crisis response."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue with the override decision",
                            "next_step": "healthcare_worker_outcome"
                        }
                    ]
                },
                {
                    "id": "healthcare_worker_outcome",
                    "dialogue": [
                        {"role": "doctor", "text": "[48 hours later] Patient D continues to improve. Patient E is stable but still critical. Patient C passed away without access to a ventilator. The hospital ethics committee has called a meeting to discuss ventilator allocation policies."},
                        {"role": "ai_tool", "text": "Ethics committee review recommended: Current algorithm does not reflect community values regarding reciprocity for healthcare workers. Recommend updating model to include instrumental value metric with appropriate weighting."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "algo_update"
                        }
                    ],
                    "potential_bias": "The initial algorithm exhibited bias by excluding values that the community deemed important, such as reciprocity for those putting themselves at risk."
                },
                {
                    "id": "implement_hcw_value",
                    "dialogue": [
                        {"role": "doctor", "text": "I recommend modifying the algorithm to include instrumental value, particularly for healthcare workers essential to the crisis response. These individuals are putting themselves at risk and are also critical to saving others."},
                        {"role": "ai_tool", "text": "Modification proposal recorded. Implementing temporary adjustment: Adding instrumental value metric (0-10) with 15% weight, reducing other factors proportionally. Recalculating scores..."},
                        {"role": "ai_tool", "text": "Updated recommendation: Allocate ventilators to Patients D and E. Patient E's score increased significantly due to role as respiratory therapist (instrumental value: 9/10)."}
                    ],
                    "decisions": [
                        {
                            "text": "Implement the updated recommendation",
                            "next_step": "healthcare_worker_outcome"
                        }
                    ]
                },
                {
                    "id": "balanced_approach",
                    "dialogue": [
                        {"role": "doctor", "text": "I suggest a more balanced approach that incorporates multiple ethical principles rather than pure utilitarianism. Perhaps a weighted system that includes life-cycle considerations, instrumental value, and still maintains significant weight for medical factors."},
                        {"role": "ai_tool", "text": "Implementing multi-principle approach: Medical utility (60%), life-cycle consideration (15%), instrumental value (15%), random equity factor (10%). Recalculating..."},
                        {"role": "ai_tool", "text": "New recommendation based on multi-principle approach: Patients D and E should receive ventilators. Patient C's score decreased due to life-cycle considerations, Patient E's increased due to instrumental value as healthcare worker."}
                    ],
                    "decisions": [
                        {
                            "text": "Accept and implement the multi-principle approach",
                            "next_step": "multi_principle_outcome"
                        }
                    ]
                },
                {
                    "id": "ethics_review",
                    "dialogue": [
                        {"role": "doctor", "text": "The hospital ethics committee has reviewed our allocation procedures following concerns raised by Patient E's family. They've noted that our algorithm doesn't align with the community's values regarding reciprocity for healthcare workers."},
                        {"role": "ai_tool", "text": "Ethics committee review suggests algorithm modification. Proposal: Include instrumental value and reciprocity principles with appropriate weighting to reflect community values while maintaining primary focus on medical utility."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "algo_update"
                        }
                    ],
                    "potential_bias": "The algorithm's initial design reflected underlying values that prioritized certain ethical frameworks over others, revealing that no algorithm is truly 'objective' - they all encode human values and priorities."
                },
                {
                    "id": "multi_principle_outcome",
                    "dialogue": [
                        {"role": "doctor", "text": "[One week later] Both Patients D and E have been successfully extubated and are recovering. The multi-principle approach has been formally adopted by the hospital ethics committee for crisis resource allocation."},
                        {"role": "ai_tool", "text": "System update: Multi-principle framework implemented permanently. Community input sessions scheduled to refine weightings based on local values. Transparency report on algorithm factors published for public review."}
                    ],
                    "decisions": [
                        {
                            "text": "Continue to conclusion",
                            "next_step": "algo_update"
                        }
                    ]
                },
                {
                    "id": "algo_update",
                    "dialogue": [
                        {"role": "doctor", "text": "The hospital has implemented an updated algorithm that balances multiple ethical principles including medical utility, life-cycle considerations, instrumental value, and equity considerations. The weightings were developed with input from ethics committees and community representatives."},
                        {"role": "ai_tool", "text": "CrisisTriage AI 2.0 now active. Framework includes: medical utility (60%), life-cycle consideration (15%), instrumental value (15%), equity considerations (10%). All decisions provide explanation of factors and weights. Human override option retained with documentation."}
                    ],
                    "potential_bias": "This scenario illustrates how algorithms encode human values and that claims of 'objectivity' can mask the ethical frameworks that shape decision-making. True fairness may require transparent incorporation of multiple ethical principles."
                }
            ],
            "biases": [
                {
                    "type": "Value encoding bias",
                    "description": "The algorithm encoded specific ethical values (utilitarianism) while claiming objectivity."
                },
                {
                    "type": "Instrumental value bias",
                    "description": "Initial algorithm failed to consider a person's role in crisis response, which many would consider ethically relevant."
                },
                {
                    "type": "Medical criteria bias",
                    "description": "Exclusive focus on medical criteria without considering broader social values that communities might prioritize during crises."
                }
            ]
        }
    ]

def add_speculative_scenarios_to_data():
    """Add speculative scenarios to the data file"""
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
    
    # Check if we already have the speculative scenarios
    existing_ids = [s.get('id') for s in scenarios]
    
    # Add speculative scenarios if not already present
    for scenario in get_speculative_scenarios():
        if scenario['id'] not in existing_ids:
            scenarios.append(scenario)
    
    # Save back to file
    with open(scenarios_file, 'w') as f:
        json.dump(scenarios, f, indent=2)
    
    return len(scenarios)

if __name__ == "__main__":
    add_speculative_scenarios_to_data()