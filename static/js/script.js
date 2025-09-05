// JavaScript for Plant Savior AI

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const dropArea = document.getElementById('dropArea');
    const imageInput = document.getElementById('imageInput');
    const browseBtn = document.getElementById('browseBtn');
    const uploadForm = document.getElementById('uploadForm');
    const predictBtn = document.getElementById('predictBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    const scrollToUpload = document.getElementById('scrollToUpload');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

    // Event Listeners
    browseBtn.addEventListener('click', () => {
        imageInput.click();
    });

    imageInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            predictBtn.disabled = false;
        }
    });

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('active');
    }

    function unhighlight() {
        dropArea.classList.remove('active');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            imageInput.files = files;
            predictBtn.disabled = false;
        }
    }

    // Form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!imageInput.files.length) {
            alert('Please select an image first');
            return;
        }
        
        // Show loading modal
        loadingModal.show();
        
        // Create FormData object
        const formData = new FormData();
        formData.append('image', imageInput.files[0]);
        
        // Send AJAX request
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading modal
            loadingModal.hide();
            
            if (data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred during prediction');
            }
        })
        .catch(error => {
            // Hide loading modal
            loadingModal.hide();
            showError('Network error: ' + error.message);
        });
    });

    // Display results
    function displayResults(data) {
        const confidencePercentage = (data.confidence * 100).toFixed(1);
        
        resultsContent.innerHTML = `
            <div class="result-card fade-in">
                <h3 class="text-center mb-4 fw-bold">
                    <i class="fas fa-diagnoses me-2"></i>Diagnosis Results
                </h3>
                
                <div class="mb-4">
                    <h4 class="fw-bold text-success mb-3">
                        <i class="fas fa-virus me-2"></i>Predicted Disease
                    </h4>
                    <div class="disease-name">${data.prediction}</div>
                </div>
                
                <div class="mb-4">
                    <h4 class="fw-bold text-primary mb-3">
                        <i class="fas fa-chart-line me-2"></i>Confidence Score
                    </h4>
                    <div class="progress-container">
                        <div class="progress-label">
                            <span>Confidence Level</span>
                            <span class="fw-bold">${confidencePercentage}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: ${confidencePercentage}%" 
                                aria-valuenow="${confidencePercentage}" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                    </div>
                </div>
                
                <div>
                    <h4 class="fw-bold text-info mb-3">
                        <i class="fas fa-prescription-bottle-alt me-2"></i>Treatment Recommendation
                    </h4>
                    <div class="treatment-box">
                        <p class="mb-0">${data.treatment}</p>
                    </div>
                </div>
            </div>
        `;
        
        // Show results section
        resultsSection.classList.remove('d-none');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Show error message
    function showError(message) {
        resultsContent.innerHTML = `
            <div class="alert alert-danger fade-in" role="alert">
                <h4 class="alert-heading">
                    <i class="fas fa-exclamation-triangle me-2"></i>Error
                </h4>
                <p class="mb-0">${message}</p>
            </div>
        `;
        
        // Show results section
        resultsSection.classList.remove('d-none');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Scroll to upload section
    scrollToUpload.addEventListener('click', function() {
        document.getElementById('upload').scrollIntoView({ behavior: 'smooth' });
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});