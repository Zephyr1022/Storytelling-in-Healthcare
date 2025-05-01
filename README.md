# Storytelling-in-Healthcare

Speculative Stories in Healthcare is an interactive agentic application that uses large language models to simulate clinical scenarios and uncover bias in AI-driven medical decision-making. Users step into the role of an observer, while AI agents play the doctor, patient, and clinical decision support system. Through dynamic storytelling, users witness how factors like race, gender, and age can influence AI recommendations and clinical outcomes—revealing the ethical risks hidden in everyday healthcare technology.

Built with Streamlit and powered by GPT-4, this tool applies speculative design to humanize algorithmic harms and make fairness training more intuitive. By turning abstract concerns into emotionally engaging narratives, it empowers clinicians, developers, and students to recognize the real-world impact of AI bias—and to reflect on how to build more inclusive, equitable health systems.

# Healthcare Storytelling Platform

## Overview
An advanced storytelling platform that critically examines algorithmic bias in healthcare decision-making through interactive, role-playing scenarios. The platform simulates complex medical interactions, revealing potential systemic biases in clinical decision support systems.

## Features

### Interactive Simulation
- **Role Selection**: Choose from doctor, patient, AI tool, or observer perspectives
- **Dynamic Scenarios**: Experience realistic clinical situations with algorithmic decision support
- **Character Profiles**: Select from pre-built characters or create custom ones with unique backgrounds
- **Decision Trees**: Navigate through complex medical decision pathways

### Bias Analysis
- **Automated Detection**: AI-powered identification of potential biases in interactions
- **Manual Flagging**: User-driven bias identification during simulations
- **Categorization**: Classification of different types of algorithmic and human biases
- **Ethical Analysis**: Assessment of potential harms and mitigation strategies

### Storytelling
- **Narrative Generation**: AI-powered creation of 15-sentence stories based on scenario interactions
- **Simplified Understanding**: Translation of complex technical biases into accessible narratives
- **Developer Focus**: Helps anticipate potential harms before implementation
- **Shareable Format**: Copy and regenerate stories for team discussions

### Analytics Dashboard
- **Session Tracking**: Monitor user engagement across scenarios
- **Bias Patterns**: Visualize commonly identified biases
- **Decision Analysis**: Track pathway choices and outcomes
- **Data Export**: Save session data for further analysis

## Technical Stack
- **Backend**: Python with Streamlit for interactive web interface
- **AI Integration**: OpenAI API (GPT-4o) for dynamic responses and analysis
- **Data Storage**: SQLite database via SQLAlchemy
- **Visualization**: Matplotlib and NetworkX for analytics and decision trees

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository
   ```
   git clone https://github.com/zephyr1022/Zephyr1022/Storytelling-in-Healthcare.git
   cd healthcare-storytelling-platform
   ```

2. Install required packages
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables
   ```
   # Create a .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. Run the application
   ```
   streamlit run app.py
   ```

## Usage Guide

### 1. Select a Scenario
Choose from available clinical scenarios in the sidebar, each focusing on a different potential bias in healthcare algorithms.

### 2. Choose Your Role
Decide whether to experience the scenario as a doctor, patient, AI tool, or external observer.

### 3. Select or Create a Character
Pick a pre-defined character or create your own with unique background, perspective, and bias tendencies.

### 4. Navigate the Simulation
Progress through the scenario by making decisions and observing how the AI clinical decision support system influences the interaction.

### 5. Identify Biases
Flag potential biases as you notice them, or review the AI-generated bias analysis at the end of the simulation.

### 6. Generate a Story
After completing the simulation, generate a 15-sentence narrative that explains the potential harms in an accessible way.

### 7. Analyze Data
Visit the Analytics Dashboard to explore patterns across multiple simulation sessions.

## Educational Value

This platform serves as a valuable educational tool for:

- **Healthcare AI Developers**: Anticipate potential biases before implementation
- **Medical Professionals**: Understand how to critically evaluate algorithmic recommendations
- **Ethics Researchers**: Study patterns of bias in clinical decision support systems
- **Students**: Learn about the intersection of technology, ethics, and healthcare

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

- This tool was developed to address the growing concern about algorithmic bias in healthcare
- Special thanks to the healthcare professionals and ethicists who contributed scenario content
