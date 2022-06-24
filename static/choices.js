/* This should change specialization options depending on the academic year the student claims to be in */

document.addEventListener("DOMContentLoaded",function() {
    grade = document.getElementById("grade")
    grade.addEventListener("change",function(){
        grade_value = grade.options[grade.selectedIndex].value
        special = document.getElementById("specializations")
        if (grade_value == "11")
        {
            special.innerHTML = '<option selected>اختر التخصص</option><option value="scientific">علمي</option><option value="literature">ادبي</option>'
        }
        else if (grade_value == "12")
        {
            special.innerHTML = '<option selected>اختر التخصص</option><option value="math_oriented">علم رياضة</option><option value="science_oriented">علم علوم</option><option value="literature">ادبي</option>' 
        }
        else
        {
            special.innerHTML = '<option selected disabled>اختر السنة الدراسية اولا</option>'
        }
    })
})
