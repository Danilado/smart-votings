let m = document.querySelector("menu");
let l = document.querySelector(".loading");
let sect = document.querySelector("section");

let arr = [];
let c = 1;

let lint = setInterval(() => {
  ++c;
  if (c >= 4) c = 1;
  l.innerHTML = `Загружаю` + `.`.repeat(c);
}, 200);

window.addEventListener("scroll", function () {
  if (window.scrollY > 0) {
    m.classList.add("active");
  } else {
    m.classList.remove("active");
  }
});

let xhr = new XMLHttpRequest();
xhr.open("GET", "../get_vote_list/", true);
xhr.send();
xhr.onload = () => {
  arr = JSON.parse(xhr.response);
  clearInterval(lint);
  l.remove();
  sect.style.justifyContent = "initial";
  createPlates(arr);
};
xhr.onerror = () => {
  l.innerHTML = `Произошла какая-то ошибка<br><br>${xhr.response}`;
  clearInterval(lint);
};

function createPlates(a) {
  for(j in a){
    el = a[j]
    // [name, desc, [<votes>]]
    let p = document.createElement("div");
    p.classList.toggle("plate");
    why = "";
    for (i in el[2]) {
      why += `<a href="../vote/submit?id=${+j+1}&choise=${+i+1}"><div class="vote">${el[2][i]}</div></a>`;
    }
    p.innerHTML += `
    <div class="column">
      <h1>${el[0]}</h1>
      <p>${el[1]}</p>
      ${why}
    </div>
    <div class="vert">
      <div class="exp">&bigtriangledown;</div>
      <div class="bt">
        <form action="/edit/" method="get">
          <input type="hidden" name="old_theme" value="${el[0]}">
          <input type="submit" value="✏️">
        </form>
      </div>
      <div class="bt">
        <form action="/vote/report/create" method="get">
          <input type="hidden" name="id" value="${+j+1}">
          <input type="submit" value="🚩">
        </form>
      </div>
    </div>
    `;
    p.innerHTML += ``;
    sect.appendChild(p);
    p.querySelector(".exp").addEventListener("click", () => {
      p.classList.toggle("active");
      if (p.classList.contains("active")) {
        anime({
          targets: p.querySelector("p"),
          height: `
          ${Math.max(
            16,
            (p.querySelector("p").innerHTML.length * 16 * 16) /
              p.querySelector("p").getBoundingClientRect().width
          )}px`,
          duration: 600,
          loop: false,
        });
        anime({
          targets: p.querySelectorAll(".vote"),
          height: "20px",
          margin: "10px 0",
          padding: "4px",
          duration: 100,
          easing: "linear",
          loop: false,
        });
        setTimeout(() => {
          anime({
            targets: p.querySelectorAll(".vote"),
            height: "20px",
            margin: "10px 0",
            width: `${
              p.querySelector("p").getBoundingClientRect().width - 8
            }px`,
            background: "rgba(255, 255, 255, 0.1)",
            color: "rgba(255, 255, 255, 1)",
            duration: 100,
            easing: "linear",
            delay: anime.stagger(50),
            loop: false,
          });
        }, 250);
      } else {
        setTimeout(() => {
          anime({
            targets: p.querySelector("p"),
            height: "16px",
            duration: 600,
            loop: false,
          });
          anime({
            targets: p.querySelectorAll(".vote"),
            width: `0px`,
            padding: "0px",
            duration: 100,
            easing: "linear",
            loop: false,
          });
        }, 75);
        anime({
          targets: p.querySelectorAll(".vote"),
          height: "0px",
          margin: "0 0",
          background: "rgba(255, 255, 255, 0)",
          color: "rgba(255, 255, 255, 0)",
          duration: 50,
          easing: "linear",
          loop: false,
        });
      }
    });
  };
}
