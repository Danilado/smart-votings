let labels = document.querySelectorAll("label");
let form = document.querySelector("form");
let inputs = document.querySelectorAll("input");
let submit = document.querySelector(".bt");
let bigflag = 0;
let timeout;

function validate() {
  flag = 0;
  clearTimeout(timeout);
  if (/\s|-|\+/g.test(form.username.value)) {
    pulse(
      form.username,
      "rgba(255, 0, 0, 1)",
      "rgba(0, 0, 0, 0.2)",
      0.1,
      0,
      0.6
    );
    flag = 1;
  }
  if (/\s|-|\+/g.test(form.password.value)) {
    pulse(
      form.password,
      "rgba(255, 0, 0, 1)",
      "rgba(0, 0, 0, 0.2)",
      0.1,
      0,
      0.6
    );
    flag = 1;
  }
  if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/.test(form.email.value)) {
    if (form.email.value) {
      timeout = setTimeout(() => {
        pulse(
          form.email,
          "rgba(255, 0, 0, 1)",
          "rgba(0, 0, 0, 0.2)",
          0.1,
          0,
          0.6
        );
      }, 1000);
    }
    flag = 1;
  }
  if (!form.username.value || !form.password.value || !form.email.value)
    flag = 1;
  if (flag) {
    if (bigflag) submit.style.color = "#333";
    bigflag = 0;
    return (submit.style.pointerEvents = "none");
  }
  if (!bigflag) {
    k = 0;
    let pogovik = setInterval(() => {
      pulse(
        inputs[k],
        "rgba(255, 255, 255, 0.2)",
        "rgba(0, 0, 0, 0.2)",
        0.3,
        0,
        0.5
      );
      ++k;
      if (k >= inputs.length - 1) clearInterval(pogovik);
    }, 200);
    submit.style.pointerEvents = "all";
    submit.style.color = "rgba(255, 255, 255, 1)";
  }

  bigflag = 1;
}

document.title = "Регистрация";

labels.forEach((node) => {
  node.innerHTML = node.innerHTML
    .replace(/Username/, "Имя пользователя")
    .replace(/Password/, "Пароль");
});

for (i = 0; i < inputs.length - 1; ++i) {
  inputs[i].addEventListener("input", validate);
}

submit.value = submit.value.replace(/Register/, "Зарегистрироваться");
