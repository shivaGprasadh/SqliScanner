import os
import subprocess
import threading
import json
import logging
import time
import re
from datetime import datetime
import tempfile
import shlex

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import within the function to avoid circular imports
def get_db():
    from app import db
    return db

class SQLMapManager:
    def __init__(self):
        self.active_scans = {}  # Maps scan_id to process object
        self.scan_threads = {}  # Maps scan_id to thread object
        self.output_dir = tempfile.mkdtemp(prefix="sqlmap_results_")
        self.sqlmap_path = "/nix/store/k8y38mbfvg8sjmsxcv1qh7dr1z4k1lk5-python3.11-sqlmap-1.8.5/bin/sqlmap"
        
        # Ensure SQLMap is installed
        try:
            subprocess.run([self.sqlmap_path, "--version"], capture_output=True, text=True, check=True)
            logger.info("SQLMap is available and working")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error(f"SQLMap check failed: {e}")
    
    def _build_sqlmap_command(self, target, target_type, options):
        """Build the SQLMap command with provided options"""
        # Base command with output directory
        cmd = [self.sqlmap_path, "-v", "--output-dir", self.output_dir]
        
        # Add target
        if target_type == 'domain':
            # SQLMap uses only --crawl, remove the crawl-depth option
            crawl_depth = options.pop("crawl-depth", 1) if "crawl-depth" in options else 1
            cmd.extend(["--url", target, "--crawl", str(crawl_depth)])
        else:  # url
            cmd.extend(["--url", target])
        
        # Add options from the form
        for option, value in options.items():
            # Skip crawl since we already handled it
            if option == 'crawl':
                continue
                
            # Handle special case for technique
            if option == 'technique' and value:
                # Ensure technique value is properly formatted (BEUSTQ)
                valid_chars = set('BEUSTQ')
                technique_value = ''.join(c for c in value if c in valid_chars)
                if technique_value:
                    cmd.extend([f"--{option}", technique_value])
            # Handle identifiers (users, passwords)
            elif option == 'identifiers' and value and isinstance(value, bool):
                cmd.append("--users")
                cmd.append("--passwords")
            # Handle Boolean options
            elif isinstance(value, bool) and value:
                cmd.append(f"--{option}")
            # Handle other value options
            elif value and not isinstance(value, bool):
                cmd.extend([f"--{option}", str(value)])
        
        # Ensure we have JSON output for parsing
        if "--batch" not in cmd:
            cmd.append("--batch")
        
        return cmd
    
    def _parse_sqlmap_output(self, output, scan_id):
        """Parse SQLMap output to update progress and detect vulnerabilities"""
        from app import app
        
        with app.app_context():
            from models import ScanResult
            
            db = get_db()
            scan = self._get_scan(scan_id)
            if not scan:
                return
                
            # Update progress based on output lines
            progress_regex = r'(\d+)% \(\d+/\d+\)'
            stage_regex = r'testing (.+?)(?:\s|$)'
            
            progress_match = re.search(progress_regex, output)
            if progress_match:
                progress = int(progress_match.group(1))
                scan.progress = progress
                
            stage_match = re.search(stage_regex, output)
            if stage_match:
                scan.current_stage = stage_match.group(1)
            
            # Check for vulnerability findings
            if "is vulnerable" in output:
                # Extract information about the vulnerability
                url_match = re.search(r'Parameter: (.+?) \((.+?)\)', output)
                if url_match:
                    parameter = url_match.group(1)
                    method = url_match.group(2)
                    
                    # Create a scan result
                    result = ScanResult()
                    result.scan_id = scan_id
                    result.url = scan.target
                    result.parameter = parameter
                    result.vulnerability_type = "SQL Injection"
                    result.details = output
                    db.session.add(result)
                    
            db.session.commit()
    
    def _get_scan(self, scan_id):
        """Get scan from database"""
        from models import Scan
        db = get_db()
        return db.session.query(Scan).filter_by(id=scan_id).first()
    
    def _scan_thread(self, scan_id, target, target_type, options, app_ctx):
        """Thread function to run SQLMap scan"""
        # Import needed at the top of the function
        from app import app
        
        # Enter the application context
        with app_ctx:
            db = get_db()
            from models import Scan, ScanResult
            
            try:
                # Get scan from database
                scan = self._get_scan(scan_id)
                if not scan:
                    logger.error(f"Scan {scan_id} not found in database")
                    return
                    
                # Update scan status to running
                scan.status = "running"
                scan.started_at = datetime.utcnow()
                db.session.commit()
                
                # Build SQLMap command
                cmd = self._build_sqlmap_command(target, target_type, options)
                logger.info(f"Starting SQLMap scan with command: {' '.join(cmd)}")
                
                # Start SQLMap process
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Store process in active_scans
                self.active_scans[scan_id] = process
                
                # Read output line by line to update progress
                if process.stdout:
                    for line in iter(process.stdout.readline, ''):
                        logger.debug(f"SQLMap output: {line.strip()}")
                        self._parse_sqlmap_output(line, scan_id)
                        
                        # Check if process was terminated
                        if scan_id not in self.active_scans:
                            logger.info(f"Scan {scan_id} was manually stopped")
                            process.terminate()
                            break
                
                # Wait for process to complete
                return_code = process.wait()
                
                # Update scan status based on return code
                scan = self._get_scan(scan_id)
                if scan and scan.status != "stopped":
                    scan.status = "completed" if return_code == 0 else "failed"
                    scan.completed_at = datetime.utcnow()
                    scan.progress = 100 if return_code == 0 else scan.progress
                    db.session.commit()
                    
                # Process results
                self._process_final_results(scan_id)
                
                # Clean up
                if scan_id in self.active_scans:
                    del self.active_scans[scan_id]
                    
            except Exception as e:
                logger.exception(f"Error in scan thread: {e}")
                scan = self._get_scan(scan_id)
                if scan:
                    scan.status = "failed"
                    scan.completed_at = datetime.utcnow()
                    db.session.commit()
    
    def _process_final_results(self, scan_id):
        """Process final results from SQLMap output files"""
        from models import Scan, ScanResult
        
        db = get_db()
        scan = self._get_scan(scan_id)
        if not scan:
            return
            
        # Check if there are any target-specific result files
        target_dir = os.path.join(self.output_dir, scan.target.replace("://", "_").replace("/", "_").replace(":", "_"))
        if os.path.exists(target_dir):
            # Look for JSON output files
            for file in os.listdir(target_dir):
                if file.endswith('.json'):
                    try:
                        with open(os.path.join(target_dir, file), 'r') as f:
                            result_data = json.load(f)
                        
                        # Process vulnerabilities
                        if 'data' in result_data:
                            for vuln_url, vuln_data in result_data['data'].items():
                                if 'params' in vuln_data:
                                    for param_type, params in vuln_data['params'].items():
                                        for param_name, param_details in params.items():
                                            if param_details.get('injectable'):
                                                # Create a scan result for each vulnerability
                                                result = ScanResult()
                                                result.scan_id = scan_id
                                                result.url = vuln_url
                                                result.parameter = f"{param_name} ({param_type})"
                                                result.payload = param_details.get('payload', '')
                                                result.vulnerability_type = "SQL Injection"
                                                result.details = json.dumps(param_details)
                                                db.session.add(result)
                    except Exception as e:
                        logger.exception(f"Error processing result file: {e}")
        
        db.session.commit()
    
    def start_scan(self, scan_id, target, target_type, options):
        """Start a new SQLMap scan"""
        from app import app
        
        # Create a copy of the application context for the thread
        app_ctx = app.app_context()
        
        scan_thread = threading.Thread(
            target=self._scan_thread,
            args=(scan_id, target, target_type, options, app_ctx)
        )
        scan_thread.daemon = True
        scan_thread.start()
        
        self.scan_threads[scan_id] = scan_thread
        return True
    
    def stop_scan(self, scan_id):
        """Stop a running scan"""
        if scan_id in self.active_scans:
            process = self.active_scans[scan_id]
            process.terminate()
            del self.active_scans[scan_id]
            return True
        return False