import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.middleware.proxy_fix import ProxyFix
from forms import ScanForm
from utils.sqlmap_manager import SQLMapManager
from database import db, configure_db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
configure_db(app)

# Initialize SQLMap manager
sqlmap_manager = SQLMapManager()

# Import models after app creation to avoid circular imports
from models import Scan, ScanResult

with app.app_context():
    # Create all tables if they don't exist
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ScanForm()
    if form.validate_on_submit():
        # Create a new scan
        target_type = form.target_type.data
        target = form.target.data
        options = {}
        
        # Collect SQLMap options from the form
        for field in form:
            if field.name not in ['csrf_token', 'target', 'target_type', 'submit']:
                if field.data:
                    # Convert field name from form_field_name to form-field-name for SQLMap
                    sqlmap_option = field.name.replace('_', '-')
                    options[sqlmap_option] = field.data

        # Create scan record in database
        new_scan = Scan()
        new_scan.target = target
        new_scan.target_type = target_type
        new_scan.options = str(options)
        new_scan.status = "pending"
        new_scan.created_at = datetime.utcnow()
        db.session.add(new_scan)
        db.session.flush()  # Get the ID without committing
        
        # Start the scan in a separate thread
        sqlmap_manager.start_scan(new_scan.id, target, target_type, options)
        
        db.session.commit()
        flash('Scan started successfully!', 'success')
        return redirect(url_for('results', scan_id=new_scan.id))
    
    return render_template('index.html', form=form)

@app.route('/results')
def results_list():
    scans = Scan.query.order_by(Scan.created_at.desc()).all()
    return render_template('results.html', scans=scans)

@app.route('/results/<int:scan_id>')
def results(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    return render_template('results.html', scan=scan)

@app.route('/api/scan_status/<int:scan_id>')
def scan_status(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    return jsonify({
        'id': scan.id,
        'status': scan.status,
        'progress': scan.progress,
        'current_stage': scan.current_stage
    })

@app.route('/api/scan_results/<int:scan_id>')
def scan_results(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    results = ScanResult.query.filter_by(scan_id=scan_id).all()
    
    results_list = []
    for result in results:
        results_list.append({
            'id': result.id,
            'url': result.url,
            'parameter': result.parameter,
            'payload': result.payload,
            'vulnerability_type': result.vulnerability_type,
            'details': result.details
        })
    
    return jsonify({
        'scan': {
            'id': scan.id,
            'target': scan.target,
            'status': scan.status,
            'started_at': scan.created_at.isoformat() if scan.created_at else None,
            'completed_at': scan.completed_at.isoformat() if scan.completed_at else None
        },
        'results': results_list
    })

@app.route('/api/stop_scan/<int:scan_id>', methods=['POST'])
def stop_scan(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    if scan.status in ['running', 'pending']:
        sqlmap_manager.stop_scan(scan_id)
        scan.status = 'stopped'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Scan stopped successfully'})
    return jsonify({'success': False, 'message': 'Cannot stop scan that is not running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
