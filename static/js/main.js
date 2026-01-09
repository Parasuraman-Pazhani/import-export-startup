// Import Export Startup – Client Script

document.addEventListener("DOMContentLoaded", function () {

    // Simple login validation
    let loginForm = document.querySelector("form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {

            let inputs = loginForm.querySelectorAll("input");
            let valid = true;

            inputs.forEach(function (input) {
                if (input.value.trim() === "") {
                    valid = false;
                    input.style.border = "2px solid red";
                } else {
                    input.style.border = "1px solid #ccc";
                }
            });

            if (!valid) {
                e.preventDefault();
                alert("Please fill all fields");
            }
        });
    }

});
