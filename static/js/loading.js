function isValidTarget(input) {
  const ipPattern = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  const hostnamePattern = /^([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,}$/;
  return ipPattern.test(input) || hostnamePattern.test(input);
}

document.getElementById("scanForm").addEventListener("submit", function (e) {
  const input = document.getElementById("target").value.trim();

  if (!isValidTarget(input)) {
    e.preventDefault();
    return false;
  } else {
    document.getElementById("loader").style.display = "block";
  }
});
