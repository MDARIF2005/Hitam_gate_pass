// Get references to the elements
const eneter = document.getElementById("out_of_time");
const normalForm = document.getElementById("Normal_pass_form");
const emergencyForm = document.getElementById("Emergency");
const em_fprm = document.getElementById("em_form");
const wait = document.getElementById("wait_approved");
const gatepass = document.getElementById("gate_pass");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    // Check if the current time is between 10:00 AM and 3:00 PM
    const now = new Date();
    const currentHour = now.getHours();

    const startHour = 7; // 10:00 AM
    const endHour = 24; // 3:00 PM

    // Hide all forms by default
    if (eneter) eneter.style.display = "none";
    if (normalForm) normalForm.style.display = "none";
    if (emergencyForm) emergencyForm.style.display = "none";
    if (em_fprm) em_fprm.style.display = "none";
    if (wait) wait.style.display = "none";
    if (gatepass) gatepass.style.display = "none";

    // Logic for displaying forms based on time
    if (currentHour >= startHour && currentHour < endHour) {
        console.log("Within allowed time range");

        // Show appropriate forms or messages
        // Show emergency form
        if (emergencyForm) emergencyForm.style.display = "block"; // Show emergency form
        if (normalForm) normalForm.style.display = "block"; // Show normal form
        if (wait) wait.style.display = "block"; // Show waiting for approval message
        if (gatepass) gatepass.style.display = "block"; // Show gate pass message
    } else {
        console.log("Outside allowed time range");
        if (eneter) eneter.style.display = "block"; // Show "out_of_time" message
        return; // Stop further execution if outside allowed time
    }

    // Show Emergency form when the button is clicked
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

// Function to show the Emergency form
function showEmergencyForm() {
    if (em_fprm) em_fprm.style.display = "block";
    if (normalForm) normalForm.style.display = "none";
}
