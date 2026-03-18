// Global variables
let currentResumeId = null;

// Document ready
$(document).ready(function() {
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Photo upload preview
    $('#profile_image').change(function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('#photo-preview-img').attr('src', e.target.result);
                $('#photo-preview').show();
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Add more fields
    $('#add-education').click(function() {
        const html = `
            <div class="education-entry">
                <input type="text" class="form-control" name="degree[]" placeholder="Degree">
                <input type="text" class="form-control" name="institution[]" placeholder="Institution">
                <input type="text" class="form-control" name="graduation_year[]" placeholder="Graduation Year">
                <input type="text" class="form-control" name="cgpa[]" placeholder="CGPA">
                <button type="button" class="btn btn-sm btn-danger remove-entry">Remove</button>
            </div>
        `;
        $('#education-container').append(html);
    });
    
    $('#add-experience').click(function() {
        const html = `
            <div class="experience-entry">
                <input type="text" class="form-control" name="company[]" placeholder="Company Name">
                <input type="text" class="form-control" name="role[]" placeholder="Job Role">
                <input type="text" class="form-control" name="duration[]" placeholder="Duration">
                <textarea class="form-control" name="achievements[]" placeholder="Key Achievements"></textarea>
                <button type="button" class="btn btn-sm btn-danger remove-entry">Remove</button>
            </div>
        `;
        $('#experience-container').append(html);
    });
    
    $('#add-project').click(function() {
        const html = `
            <div class="project-entry">
                <input type="text" class="form-control" name="project_title[]" placeholder="Project Title">
                <textarea class="form-control" name="project_description[]" placeholder="Description"></textarea>
                <input type="text" class="form-control" name="project_technologies[]" placeholder="Technologies Used">
                <button type="button" class="btn btn-sm btn-danger remove-entry">Remove</button>
            </div>
        `;
        $('#projects-container').append(html);
    });
    
    // Remove entry
    $(document).on('click', '.remove-entry', function() {
        $(this).closest('.education-entry, .experience-entry, .project-entry').remove();
    });
    
    // Experience level toggle
    $('#experience_level').change(function() {
        if ($(this).val() === 'experienced') {
            $('#experience-section').show();
        } else {
            $('#experience-section').hide();
        }
    });
    
    // Template selection
    $('.template-card').click(function() {
        const templateId = $(this).data('template-id');
        const resumeId = $(this).data('resume-id');
        
        $('.template-card').removeClass('selected');
        $(this).addClass('selected');
        
        // Save template selection
        $.ajax({
            url: '/select-template/' + resumeId,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ template_id: templateId }),
            success: function(response) {
                if (response.success) {
                    showAlert('Template selected successfully!', 'success');
                }
            },
            error: function(xhr) {
                showAlert('Error selecting template', 'danger');
            }
        });
    });
    
    // ATS Score analysis
    $('#analyze-ats').click(function() {
        const resumeId = $(this).data('resume-id');
        
        $('#ats-loading').show();
        
        $.ajax({
            url: '/ats-score/' + resumeId,
            method: 'GET',
            success: function(data) {
                $('#ats-loading').hide();
                updateATSScore(data.score, data.feedback);
            },
            error: function(xhr) {
                $('#ats-loading').hide();
                showAlert('Error analyzing ATS score', 'danger');
            }
        });
    });
    
    // Job match analysis
    $('#analyze-job-match').click(function() {
        const resumeId = $(this).data('resume-id');
        const jobDescription = $('#job-description').val();
        
        if (!jobDescription) {
            showAlert('Please enter a job description', 'warning');
            return;
        }
        
        $('#match-loading').show();
        
        $.ajax({
            url: '/analyze-job-match',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                resume_id: resumeId,
                job_description: jobDescription
            }),
            success: function(data) {
                $('#match-loading').hide();
                displayJobMatch(data);
            },
            error: function(xhr) {
                $('#match-loading').hide();
                showAlert('Error analyzing job match', 'danger');
            }
        });
    });
    
    // PDF download
    $('#download-pdf').click(function() {
        const resumeId = $(this).data('resume-id');
        window.location.href = '/download-pdf/' + resumeId;
    });
    
    // OTP verification
    $('#verify-email-otp').click(function() {
        const otp = $('#email-otp').val();
        if (!otp) {
            showAlert('Please enter OTP', 'warning');
            return;
        }
        
        // Form submission handled by regular form
    });
    
    $('#resend-otp').click(function() {
        const type = $(this).data('type');
        const email = $('#email').val();
        const phone = $('#phone').val();
        
        $.ajax({
            url: '/resend-otp',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                type: type,
                email: email,
                phone: phone
            }),
            success: function(response) {
                if (response.success) {
                    showAlert('OTP resent successfully!', 'success');
                }
            },
            error: function(xhr) {
                showAlert('Error resending OTP', 'danger');
            }
        });
    });
});

// Helper functions
function showAlert(message, type) {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
    
    $('#alert-container').html(alertHtml);
    
    // Auto dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
}

function updateATSScore(score, feedback) {
    $('#ats-score-value').text(Math.round(score));
    
    // Update score circle
    const percentage = score;
    const degrees = (percentage / 100) * 360;
    $('.score-circle').css('background', 
        `conic-gradient(var(--primary-color) 0deg ${degrees}deg, #eee ${degrees}deg 360deg)`
    );
    
    // Update feedback
    $('#ats-feedback').html(feedback);
    
    // Update score breakdown if available
    if (feedback.components) {
        updateScoreBreakdown(feedback.components);
    }
    
    // Show dashboard
    $('#ats-dashboard').show();
}

function updateScoreBreakdown(components) {
    let html = '';
    for (const [key, value] of Object.entries(components)) {
        const percentage = Math.round(value);
        html += `
            <div class="score-item">
                <span class="score-label">${key.replace('_', ' ')}</span>
                <div class="score-bar">
                    <div class="score-bar-fill" style="width: ${percentage}%"></div>
                </div>
                <span class="score-value">${percentage}%</span>
            </div>
        `;
    }
    $('#score-breakdown').html(html);
}

function displayJobMatch(data) {
    const html = `
        <div class="job-match-results">
            <h4>Match Analysis</h4>
            <p><strong>Similarity Score:</strong> ${Math.round(data.similarity_score * 100)}%</p>
            <p><strong>ATS Score:</strong> ${Math.round(data.ats_score)}%</p>
            
            <div class="keywords-section">
                <h5>Resume Keywords</h5>
                <div class="keyword-tags">
                    ${data.resume_keywords.map(k => `<span class="badge badge-primary">${k}</span>`).join(' ')}
                </div>
                
                <h5>Job Keywords</h5>
                <div class="keyword-tags">
                    ${data.job_keywords.map(k => `<span class="badge badge-secondary">${k}</span>`).join(' ')}
                </div>
            </div>
            
            <p><strong>Feedback:</strong> ${data.ats_feedback}</p>
        </div>
    `;
    
    $('#job-match-results').html(html);
}

// Form validation
function validateResumeForm() {
    const required = ['full_name', 'email', 'phone', 'job_role'];
    let isValid = true;
    
    required.forEach(field => {
        const value = $('[name="' + field + '"]').val();
        if (!value) {
            $('[name="' + field + '"]').addClass('is-invalid');
            isValid = false;
        } else {
            $('[name="' + field + '"]').removeClass('is-invalid');
        }
    });
    
    // Email validation
    const email = $('[name="email"]').val();
    if (email && !isValidEmail(email)) {
        $('[name="email"]').addClass('is-invalid');
        isValid = false;
    }
    
    // Phone validation
    const phone = $('[name="phone"]').val();
    if (phone && !isValidPhone(phone)) {
        $('[name="phone"]').addClass('is-invalid');
        isValid = false;
    }
    
    if (!isValid) {
        showAlert('Please fill all required fields correctly', 'warning');
    }
    
    return isValid;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function isValidPhone(phone) {
    const re = /^[\d\s\-+()]{10,}$/;
    return re.test(phone);
}

// Print resume
function printResume() {
    window.print();
}

// Share resume
function shareResume(resumeId) {
    const url = window.location.origin + '/preview/' + resumeId;
    
    if (navigator.share) {
        navigator.share({
            title: 'My Resume',
            text: 'Check out my resume!',
            url: url
        }).catch(console.error);
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(url).then(() => {
            showAlert('Link copied to clipboard!', 'success');
        });
    }
}

// Dynamic skill suggestions
function suggestSkills() {
    const jobRole = $('#job_role').val();
    
    if (!jobRole) return;
    
    const suggestions = {
        'software engineer': ['Python', 'Java', 'SQL', 'Git', 'Docker', 'AWS', 'JavaScript'],
        'data scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics', 'TensorFlow'],
        'web developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'MongoDB'],
        'project manager': ['Agile', 'Scrum', 'JIRA', 'Risk Management', 'Communication']
    };
    
    let skills = [];
    for (const [role, skillList] of Object.entries(suggestions)) {
        if (jobRole.toLowerCase().includes(role)) {
            skills = skillList;
            break;
        }
    }
    
    if (skills.length > 0) {
        $('#skill-suggestions').html(`
            <div class="suggestions-box">
                <p><strong>Suggested skills:</strong></p>
                ${skills.map(s => `<span class="badge badge-info skill-suggestion">${s}</span>`).join(' ')}
            </div>
        `);
        
        $('.skill-suggestion').click(function() {
            const skill = $(this).text();
            $('#technical_skills').val($('#technical_skills').val() + ', ' + skill);
        });
    }
}

// Auto-save resume
let autoSaveTimer;
function autoSaveResume(resumeId) {
    clearTimeout(autoSaveTimer);
    
    autoSaveTimer = setTimeout(function() {
        const formData = new FormData($('#resume-form')[0]);
        
        $.ajax({
            url: '/auto-save-resume/' + resumeId,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                showAlert('Resume auto-saved', 'success');
            }
        });
    }, 3000);
}

// Initialize on form changes
$(document).on('input change', '#resume-form input, #resume-form textarea, #resume-form select', function() {
    const resumeId = $('#resume-id').val();
    if (resumeId) {
        autoSaveResume(resumeId);
    }
});