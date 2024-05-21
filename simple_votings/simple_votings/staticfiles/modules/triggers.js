function pulse(node, color, color2, fadein, hold, fadeout) {
  anime({
    targets: node,
    backgroundColor: color,
    duration: fadein * 1000,
    easing: "linear",
    loop: false,
  });
  setTimeout(() => {
    anime({
      targets: node,
      backgroundColor: color2,
      duration: fadeout * 1000,
      easing: "linear",
      loop: false,
    });
    // setTimeout(() => {
    //   node.style.backgroundColor = "";
    // }, fadeout * 1000);
  }, (fadein + hold) * 1000);
}

function validateArr(arr) {
  for (i = 0; i < arr.length; ++i)
    if (arr[i].value == "" || arr[i].value == undefined || !arr[i].value)
      return 0;
  return 1;
}
function validateIntArr(arr) {
  for (i = 0; i < arr.length; ++i)
    if (
      arr[i].value == "" ||
      arr[i].value == undefined ||
      !arr[i].value ||
      arr[i].value.match(/\D/)
    )
      return 0;
  return 1;
}
