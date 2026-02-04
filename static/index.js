const MAX_FILE_SIZE = 30 * 1024 * 1024; // 30 MB in bytes

const fileInput = document.getElementById("file");
const submitBtn = document.getElementById("submit-btn");
const errorEl = document.getElementById("error");

fileInput.addEventListener("change", function () {
  if (this.files.length > 0) {
    const file = this.files[0];
    if (file.size > MAX_FILE_SIZE) {
      printError("File exceeds size limit (30 MB)");
      this.value = "";
      submitBtn.disabled = true;
    } else {
      clearError();
      submitBtn.disabled = false;
    }
  } else {
    submitBtn.disabled = true;
  }
});

function printError(error) {
  errorEl.innerHTML = `<p>${error}</p>`;
}

function clearError() {
  errorEl.innerHTML = "";
}
