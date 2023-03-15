let elem = document.getElementById("time");

const arr = [0, 1, 2, 3, 4, 5];
arr.forEach((item) => {
  setTimeout(() => {
    elem.textContent = (5 - item).toString();
  }, 1000 * item);
});

setTimeout(function () {
  document.location.href = "/";
}, 6000);
