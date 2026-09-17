const API_BASE_URL = 'http://127.0.0.1:8000/api';

/**
 * Authentication Module
 * Handles login, signup, password visibility, and form validation
 */

// ============================================================
// DOM READY
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize password strength checker if on signup page
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', checkPasswordStrength);
    }
    
    // Initialize confirm password validation
    const confirmInput = document.getElementById('confirmPassword');
    if (confirmInput) {
        confirmInput.addEventListener('input', validateConfirmPassword);
    }
    
    // Auto-focus first input
    const firstInput = document.querySelector('.input-wrapper input');
    if (firstInput) {
        firstInput.focus();
    }
});

// ============================================================
// PASSWORD VISIBILITY TOGGLE
// ============================================================

function togglePassword(inputId) {
    // If inputId is provided, use it; otherwise find the input in the same wrapper
    let input;
    if (inputId) {
        input = document.getElementById(inputId);
    } else {
        const wrapper = event.target.closest('.input-wrapper');
        input = wrapper.querySelector('input');
    }
    
    if (!input) return;
    
    const icon = input.parentElement.querySelector('.toggle-password i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// ============================================================
// PASSWORD STRENGTH CHECKER
// ============================================================

function checkPasswordStrength() {
    const password = document.getElementById('password').value;
    const strengthContainer = document.getElementById('passwordStrength');
    const strengthLabel = document.getElementById('strengthLabel');
    
    // Remove existing classes
    strengthContainer.classList.remove('weak', 'medium', 'strong');
    
    if (password.length === 0) {
        strengthLabel.textContent = 'Weak';
        return;
    }
    
    let score = 0;
    
    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    
    // Complexity checks
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;
    
    // Determine strength
    let strength = 'weak';
    let label = 'Weak';
    
    if (score >= 6) {
        strength = 'strong';
        label = 'Strong';
    } else if (score >= 4) {
        strength = 'medium';
        label = 'Medium';
    }
    
    strengthContainer.classList.add(strength);
    strengthLabel.textContent = label;
}

// ============================================================
// CONFIRM PASSWORD VALIDATION
// ============================================================

function validateConfirmPassword() {
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('confirmPassword').value;
    const confirmWrapper = document.getElementById('confirmPassword').parentElement;
    
    if (confirm.length === 0) {
        confirmWrapper.style.borderColor = '';
        return;
    }
    
    if (password === confirm) {
        confirmWrapper.style.borderColor = 'var(--success)';
    } else {
        confirmWrapper.style.borderColor = 'var(--danger)';
    }
}

// ============================================================
// LOGIN HANDLER
// ============================================================

function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.querySelector('.remember-me input').checked;
    
    // Basic validation
    if (!email || !password) {
        showToast('Please fill in all fields', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showToast('Please enter a valid email address', 'error');
        return;
    }
    
    const loginBtn = event.target.querySelector('.auth-btn-primary');
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
    loginBtn.disabled = true;

    fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    })
    .then(async response => {
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Unable to sign in');
        return data;
    })
    .then(data => {
        localStorage.setItem('carRentalSession', JSON.stringify({
            ...data.user,
            loggedInAt: new Date().toISOString()
        }));
        showToast('Welcome back! Redirecting to dashboard...', 'success');
        loginBtn.innerHTML = 'Sign In';
        loginBtn.disabled = false;
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
    })
    .catch(error => {
        showToast(error.message, 'error');
        loginBtn.innerHTML = 'Sign In';
        loginBtn.disabled = false;
    });
    
    return false;
}

// ============================================================
// SIGNUP HANDLER
// ============================================================

function handleSignup(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const company = document.getElementById('company').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const termsChecked = document.querySelector('.checkbox-label input[type="checkbox"]').checked;
    
    // Validation
    if (!firstName || !lastName || !email || !password || !confirmPassword) {
        showToast('Please fill in all required fields', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showToast('Please enter a valid email address', 'error');
        return;
    }
    
    if (password.length < 8) {
        showToast('Password must be at least 8 characters long', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showToast('Passwords do not match', 'error');
        return;
    }
    
    if (!termsChecked) {
        showToast('Please agree to the Terms of Service', 'error');
        return;
    }
    
    const signupBtn = event.target.querySelector('.auth-btn-primary');
    signupBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account...';
    signupBtn.disabled = true;

    fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email,
            phone,
            password
        })
    })
    .then(async response => {
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Unable to create account');
        return data;
    })
    .then(data => {
        localStorage.setItem('carRentalSession', JSON.stringify({
            ...data.user,
            loggedInAt: new Date().toISOString()
        }));
        showToast('Account created successfully! Redirecting...', 'success');
        signupBtn.innerHTML = 'Create Account';
        signupBtn.disabled = false;
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
    })
    .catch(error => {
        showToast(error.message, 'error');
        signupBtn.innerHTML = 'Create Account';
        signupBtn.disabled = false;
    });
    
    return false;
}

// ============================================================
// TOAST / ALERT SYSTEM
// ============================================================

function showToast(message, type = 'success') {
    // Remove existing toast
    const existingToast = document.querySelector('.auth-toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `auth-toast ${type}`;
    
    const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(toast);
    
    // Trigger show animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 400);
    }, 5000);
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function isValidEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

// ============================================================
// ENTER KEY SUPPORT
// ============================================================

document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        const form = document.querySelector('form');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});

// ============================================================
// SOCIAL BUTTON HANDLERS
// ============================================================

document.querySelectorAll('.social-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const provider = this.classList.contains('google') ? 'Google' : 'Email';
        showToast(`Redirecting to ${provider} authentication...`, 'success');
    });
});

// ============================================================
// FORGOT PASSWORD HANDLER
// ============================================================

document.querySelector('.forgot-password')?.addEventListener('click', function(e) {
    e.preventDefault();
    showToast('Password reset link sent to your email!', 'success');
});

// ============================================================
// KEYBOARD SHORTCUTS
// ============================================================

document.addEventListener('keydown', function(e) {
    // Ctrl+Shift+L to quickly focus login
    if (e.ctrlKey && e.shiftKey && e.key === 'L') {
        e.preventDefault();
        const emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.focus();
        }
    }
});

console.log('🔐 CarRentalPro Authentication Module Loaded');
console.log('📌 Keyboard shortcuts: Ctrl+Shift+L to focus email field');
