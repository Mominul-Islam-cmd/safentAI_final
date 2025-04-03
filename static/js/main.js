// Common JavaScript functions for the site

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Setup approval buttons
    setupApprovalButtons();
    
    // Setup like buttons
    setupLikeButtons();
    
    // Setup delete confirmations
    setupDeleteConfirmations();
    
    // Animate feedback cards
    animateFeedbackCards();
});

// Function to handle approval/rejection of content
function setupApprovalButtons() {
    const approvalButtons = document.querySelectorAll('.approval-btn');
    
    approvalButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const contentId = this.dataset.id;
            const status = this.dataset.status;
            const contentType = this.dataset.type;
            let url;
            
            // Set URL based on content type
            if (contentType === 'paper') {
                url = `/research/approve/${contentId}/`;
            } else if (contentType === 'topic') {
                url = `/expert-topics/approve/${contentId}/`;
            } else if (contentType === 'blog') {
                url = `/blog/approve/${contentId}/`;
            }
            
            // Send approval/rejection request
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `status=${status}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove the approved/rejected item from the list
                    const itemElement = document.getElementById(`${contentType}-${contentId}`);
                    if (itemElement) {
                        itemElement.remove();
                    }
                    
                    // Show success message
                    showAlert('success', `Content has been ${status}!`);
                } else {
                    showAlert('danger', 'An error occurred. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred. Please try again.');
            });
        });
    });
}

// Function to handle likes on blog posts
function setupLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const postId = this.dataset.id;
            const url = `/blog/like/${postId}/`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update like count
                    const likeCountElement = document.getElementById(`likes-count-${postId}`);
                    if (likeCountElement) {
                        likeCountElement.textContent = data.likes_count;
                    }
                    
                    // Toggle like button icon/text
                    const likeIcon = this.querySelector('i');
                    if (data.liked) {
                        likeIcon.classList.remove('far');
                        likeIcon.classList.add('fas');
                        this.classList.add('liked');
                    } else {
                        likeIcon.classList.remove('fas');
                        likeIcon.classList.add('far');
                        this.classList.remove('liked');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred. Please try again.');
            });
        });
    });
}

// Function to setup delete confirmations
function setupDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
}

// Helper function to show alerts
function showAlert(type, message) {
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        const alertElement = document.createElement('div');
        alertElement.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
        alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        alertContainer.appendChild(alertElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alertElement.classList.remove('show');
            setTimeout(() => {
                alertContainer.removeChild(alertElement);
            }, 150);
        }, 5000);
    }
}

// Helper function to get CSRF cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to animate feedback cards when they appear
function animateFeedbackCards() {
    const feedbackCards = document.querySelectorAll('.feedback-card');
    
    if (feedbackCards.length === 0) return;
    
    // Add intersection observer to animate cards when they come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add a small delay for each card to create a cascade effect
                setTimeout(() => {
                    entry.target.classList.add('show');
                }, 100 * Array.from(feedbackCards).indexOf(entry.target));
                
                // Unobserve after animation
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 }); // Trigger when at least 10% of the card is visible
    
    // Observe each feedback card
    feedbackCards.forEach(card => {
        observer.observe(card);
    });
    
    // Also handle filter tab clicks to animate newly visible cards
    const filterTabs = document.querySelectorAll('.feedback-filter-tab');
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Reset all cards (wait a bit for the filter to take effect)
            setTimeout(() => {
                document.querySelectorAll('.feedback-card:not(.show)').forEach(card => {
                    if (card.style.display !== 'none') {
                        setTimeout(() => {
                            card.classList.add('show');
                        }, 100 * Array.from(document.querySelectorAll('.feedback-card:not(.show)')).indexOf(card));
                    }
                });
            }, 100);
        });
    });
}
