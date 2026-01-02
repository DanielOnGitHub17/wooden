document.addEventListener("DOMContentLoaded", function () {
    const form = getS(".register-form");
    const recaptchaErrors = get("recaptcha-errors");

    form.addEventListener("submit", function (event) {
        if (!grecaptcha.getResponse()) {
            event.preventDefault();
            recaptchaErrors.textContent = "Please complete the reCAPTCHA.";
        }
    });
});