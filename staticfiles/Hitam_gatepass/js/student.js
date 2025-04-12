// Get references to the elements
const eneter = document.getElementById("out_of_time");
const student = document.getElementById("student");
const normalForm = document.getElementById("Normal_pass_form");
const emergencyForm = document.getElementById("Emergency");
const em_fprm = document.getElementById("em_form");


eneter.style.display = "none"; // Hide the "out_of_time" message by default
student.style.display = "none";
em_fprm.style.display = "none"; // Hide the student form by default
emergencyForm.style.display = "none"; // Hide the emergency form by default
normalForm.style.display = "none"; // Hide the normal form by default
 // Hide the student form by default

// Example logic to show/hide forms based on conditions
if (eneter) {
    eneter.style.display = "block"; // Show the "out_of_time" message
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");
    const normalForm = document.getElementById("Normal_pass_form");
    const emergencyForm = document.getElementById("Emergency");

    // Hide forms by default
    if (normalForm) normalForm.style.display = "none";
    if (emergencyForm) emergencyForm.style.display = "none";

    // Example: Show Emergency form when the button is clicked
    const emergencyButton = document.getElementById("Emergency_button");
    if (emergencyButton) {
        emergencyButton.addEventListener("click", () => {
            showEmergencyForm();
        });
    }

    // Show Normal Pass form on button click
    const submitButton = document.getElementById("submit_button");
    if (submitButton) {
        submitButton.addEventListener("click", () => {
            if (normalForm) normalForm.style.display = "block";
            if (emergencyForm) emergencyForm.style.display = "none";
        });
    }
});

function showEmergencyForm() {
    const emergencyForm = document.getElementById("Emergency_form");
    const normalForm = document.getElementById("Normal_pass_form");

    if (emergencyForm) emergencyForm.style.display = "block";
    if (normalForm) normalForm.style.display = "none";
}
