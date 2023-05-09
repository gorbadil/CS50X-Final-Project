document.addEventListener("DOMContentLoaded", function () {
  setInterval(() => {
    let time = new Date();
    let hour = time.getHours();
    let min = time.getMinutes();
    let sec = time.getSeconds();
    let day = time.getDate();
    let month = time.getMonth() + 1;
    let year = time.getFullYear();
    let clock = document.querySelector(".clock");

    clock.innerHTML = `${hour}:${min}:${sec} / ${day}-${month}-${year}`;
  }, 1000);
});

document.querySelector(".clock").onmouseover = function () {
  clockMouseOver(document.querySelector(".clock"));
};

document.querySelector(".clock").onmouseout = function () {
  clockMouseOut(document.querySelector(".clock"));
};

function clockMouseOver(item) {
  item.style.color = "red";
}

function clockMouseOut(item) {
  item.style.color = "white";
}

document.querySelector(".head-title-main").onmouseover = function () {
  clockMouseOver(document.querySelector(".head-title-main"));
};

document.querySelector(".head-title-main").onmouseout = function () {
  clockMouseOut(document.querySelector(".head-title-main"));
};
