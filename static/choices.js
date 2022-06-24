/* This should change specialization options depending on the academic year the student claims to be in */

document.addEventListener("DOMContentLoaded",function() {
    grade = document.getElementById("grade")
    grade.addEventListener("change",function(){
        grade_value = grade.options[grade.selectedIndex].value
        special = document.getElementById("specializations")
        if (grade_value == "second")
        {
            special.innerHTML = '<option selected>اختر التخصص</option><option value="second">علمي</option><option value="third">ادبي</option>'
        }
        else if (grade_value == "third")
        {
            special.innerHTML = '<option selected>اختر التخصص</option><option value="second">علم رياضة</option><option value="third">علم علوم</option><option value="third">ادبي</option>' 
        }
        else
        {
            special.innerHTML = '<option selected disabled>اختر السنة الدراسية اولا</option>'
        }
    })
})
