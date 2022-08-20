import { form_validatation, change_spec } from "./module.js";

document.addEventListener("DOMContentLoaded", function () {
    // FORM VALIDATION USING BOOTSTRAP
    form_validatation();


    // Update Grades Values while choosing
    var grade = document.getElementById("grade");
    var grade_value = grade.options[grade.selectedIndex].value
    change_spec(grade_value);
    grade.addEventListener("change", function () {
        grade_value = grade.options[grade.selectedIndex].value;
        change_spec(grade_value);
    })
})
