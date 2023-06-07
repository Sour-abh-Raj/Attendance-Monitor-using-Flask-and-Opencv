"use strict";

function updateDateTime() {
  const now = new Date();
  const datetime = now.toLocaleString("en-US", {
    dateStyle: "medium",
    timeStyle: "medium",
  });
  document.getElementById("datetime").textContent = datetime;
}

setInterval(updateDateTime, 1000);
