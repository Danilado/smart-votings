let labels = document.querySelectorAll("label");
let form = document.querySelector("form");
let inputs = document.querySelectorAll("input");
let submit = document.querySelector(".bt");
let bigflag = 0;

function validate() {
  flag = 0;
  if (!form.new_password1.value || !form.new_password2.value) flag = 1;
  if (form.new_password1.value != form.new_password2.value) flag = 1;
  if (flag) {
    if (bigflag) submit.style.color = "#333";
    bigflag = 0;
    return (submit.style.pointerEvents = "none");
  }
  if (!bigflag) {
    submit.style.pointerEvents = "all";
    submit.style.color = "rgba(255, 255, 255, 1)";
  }

  bigflag = 1;
}

for (i = 0; i < inputs.length - 1; ++i) {
  inputs[i].addEventListener("input", validate);
}

validate();
