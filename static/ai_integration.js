/**
 * AI Integration JavaScript
 * Handles help tooltips and AI Legal Assistant functionality
 * for the PardonMe Wisconsin Pardon Application
 */

// Global variables for AI integration
let currentAIModal = null;
let activeTooltip = null;

// Configuration
const AI_CONFIG = {
    MIN_CHARS_FOR_AI: 10,
    TOOLTIP_HIDE_DELAY: 300,
    AI_BUTTON_ACTIVATION_DELAY: 500
};

// Target fields for AI Assistant (matches backend configuration)
const AI_TARGET_FIELDS = [
    'previous_pardon_details',
    'other_law_enforcement_details', 
    'other_crimes_details',
    'sentence_details',
    'education_since_conviction',
    'volunteer_work',
    'community_service',
    'counseling_participation',
    'rehabilitation_steps'
];

/**
 * Initialize AI Integration features
 * Call this function when the page loads
 */
function initializeAIIntegration() {
    console.log('Initializing AI Integration...');
    setupTooltips();
    setupAIAssistant();
    setupGlobalEventListeners();
    console.log('AI Integration initialized successfully');
}

/**
 * Setup Help Tooltips System
 * Adds click handlers to all help icons
 */
function setupTooltips() {
    const helpIcons = document.querySelectorAll('.help-icon');
    console.log(`Setting up tooltips for ${helpIcons.length} help icons`);
    
    helpIcons.forEach(icon => {
        icon.addEventListener('click', function(e) {
            e.stopPropagation();
            const tooltip = this.closest('.tooltip');
            const fieldName = this.dataset.field;
            
            if (tooltip && fieldName) {
                toggleTooltip(tooltip, fieldName);
            }
        });
    });
}

/**
 * Toggle tooltip visibility and load content
 */
function toggleTooltip(tooltipElement, fieldName) {
    const tooltipContent = tooltipElement.querySelector('.tooltip-content');
    
    if (!tooltipContent) {
        console.error('Tooltip content element not found');
        return;
    }
    
    // Hide any other active tooltips
    if (activeTooltip && activeTooltip !== tooltipContent) {
        activeTooltip.classList.remove('show');
    }
    
    // Toggle current tooltip
    if (tooltipContent.classList.contains('show')) {
        tooltipContent.classList.remove('show');
        activeTooltip = null;
    } else {
        loadTooltipContent(tooltipContent, fieldName);
        tooltipContent.classList.add('show');
        activeTooltip = tooltipContent;
    }
}

/**
 * Load help text content for tooltip
 */
async function loadTooltipContent(tooltipElement, fieldName) {
    try {
        // Show loading state
        tooltipElement.innerHTML = '<div class="ai-loading-spinner"></div> Loading help...';
        
        const response = await fetch(`/get_field_help/${fieldName}`);
        const data = await response.json();
        
        if (data.success) {
            tooltipElement.innerHTML = data.help_text;
        } else {
            tooltipElement.innerHTML = 'Error loading help text. Please try again.';
            console.error('Error loading tooltip:', data.error);
        }
    } catch (error) {
        console.error('Network error loading tooltip:', error);
        tooltipElement.innerHTML = 'Unable to load help text. Please check your connection.';
    }
}

/**
 * Setup AI Assistant System
 * Monitors textareas and manages AI assistant buttons
 */
function setupAIAssistant() {
    console.log('Setting up AI Assistant...');
    
    // Find all textareas that should have AI assistance
    const textareas = document.querySelectorAll('textarea');
    let aiTextareaCount = 0;
    
    textareas.forEach(textarea => {
        const fieldName = textarea.name || textarea.id;
        
        if (AI_TARGET_FIELDS.includes(fieldName)) {
            setupTextareaAI(textarea, fieldName);
            aiTextareaCount++;
        }
    });
    
    console.log(`AI Assistant enabled for ${aiTextareaCount} textareas`);
}

/**
 * Setup AI assistant for a specific textarea
 */
function setupTextareaAI(textarea, fieldName) {
    // Wrap textarea in container if not already wrapped
    if (!textarea.parentElement.classList.contains('textarea-container')) {
        const container = document.createElement('div');
        container.className = 'textarea-container';
        textarea.parentNode.insertBefore(container, textarea);
        container.appendChild(textarea);
    }
    
    // Create AI assistant button
    const aiButton = document.createElement('button');
    aiButton.type = 'button';
    aiButton.className = 'ai-assistant-btn';
    aiButton.setAttribute('data-field', fieldName);
    aiButton.innerHTML = '✨ AI Legal Assistant';
    
    // Insert button into container
    textarea.parentElement.appendChild(aiButton);
    
    // Setup event listeners
    let activationTimeout;
    
    textarea.addEventListener('input', function() {
        const text = this.value.trim();
        
        // Clear existing timeout
        clearTimeout(activationTimeout);
        
        if (text.length >= AI_CONFIG.MIN_CHARS_FOR_AI) {
            // Activate button after delay
            activationTimeout = setTimeout(() => {
                aiButton.classList.add('active', 'flashing');
            }, AI_CONFIG.AI_BUTTON_ACTIVATION_DELAY);
        } else {
            // Deactivate button immediately
            aiButton.classList.remove('active', 'flashing');
        }
    });
    
    // AI button click handler
    aiButton.addEventListener('click', function() {
        const userInput = textarea.value.trim();
        if (userInput.length >= AI_CONFIG.MIN_CHARS_FOR_AI) {
            openAIModal(fieldName, userInput, textarea);
        }
    });
}

/**
 * Open AI Legal Assistant Modal
 */
async function openAIModal(fieldName, userInput, textareaElement) {
    // Create modal HTML
    const modal = createAIModal(fieldName, userInput);
    document.body.appendChild(modal);
    currentAIModal = modal;
    
    // Show modal
    modal.style.display = 'block';
    
    // Start AI processing
    await processAIRequest(fieldName, userInput, textareaElement);
}

/**
 * Create AI Modal HTML Structure
 */
function createAIModal(fieldName, userInput) {
    const modal = document.createElement('div');
    modal.className = 'ai-modal';
    modal.innerHTML = `
        <div class="ai-modal-content">
            <div class="ai-modal-header">
                <h2 class="ai-modal-title">✨ AI Legal Assistant</h2>
                <span class="ai-modal-close">&times;</span>
            </div>
            <div class="ai-modal-body">
                <div class="ai-field-info">
                    <div class="ai-field-label">Field: ${fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</div>
                    <div class="ai-original-text">"${userInput}"</div>
                </div>
                <div class="ai-loading">
                    <div class="ai-loading-spinner"></div>
                    Analyzing your response and generating suggestions...
                </div>
            </div>
            <div class="ai-modal-footer" style="display: none;">
                <button class="ai-btn ai-btn-reject">Keep Original</button>
                <button class="ai-btn ai-btn-accept">Use AI Suggestion</button>
            </div>
        </div>
    `;
    
    // Setup close handlers
    const closeBtn = modal.querySelector('.ai-modal-close');
    closeBtn.addEventListener('click', () => closeAIModal());
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeAIModal();
        }
    });
    
    return modal;
}

/**
 * Process AI Request
 */
async function processAIRequest(fieldName, userInput, textareaElement) {
    try {
        const response = await fetch('/ai_help', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                field_name: fieldName,
                user_input: userInput
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAIResponse(data, textareaElement);
        } else {
            showAIError(data.error);
        }
    } catch (error) {
        console.error('AI request failed:', error);
        showAIError('Unable to connect to AI service. Please check your internet connection and try again.');
    }
}

/**
 * Show AI Response in Modal
 */
function showAIResponse(data, textareaElement) {
    if (!currentAIModal) return;
    
    const modalBody = currentAIModal.querySelector('.ai-modal-body');
    const modalFooter = currentAIModal.querySelector('.ai-modal-footer');
    
    modalBody.innerHTML = `
        <div class="ai-field-info">
            <div class="ai-field-label">Field: ${data.field_name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</div>
            <div class="ai-original-text">"${data.original_input}"</div>
        </div>
        
        <div class="ai-feedback-section">
            <div class="ai-section-title">Feedback & Suggestions</div>
            <div class="ai-feedback-text">${data.feedback}</div>
        </div>
        
        <div class="ai-feedback-section ai-improved-section">
            <div class="ai-section-title">Improved Version</div>
            <div class="ai-improved-text">${data.improved_version}</div>
        </div>
    `;
    
    modalFooter.style.display = 'flex';
    
    // Setup button handlers
    const acceptBtn = modalFooter.querySelector('.ai-btn-accept');
    const rejectBtn = modalFooter.querySelector('.ai-btn-reject');
    
    acceptBtn.onclick = () => {
        textareaElement.value = data.improved_version;
        // Trigger input event to update any other listeners
        textareaElement.dispatchEvent(new Event('input', { bubbles: true }));
        closeAIModal();
        
        // Remove flashing from AI button
        const aiButton = textareaElement.parentElement.querySelector('.ai-assistant-btn');
        if (aiButton) {
            aiButton.classList.remove('flashing');
        }
    };
    
    rejectBtn.onclick = () => {
        closeAIModal();
    };
}

/**
 * Show AI Error in Modal
 */
function showAIError(errorMessage) {
    if (!currentAIModal) return;
    
    const modalBody = currentAIModal.querySelector('.ai-modal-body');
    const modalFooter = currentAIModal.querySelector('.ai-modal-footer');
    
    modalBody.innerHTML = `
        <div class="ai-error">
            <strong>Error:</strong> ${errorMessage}
        </div>
        <p>Please try again or continue with your original response.</p>
    `;
    
    modalFooter.innerHTML = `
        <button class="ai-btn ai-btn-reject">Close</button>
    `;
    modalFooter.style.display = 'flex';
    
    modalFooter.querySelector('.ai-btn-reject').onclick = () => closeAIModal();
}

/**
 * Close AI Modal
 */
function closeAIModal() {
    if (currentAIModal) {
        currentAIModal.remove();
        currentAIModal = null;
    }
}

/**
 * Setup Global Event Listeners
 */
function setupGlobalEventListeners() {
    // Hide tooltips when clicking outside
    document.addEventListener('click', function(e) {
        if (activeTooltip && !e.target.closest('.tooltip')) {
            activeTooltip.classList.remove('show');
            activeTooltip = null;
        }
    });
    
    // Handle escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // Close AI modal
            if (currentAIModal) {
                closeAIModal();
            }
            
            // Close active tooltip
            if (activeTooltip) {
                activeTooltip.classList.remove('show');
                activeTooltip = null;
            }
        }
    });
}

/**
 * Utility function to check if AI features are available
 */
function checkAIAvailability() {
    return fetch('/ai_help', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ field_name: 'test', user_input: 'test' })
    })
    .then(response => response.status !== 503)
    .catch(() => false);
}

// Auto-initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAIIntegration);
} else {
    initializeAIIntegration();
}
