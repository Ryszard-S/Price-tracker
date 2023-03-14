let elem = document.getElementById("time");

const arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
arr.forEach((item) => {
  console.log(item, 9 - item);
  setTimeout(() => {
    elem.textContent = (9 - item).toString();
  }, 1000 * item);
});

setTimeout(function () {
  document.location.href = "/";
}, 10000);
