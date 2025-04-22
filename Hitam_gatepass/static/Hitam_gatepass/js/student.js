
const eneter = document.getElementById("out_of_time");
const normalForm = document.getElementById("Normal_pass_form");
const emergencyForm = document.getElementById("Emergency");
const em_fprm = document.getElementById("em_form");
const wait = document.getElementById("wait_approved");
const gatepass = document.getElementById("gate_pass");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    const now = new Date();
    const currentHour = now.getHours();

    const startHour = 10; 
    const endHour = 15; 

    if (eneter) eneter.style.display = "none";
    if (normalForm) normalForm.style.display = "none";
    if (emergencyForm) emergencyForm.style.display = "none";
    if (em_fprm) em_fprm.style.display = "none";
    if (wait) wait.style.display = "none";
    if (gatepass) gatepass.style.display = "none";

    if (currentHour >= startHour && currentHour <= endHour) {
        console.log("Within allowed time range");

    
        if (emergencyForm) emergencyForm.style.display = "block"; 
        if (normalForm) normalForm.style.display = "block"; 
        if (wait) wait.style.display = "block"; 
        if (gatepass) gatepass.style.display = "block"; 
    } else {
        console.log("Outside allowed time range");
        if (eneter) eneter.style.display = "block"; 
        return; 
    }

    
    const emergencyButton = document.getElementById("Emergency_button");
    if (emergencyButton) {
        emergencyButton.addEventListener("click", () => {
            showEmergencyForm();
        });
    }

    const submitButton = document.getElementById("submit_button");
    if (submitButton) {
        submitButton.addEventListener("click", () => {
            if (normalForm) normalForm.style.display = "block";
            if (emergencyForm) emergencyForm.style.display = "none";
        });
    }
});


function showEmergencyForm() {
    if (em_fprm) em_fprm.style.display = "block";
    if (normalForm) normalForm.style.display = "none";
}
