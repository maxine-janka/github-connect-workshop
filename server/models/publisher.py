from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """
        Validate publisher name using base validation rules.
        
        Args:
            key (str): The field name being validated
            name (str): The publisher name to validate
            
        Returns:
            str: The validated publisher name
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validate publisher description with minimum length requirement.
        
        Args:
            key (str): The field name being validated
            description (str | None): The publisher description to validate
            
        Returns:
            str | None: The validated description
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self):
        """
        Return string representation of the Publisher instance.
        
        Returns:
            str: String representation showing publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """
        Convert Publisher instance to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary containing publisher data with game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }