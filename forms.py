from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, NumberRange, ValidationError
import re

def validate_domain_or_url(form, field):
    """Validates that input is either a valid domain or URL based on target_type selection"""
    target_type = form.target_type.data
    value = field.data
    
    if target_type == 'domain':
        # Basic domain validation
        domain_pattern = re.compile(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')
        if not domain_pattern.match(value):
            raise ValidationError('Invalid domain format. Example: example.com')
    elif target_type == 'url':
        # URL validation
        url_pattern = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ipv4
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_pattern.match(value):
            raise ValidationError('Invalid URL format. Example: https://example.com/page')

class ScanForm(FlaskForm):
    target_type = SelectField('Target Type', choices=[
        ('url', 'Specific URL'), 
        ('domain', 'Domain (Crawl and Scan)')
    ], validators=[DataRequired()])
    target = StringField('Target', validators=[DataRequired(), validate_domain_or_url])
    
    # Basic options
    crawl = IntegerField('Crawl Depth (--crawl)', validators=[Optional(), NumberRange(min=1, max=10)])
    forms = BooleanField('Test Forms (--forms)')
    
    # Enumeration options
    dbs = BooleanField('Enumerate DBs (--dbs)')
    tables = BooleanField('Enumerate Tables (--tables)')
    columns = BooleanField('Enumerate Columns (--columns)')
    
    # Detection options
    level = IntegerField('Detection level (--level)', validators=[Optional(), NumberRange(min=1, max=5)], default=1)
    risk = IntegerField('Risk level (--risk)', validators=[Optional(), NumberRange(min=1, max=3)], default=1)
    
    # Request options
    data = TextAreaField('HTTP POST data (--data)')
    cookie = StringField('Cookie (--cookie)')
    user_agent = StringField('User-Agent (--user-agent)')
    
    # Injection options
    technique = StringField('SQL Injection Techniques (--technique) B,E,U,S,T,Q')
    tamper = StringField('Tamper Scripts (--tamper)')
    
    # Advanced options
    threads = IntegerField('Threads (--threads)', validators=[Optional(), NumberRange(min=1, max=10)], default=1)
    time_sec = IntegerField('Time delay seconds (--time-sec)', validators=[Optional(), NumberRange(min=1)]) 
    timeout = IntegerField('Timeout (--timeout)', validators=[Optional(), NumberRange(min=1)])
    batch = BooleanField('Batch mode (--batch)', default=True)
    random_agent = BooleanField('Random User-Agent (--random-agent)')
    dump = BooleanField('Dump database data (--dump)')
    os_shell = BooleanField('Get OS shell if possible (--os-shell)')
    is_dba = BooleanField('Check for DBA privileges (--is-dba)')
    identifiers = BooleanField('Enumerate DBMS users/passwords (--users --passwords)')
    all = BooleanField('Test all features (--all)')
    
    submit = SubmitField('Start Scan')
