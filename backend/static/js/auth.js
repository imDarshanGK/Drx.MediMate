// Enhanced Form switching functionality with role-based features
document.addEventListener('DOMContentLoaded', function() {
    const signInForm = document.getElementById('signIn');
    const signUpForm = document.getElementById('signup');
    const recoverForm = document.getElementById('recoverPassword');
    
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');
    const recoverPasswordLink = document.getElementById('recoverPasswordLink');
    const backToSignIn = document.getElementById('backToSignIn');
    
    // Password visibility toggles
    const togglePassword = document.getElementById('togglePassword');
    const toggleSignUpPassword = document.getElementById('toggleSignUpPassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword'); // NEW
    const passwordInput = document.getElementById('password');
    const signUpPasswordInput = document.getElementById('rPassword');
    const confirmPasswordInput = document.getElementById('cPassword'); // NEW
    
    // Form switching functions
    function showForm(targetForm) {
        [signInForm, signUpForm, recoverForm].forEach(form => {
            form.style.display = 'none';
            form.classList.remove('active');
        });
        
        targetForm.style.display = 'block';
        setTimeout(() => {
            targetForm.classList.add('active');
        }, 10);
        
        // Clear any existing messages
        document.querySelectorAll('.alert-message').forEach(msg => {
            msg.style.display = 'none';
        });
    }
    
    // Event listeners for form switching
    if (signUpButton) signUpButton.addEventListener('click', (e) => { e.preventDefault(); showForm(signUpForm); });
    if (signInButton) signInButton.addEventListener('click', (e) => { e.preventDefault(); showForm(signInForm); });
    if (recoverPasswordLink) recoverPasswordLink.addEventListener('click', (e) => { e.preventDefault(); showForm(recoverForm); });
    if (backToSignIn) backToSignIn.addEventListener('click', (e) => { e.preventDefault(); showForm(signInForm); });
    
    // Password visibility toggles
    function setupPasswordToggle(toggleButton, passwordField) {
        if (toggleButton && passwordField) {
            toggleButton.addEventListener('click', () => {
                const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordField.setAttribute('type', type);
                
                const icon = toggleButton.querySelector('i');
                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
            });
        }
    }
    
    setupPasswordToggle(togglePassword, passwordInput);
    setupPasswordToggle(toggleSignUpPassword, signUpPasswordInput);
    setupPasswordToggle(toggleConfirmPassword, confirmPasswordInput); // NEW
    
    // Password strength checker
    if (signUpPasswordInput) {
        const strengthBars = document.querySelectorAll('.strength-bar');
        const strengthText = document.querySelector('.strength-text');
        const requirements = document.querySelectorAll('.requirement');
        
        signUpPasswordInput.addEventListener('input', (e) => {
            const password = e.target.value;
            const strength = checkPasswordStrength(password);
            
            strengthBars.forEach((bar, index) => {
                bar.style.backgroundColor = index < strength.score ? getStrengthColor(strength.score) : 'var(--gray-200)';
            });
            
            if (strengthText) strengthText.textContent = getStrengthLabel(strength.score);
            
            requirements.forEach(req => {
                const reqType = req.getAttribute('data-requirement');
                req.classList.toggle('met', strength.requirements[reqType]);
            });
        });
    }
    
    // Role selection handling
    document.querySelectorAll('input[name="userRole"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.querySelectorAll('.role-specific-fields').forEach(field => {
                field.style.display = 'none';
                field.querySelectorAll('input').forEach(input => {
                    input.removeAttribute('required');
                });
            });
            
            const roleFields = document.getElementById(`${this.value}Fields`);
            if (roleFields) {
                roleFields.style.display = 'block';
                roleFields.querySelectorAll('input[data-required="true"]').forEach(input => {
                    input.setAttribute('required', 'required');
                });
            }

            document.querySelectorAll('.role-card').forEach(card => card.classList.remove('selected'));
            this.nextElementSibling.classList.add('selected');
        });
    });
    
    function checkPasswordStrength(password) {
        const requirements = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /\d/.test(password)
        };
        const score = Object.values(requirements).filter(Boolean).length;
        return { requirements, score };
    }
    
    function getStrengthColor(score) {
        return ['var(--gray-200)', 'var(--error-500)', 'var(--warning-500)', 'var(--warning-500)', 'var(--success-500)'][score] || 'var(--gray-200)';
    }
    
    function getStrengthLabel(score) {
        return ['Password strength', 'Very weak', 'Weak', 'Good', 'Strong'][score] || 'Password strength';
    }
    
    // Make validateForm global to be accessible by the Firebase module script
    window.validateForm = function(formType) {
        const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

        if (formType === 'signIn') {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                showMessage('Please fill in all fields.', 'signInMessage', 'warning');
                return false;
            }
            if (!validateEmail(email)) {
                showMessage('Please enter a valid email address.', 'signInMessage', 'error');
                return false;
            }
        }
        
        if (formType === 'signUp') {
            const email = document.getElementById('rEmail').value;
            const password = document.getElementById('rPassword').value;
            const confirmPassword = document.getElementById('cPassword').value; // NEW
            const firstName = document.getElementById('fName').value;
            const lastName = document.getElementById('lName').value;
            const selectedRole = document.querySelector('input[name="userRole"]:checked');
            const agreeTerms = document.getElementById('agreeTerms').checked;
            
            if (!email || !password || !firstName || !lastName || !confirmPassword) {
                showMessage('Please fill in all required fields.', 'signUpMessage', 'warning');
                return false;
            }
            // NEW: Password match validation
            if (password !== confirmPassword) {
                showMessage('Passwords do not match. Please try again.', 'signUpMessage', 'warning');
                return false;
            }
            if (!selectedRole) {
                showMessage('Please select your role.', 'signUpMessage', 'warning');
                return false;
            }
            if (!validateEmail(email)) {
                showMessage('Please enter a valid email address.', 'signUpMessage', 'error');
                return false;
            }
            if (checkPasswordStrength(password).score < 4) { // Requiring strong password
                showMessage('Please choose a stronger password that meets all criteria.', 'signUpMessage', 'error');
                return false;
            }
            
            const roleFields = document.getElementById(`${selectedRole.value}Fields`);
            if (roleFields) {
                for (let field of roleFields.querySelectorAll('input[required]')) {
                    if (!field.value.trim()) {
                        showMessage(`Please fill in all required fields for the ${selectedRole.value} role.`, 'signUpMessage', 'warning');
                        return false;
                    }
                }
            }
            
            if (!agreeTerms) {
                showMessage('Please agree to the Terms of Service and Privacy Policy.', 'signUpMessage', 'warning');
                return false;
            }
        }
        return true;
    }
    
    // Make showMessage global
    window.showMessage = function(message, divId, type = 'error') {
        const messageDiv = document.getElementById(divId);
        messageDiv.className = `alert-message ${type}`;
        messageDiv.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'exclamation-circle'}"></i><span>${message}</span>`;
        messageDiv.style.display = "flex";
        
        setTimeout(() => {
            messageDiv.style.opacity = 0;
            setTimeout(() => { messageDiv.style.display = "none"; messageDiv.style.opacity = 1; }, 300);
        }, 5000);
    };
    
    // Initialize with sign-in form
    showForm(signInForm);
});