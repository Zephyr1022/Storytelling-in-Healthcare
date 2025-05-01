"""
Database module for the Healthcare Storytelling Platform.
Handles storing and retrieving data about scenarios, sessions, and bias identifications.
"""

import os
import json
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Initialize SQLAlchemy
Base = declarative_base()

# Define database models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    role = Column(String(50))  # researcher, healthcare_professional, student, etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    sessions = relationship("Session", back_populates="user")
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"


class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    scenario_id = Column(String(50), nullable=False)
    selected_role = Column(String(50))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    completed = Column(Boolean, default=False)
    gpt_enabled = Column(Boolean, default=False)
    user = relationship("User", back_populates="sessions")
    dialogue_entries = relationship("DialogueEntry", back_populates="session")
    decisions = relationship("Decision", back_populates="session")
    bias_identifications = relationship("BiasIdentification", back_populates="session")
    
    def __repr__(self):
        return f"<Session(scenario='{self.scenario_id}', role='{self.selected_role}')>"


class DialogueEntry(Base):
    __tablename__ = 'dialogue_entries'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    step_id = Column(String(50))
    speaker = Column(String(50))
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_gpt_generated = Column(Boolean, default=False)
    session = relationship("Session", back_populates="dialogue_entries")
    
    def __repr__(self):
        return f"<DialogueEntry(speaker='{self.speaker}', step='{self.step_id}')>"


class Decision(Base):
    __tablename__ = 'decisions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    step_id = Column(String(50))
    decision_text = Column(Text)
    next_step_id = Column(String(50))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    session = relationship("Session", back_populates="decisions")
    
    def __repr__(self):
        return f"<Decision(text='{self.decision_text}', step='{self.step_id}')>"


class BiasIdentification(Base):
    __tablename__ = 'bias_identifications'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    step_id = Column(String(50))
    bias_type = Column(String(100))
    description = Column(Text)
    is_ai_generated = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    session = relationship("Session", back_populates="bias_identifications")
    
    def __repr__(self):
        return f"<BiasIdentification(type='{self.bias_type}', step='{self.step_id}')>"


class EthicalAnalysis(Base):
    __tablename__ = 'ethical_analyses'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    bias_type = Column(String(100))
    description = Column(Text)
    potential_harm = Column(Text)
    mitigation = Column(Text)
    confidence_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<EthicalAnalysis(type='{self.bias_type}')>"


# Initialize database connection
def init_db(db_path='data/healthcare_storytelling.db'):
    """Initialize the database and create tables if they don't exist"""
    # Make sure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create database engine
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create tables
    Base.metadata.create_all(engine)
    
    # Create session factory
    Session = sessionmaker(bind=engine)
    
    return engine, Session


# Database operations
class DatabaseManager:
    """Manager class for database operations"""
    
    def __init__(self, db_path='data/healthcare_storytelling.db'):
        """Initialize database connection"""
        self.engine, self.SessionFactory = init_db(db_path)
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionFactory()
    
    def create_user(self, username, role="user"):
        """Create a new user or get existing one"""
        session = self.get_session()
        
        # Check if user exists
        user = session.query(User).filter_by(username=username).first()
        
        if not user:
            # Create new user
            user = User(username=username, role=role)
            session.add(user)
            session.commit()
        
        user_id = user.id
        session.close()
        return user_id
    
    def start_session(self, user_id, scenario_id, selected_role, gpt_enabled=False):
        """Start a new simulation session"""
        session = self.get_session()
        
        new_session = Session(
            user_id=user_id,
            scenario_id=scenario_id,
            selected_role=selected_role,
            gpt_enabled=gpt_enabled
        )
        
        session.add(new_session)
        session.commit()
        
        session_id = new_session.id
        session.close()
        return session_id
    
    def end_session(self, session_id):
        """Mark a session as completed"""
        session = self.get_session()
        
        sim_session = session.query(Session).filter_by(id=session_id).first()
        if sim_session:
            sim_session.end_time = datetime.datetime.utcnow()
            sim_session.completed = True
            session.commit()
        
        session.close()
    
    def add_dialogue_entry(self, session_id, step_id, speaker, text, is_gpt_generated=False):
        """Add a dialogue entry to the session"""
        session = self.get_session()
        
        entry = DialogueEntry(
            session_id=session_id,
            step_id=step_id,
            speaker=speaker,
            text=text,
            is_gpt_generated=is_gpt_generated
        )
        
        session.add(entry)
        session.commit()
        session.close()
    
    def add_decision(self, session_id, step_id, decision_text, next_step_id):
        """Add a decision to the session"""
        session = self.get_session()
        
        decision = Decision(
            session_id=session_id,
            step_id=step_id,
            decision_text=decision_text,
            next_step_id=next_step_id
        )
        
        session.add(decision)
        session.commit()
        session.close()
    
    def add_bias_identification(self, session_id, step_id, bias_type, description, is_ai_generated=False):
        """Add a bias identification to the session"""
        session = self.get_session()
        
        bias = BiasIdentification(
            session_id=session_id,
            step_id=step_id,
            bias_type=bias_type,
            description=description,
            is_ai_generated=is_ai_generated
        )
        
        session.add(bias)
        session.commit()
        session.close()
    
    def add_ethical_analysis(self, session_id, bias_type, description, potential_harm, mitigation, confidence_score=1.0):
        """Add an ethical analysis to the session"""
        session = self.get_session()
        
        analysis = EthicalAnalysis(
            session_id=session_id,
            bias_type=bias_type,
            description=description,
            potential_harm=potential_harm,
            mitigation=mitigation,
            confidence_score=confidence_score
        )
        
        session.add(analysis)
        session.commit()
        session.close()
    
    def get_user_sessions(self, user_id):
        """Get all sessions for a user"""
        session = self.get_session()
        
        sessions = session.query(Session).filter_by(user_id=user_id).all()
        results = [{"id": s.id, "scenario_id": s.scenario_id, "role": s.selected_role, 
                   "start_time": s.start_time, "completed": s.completed} for s in sessions]
        
        session.close()
        return results
    
    def get_session_data(self, session_id):
        """Get complete data for a session"""
        session = self.get_session()
        
        # Get session info
        sim_session = session.query(Session).filter_by(id=session_id).first()
        if not sim_session:
            session.close()
            return None
        
        # Get dialogue
        dialogue = session.query(DialogueEntry).filter_by(session_id=session_id).all()
        dialogue_data = [{"step_id": d.step_id, "speaker": d.speaker, "text": d.text, 
                         "timestamp": d.timestamp, "is_gpt_generated": d.is_gpt_generated} for d in dialogue]
        
        # Get decisions
        decisions = session.query(Decision).filter_by(session_id=session_id).all()
        decision_data = [{"step_id": d.step_id, "text": d.decision_text, 
                         "next_step": d.next_step_id, "timestamp": d.timestamp} for d in decisions]
        
        # Get bias identifications
        biases = session.query(BiasIdentification).filter_by(session_id=session_id).all()
        bias_data = [{"step_id": b.step_id, "type": b.bias_type, 
                     "description": b.description, "is_ai_generated": b.is_ai_generated} for b in biases]
        
        session_data = {
            "id": sim_session.id,
            "user_id": sim_session.user_id,
            "scenario_id": sim_session.scenario_id,
            "role": sim_session.selected_role,
            "start_time": sim_session.start_time,
            "end_time": sim_session.end_time,
            "completed": sim_session.completed,
            "gpt_enabled": sim_session.gpt_enabled,
            "dialogue": dialogue_data,
            "decisions": decision_data,
            "biases": bias_data
        }
        
        session.close()
        return session_data
    
    def export_session_data(self, session_id, output_file=None):
        """Export session data to a JSON file"""
        session_data = self.get_session_data(session_id)
        
        if not session_data:
            return False
        
        # Convert datetime objects to strings
        for key in ["start_time", "end_time"]:
            if session_data[key]:
                session_data[key] = session_data[key].isoformat()
        
        for dialogue in session_data["dialogue"]:
            dialogue["timestamp"] = dialogue["timestamp"].isoformat()
        
        for decision in session_data["decisions"]:
            decision["timestamp"] = decision["timestamp"].isoformat()
        
        # Generate output filename if not provided
        if not output_file:
            os.makedirs("data/exports", exist_ok=True)
            output_file = f"data/exports/session_{session_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return output_file


# Create instance for use throughout the application
db_manager = DatabaseManager()

# For testing
if __name__ == "__main__":
    # Test database operations
    db = DatabaseManager()
    user_id = db.create_user("test_user", "researcher")
    session_id = db.start_session(user_id, "scenario_1", "Observer", True)
    
    db.add_dialogue_entry(session_id, "start", "doctor", "Hello, how can I help you?", False)
    db.add_dialogue_entry(session_id, "start", "patient", "I've been experiencing pain.", False)
    
    db.add_decision(session_id, "start", "Ask more questions", "step_2")
    
    db.add_bias_identification(session_id, "start", "Anchoring bias", 
                             "The doctor immediately focused on the first symptom mentioned", False)
    
    print("Test data added to database.")