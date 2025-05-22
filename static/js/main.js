/**
 * SQLi Scanner - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Form validation for scan form (if exists)
    const scanForm = document.getElementById('scanForm');
    if (scanForm) {
        scanForm.addEventListener('submit', function(event) {
            // Form validation is handled by Flask-WTF and the jQuery validation in index.html
        });
    }
    
    // Target type change handler
    const targetTypeSelect = document.getElementById('target_type');
    const targetInput = document.getElementById('target');
    const targetHelp = document.getElementById('targetHelp');
    
    if (targetTypeSelect && targetInput && targetHelp) {
        targetTypeSelect.addEventListener('change', function() {
            updateTargetPlaceholder();
        });
        
        // Initial update
        updateTargetPlaceholder();
    }
    
    function updateTargetPlaceholder() {
        const targetType = targetTypeSelect.value;
        if (targetType === 'domain') {
            targetInput.placeholder = 'example.com';
            if (targetHelp) {
                targetHelp.textContent = 'For domain scans, SQLmap will crawl and test all found URLs.';
            }
        } else {
            targetInput.placeholder = 'https://example.com/page.php?id=1';
            if (targetHelp) {
                targetHelp.textContent = 'For URL scans, SQLmap will test the specific URL.';
            }
        }
    }
    
    // Stop scan confirmation
    const stopScanBtns = document.querySelectorAll('.stop-scan-btn, #stopScanBtn');
    stopScanBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const scanId = this.getAttribute('data-scan-id');
            
            // Using SweetAlert2
            Swal.fire({
                title: 'Stop Scan?',
                text: 'Are you sure you want to stop this scan?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, stop it!'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Send AJAX request to stop scan
                    fetch(`/api/stop_scan/${scanId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire(
                                'Stopped!',
                                'The scan has been stopped.',
                                'success'
                            ).then(() => {
                                window.location.reload();
                            });
                        } else {
                            Swal.fire(
                                'Error!',
                                data.message,
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Error!',
                            'Failed to stop the scan. Please try again.',
                            'error'
                        );
                    });
                }
            });
        });
    });
    
    // Modal handling for vulnerability details
    const resultDetailsModal = document.getElementById('resultDetailsModal');
    if (resultDetailsModal) {
        resultDetailsModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const url = button.getAttribute('data-url');
            const parameter = button.getAttribute('data-parameter');
            const payload = button.getAttribute('data-payload');
            const details = button.getAttribute('data-details');
            
            const modalUrl = document.getElementById('modalUrl');
            const modalParameter = document.getElementById('modalParameter');
            const modalPayload = document.getElementById('modalPayload');
            const modalDetails = document.getElementById('modalDetails');
            
            if (modalUrl) modalUrl.textContent = url;
            if (modalParameter) modalParameter.textContent = parameter;
            if (modalPayload) modalPayload.textContent = payload || 'Not available';
            if (modalDetails) modalDetails.textContent = details || 'Not available';
        });
    }
});
