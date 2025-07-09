// First check if input is valid before any processing
function isValidTarget(input) {
  input = input.trim();

  // 1. Check for "localhost"
  if (input.toLowerCase() === 'localhost') return true;

  // 2. Check for IPv4 (0-255.0-255.0-255.0-255)
  const ipv4Pattern = /^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$/;
  if (ipv4Pattern.test(input)) return true;

  // 3. Check for domain (example.com)
  const domainPattern = /^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$/i;
  return domainPattern.test(input);
}

function showInputError(element) {
  element.classList.add('error', 'shake-animation');

  // Remove animation after it ends
  element.addEventListener('animationend', () => {
    element.classList.remove('shake-animation');
  }, { once: true });

  element.focus();
  element.select();
}

function showLoader() {
  document.getElementById("loader").style.display = "block";
}

async function handleSearch(event) {
  event.preventDefault();

  const inputElement = document.getElementById('target');
  const input = inputElement.value.trim();

  // First validate client-side
  if (!isValidTarget(input)) {
    showInputError(inputElement);
    return; // Stop if invalid
  }

  const searchBtn = document.querySelector('.btn-search');
  searchBtn.textContent = 'Scanning...';
  searchBtn.disabled = true;

  try {
    const form = event.target;
    form.submit(); // Let the form submit normally
  } catch (error) {
    console.error('Error:', error);
    searchBtn.textContent = 'Scan Now';
    searchBtn.disabled = false;
  }
}

// Clear error when typing
document.getElementById('target')?.addEventListener('input', function() {
  this.classList.remove('error', 'shake-animation');
});

// Initialize form handler
document.querySelector('form')?.addEventListener('submit', handleSearch);

document.getElementById('save-report')?.addEventListener('click', function () {
  const h2Elements = document.querySelectorAll('.nmap-overlay h2');
  let target = '';

  h2Elements.forEach(el => {
    if (el.textContent && !el.textContent.startsWith('IP:')) {
      target = el.textContent.trim();
    }
  });

  console.log("Target found:", target);

  if (!target) {
    alert("Target not found.");
    return;
  }

  const downloadUrl = `/download/${encodeURIComponent(target)}`;
  console.log("Download URL:", downloadUrl);

  const link = document.createElement('a');
  link.href = downloadUrl;
  link.download = `scan_result_${target}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
});
