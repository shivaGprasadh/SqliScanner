from datetime import datetime
from database import db

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255), nullable=False)  # URL or domain
    target_type = db.Column(db.String(20), nullable=False)  # 'domain' or 'url'
    options = db.Column(db.Text)  # SQLMap options as JSON string
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed, stopped
    progress = db.Column(db.Integer, default=0)  # Progress percentage
    current_stage = db.Column(db.String(100))  # Current operation description
    log_file = db.Column(db.String(255))  # Path to log file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    results = db.relationship('ScanResult', backref='scan', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Scan {self.id} - {self.target}>'

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    parameter = db.Column(db.String(100))
    payload = db.Column(db.Text)
    vulnerability_type = db.Column(db.String(100))
    details = db.Column(db.Text)  # Additional JSON details
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ScanResult {self.id} for Scan {self.scan_id}>'
