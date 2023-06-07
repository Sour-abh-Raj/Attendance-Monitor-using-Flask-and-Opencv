"use strict";

function markAttendance() {
  fetch("/mark_attendance").catch((error) => {
    console.error("Error:", error);
  });
}

function updateDateTime() {
  const now = new Date();
  const datetime = now.toLocaleString("en-US", {
    dateStyle: "medium",
    timeStyle: "medium",
  });
  document.getElementById("datetime").textContent = datetime;
}

setInterval(updateDateTime, 1000);
