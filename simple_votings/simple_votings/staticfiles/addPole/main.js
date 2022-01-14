let b = document.querySelector(".bt");
let i = document.querySelectorAll("input");

i.forEach((p) => {
  p.addEventListener("input", () => {
    if (i[1].value && i[2].value && i[3].value)
      if (/((\w|\d)\;(\w|\d))/.test(i[3].value))
        b.style.cssText = `
                    pointer-events: all;
                    color: rgba(255, 255, 255, 1);
                `;
      else {
        b.style.cssText = `
                    pointer-events: none;
                    color: #333;
                `;
      }
  });
});

addEventListener("load", () => {
  if (i[1].value && i[2].value && i[3].value)
    if (/((\w|\d)\;(\w|\d))/.test(i[3].value))
      b.style.cssText = `
                    pointer-events: all;
                    color: rgba(255, 255, 255, 1);
                `;
    else {
      b.style.cssText = `
                    pointer-events: none;
                    color: #333;
                `;
    }
});
