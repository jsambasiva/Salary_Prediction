// When opened directly as a file, talk to the local backend; otherwise use same origin.
const API_BASE = window.location.protocol === "file:" ? "http://127.0.0.1:8000" : "";

const form = document.getElementById("salary-form");
const submitBtn = document.getElementById("submit-btn");
const emptyState = document.getElementById("empty-state");
const resultBox = document.getElementById("result");
const errorBox = document.getElementById("error");

const inr = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0,
});

const toLakhs = (value) => `${(value / 100000).toFixed(2)} lakh per year`;

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
  resultBox.hidden = true;
  emptyState.hidden = true;
}

function showResult(data) {
  errorBox.hidden = true;
  emptyState.hidden = true;
  resultBox.hidden = false;

  document.getElementById("amount").textContent = inr.format(data.predicted_salary);
  document.getElementById("amount-words").textContent = toLakhs(data.predicted_salary);
  document.getElementById("low").textContent = inr.format(data.lower_estimate);
  document.getElementById("high").textContent = inr.format(data.upper_estimate);

  // Fill shows where the prediction sits inside the range.
  const span = data.upper_estimate - data.lower_estimate || 1;
  const pct = ((data.predicted_salary - data.lower_estimate) / span) * 100;
  const fill = document.getElementById("range-fill");
  fill.style.width = "0";
  requestAnimationFrame(() => (fill.style.width = `${Math.min(Math.max(pct, 5), 100)}%`));
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const experience = parseFloat(form.experience.value);
  if (Number.isNaN(experience) || experience < 0 || experience > 40) {
    showError("Enter years of experience between 0 and 40.");
    return;
  }

  const payload = {
    experience,
    education: form.education.value,
    job_role: form.job_role.value,
    city_tier: form.city_tier.value,
  };

  submitBtn.disabled = true;
  submitBtn.textContent = "Predicting...";

  try {
    const response = await fetch(`${API_BASE}/api/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`Server returned ${response.status}`);
    showResult(await response.json());
  } catch (err) {
    showError("Could not reach the server. Check that the backend is running on port 8000.");
    console.error(err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Predict salary";
  }
});
