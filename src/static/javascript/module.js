export function change_spec(grade_value){ 
    /* changes specialization options depending on the academic year the student claims to be in */
    var special = document.getElementById("specialization")
    if (grade_value == "1")
    {
        special.innerHTML = '<option selected disabled>اختر التخصص</option><option value="s">علمي</option><option value="l">ادبي</option>'
    }
    else if (grade_value == "2")
    {
        special.innerHTML = '<option selected disabled>اختر التخصص</option><option value="m">علم رياضة</option><option value="o">علم علوم</option><option value="l">ادبي</option>' 
    }
    else
    {
        special.innerHTML = '<option selected disabled>اختر السنة الدراسية اولا</option>'
    }
}

export function form_validatation()
{
    'use strict'
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
    
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }
    
        form.classList.add('was-validated')
        }, false)
    })
}