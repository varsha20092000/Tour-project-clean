document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");
    const usernameField = document.querySelector("input[name='username']");
    const passwordField = document.querySelector("input[name='password']");
    const submitButton = document.querySelector(".btn");

    const continueButton = document.querySelector("#continue-button");
    const otpPopup = document.getElementById("otp-popup");
    const otpInputs = document.querySelectorAll(".otp-input-container input");
    const verifyOtpButton = document.getElementById("verify-otp");
    const closeOtpPopupButton = document.getElementById("close-otp-popup");

    let sentOtp = ""; // Store OTP

    // Validate login form
    function validateInput() {
        let isValid = true;

        if (usernameField.value.trim() === "") {
            usernameField.classList.add("error");
            isValid = false;
        } else {
            usernameField.classList.remove("error");
        }

        if (passwordField.value.trim() === "") {
            passwordField.classList.add("error");
            isValid = false;
        } else {
            passwordField.classList.remove("error");
        }

        submitButton.disabled = !isValid;
    }

    // Event listeners for validation
    usernameField.addEventListener("input", validateInput);
    passwordField.addEventListener("input", validateInput);

    // Handle form submission
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const username = usernameField.value.trim();
        const password = passwordField.value.trim();

        if (username && password) {
            console.log("Form submitted:", { username, password });
            loginForm.submit();
        } else {
            alert("Please fill in all fields!");
        }
    });

    // Forgot Password functionality
    const forgotPasswordLink = document.getElementById('forgot-password-link');
    const popupOverlay = document.getElementById('popup-overlay');
    const closePopup = document.getElementById('close-popup');
    const forgotEmailField = document.getElementById('forgot-email');

    if (forgotPasswordLink && popupOverlay && closePopup) {
        forgotPasswordLink.addEventListener('click', function(event) {
            event.preventDefault();
            popupOverlay.style.display = 'flex';
        });

        closePopup.addEventListener('click', function() {
            popupOverlay.style.display = 'none';
        });

        window.addEventListener('click', function(event) {
            if (event.target === popupOverlay) {
                popupOverlay.style.display = 'none';
            }
        });
    }

    // OTP functionality
    function sendOtpToEmail() {
        sentOtp = Math.floor(1000 + Math.random() * 9000).toString();
        console.log("OTP sent to email:", sentOtp); // For demo purposes
    }

    function showOtpPopup() {
        otpPopup.style.display = "flex";
    }

    function verifyOtp() {
        const enteredOtp = Array.from(otpInputs).map(input => input.value).join('');
        
        if (enteredOtp === sentOtp) {
            alert("OTP Verified Successfully!");
            otpPopup.style.display = "none"; // Close OTP popup
        } else {
            alert("Invalid OTP. Please try again.");
        }
    }

    continueButton.addEventListener("click", function() {
        if (forgotEmailField.value.trim() !== "") {
            console.log("Continue button clicked, sending OTP...");
            sendOtpToEmail();
            showOtpPopup();
        } else {
            alert("Please enter a valid email address.");
        }
    });
    

    verifyOtpButton.addEventListener("click", verifyOtp);

    closeOtpPopupButton.addEventListener("click", function() {
        otpPopup.style.display = "none";
    });

    otpInputs.forEach((input, index) => {
        input.addEventListener("input", function() {
            if (input.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });
    });
});
