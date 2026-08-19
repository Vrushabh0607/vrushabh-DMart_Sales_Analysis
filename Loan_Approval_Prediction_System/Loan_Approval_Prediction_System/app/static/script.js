// Loan Approval Prediction System — front-end logic
// Handles client-side validation, the predict request, and rendering
// the stamp / probability verdict.

(function () {
  const form = document.getElementById("loanForm");
  const submitBtn = document.getElementById("submitBtn");
  const btnLabel = submitBtn.querySelector(".btn-label");
  const btnLoading = submitBtn.querySelector(".btn-loading");
  const formError = document.getElementById("formError");
  const refNumber = document.getElementById("refNumber");

  const stampPlaceholder = document.getElementById("stampPlaceholder");
  const stamp = document.getElementById("stamp");
  const stampText = document.getElementById("stampText");
  const stampRingParent = stamp.querySelector(".stamp-ring");

  const probabilityBlock = document.getElementById("probabilityBlock");
  const approvalProb = document.getElementById("approvalProb");
  const rejectionProb = document.getElementById("rejectionProb");
  const approvalBar = document.getElementById("approvalBar");
  const rejectionBar = document.getElementById("rejectionBar");

  // Cosmetic file-reference number, purely for the ledger theme
  refNumber.textContent = "FILE No. " + Math.floor(100000 + Math.random() * 900000);

  const VALID_LOAN_TERMS = new Set([120, 180, 240, 300, 360]);
  const VALID_PROPERTY_AREAS = new Set(["Urban", "Semiurban", "Rural"]);

  function setError(fieldName, message) {
    const el = form.querySelector(`.error[data-for="${fieldName}"]`);
    if (el) el.textContent = message || "";
  }

  function clearAllErrors() {
    form.querySelectorAll(".error").forEach((el) => (el.textContent = ""));
    formError.hidden = true;
    formError.textContent = "";
  }

  function validate(values) {
    let valid = true;

    if (values.applicant_income === "" || Number(values.applicant_income) < 0) {
      setError("applicant_income", "Must be 0 or greater.");
      valid = false;
    }
    if (values.coapplicant_income === "" || Number(values.coapplicant_income) < 0) {
      setError("coapplicant_income", "Must be 0 or greater.");
      valid = false;
    }
    if (values.loan_amount === "" || Number(values.loan_amount) < 0) {
      setError("loan_amount", "Must be 0 or greater.");
      valid = false;
    }
    if (!VALID_LOAN_TERMS.has(Number(values.loan_term))) {
      setError("loan_term", "Select a valid term.");
      valid = false;
    }
    const cs = Number(values.credit_score);
    if (values.credit_score === "" || cs < 300 || cs > 850) {
      setError("credit_score", "Must be between 300 and 850.");
      valid = false;
    }
    const ey = Number(values.employment_years);
    if (values.employment_years === "" || ey < 0 || ey > 35) {
      setError("employment_years", "Must be between 0 and 35.");
      valid = false;
    }
    const dti = Number(values.debt_to_income_ratio);
    if (values.debt_to_income_ratio === "" || dti < 0 || dti > 1) {
      setError("debt_to_income_ratio", "Must be between 0 and 1.");
      valid = false;
    }
    if (!VALID_PROPERTY_AREAS.has(values.property_area)) {
      setError("property_area", "Select a property area.");
      valid = false;
    }

    return valid;
  }

  function showStamp(status) {
    stampPlaceholder.hidden = true;
    stamp.hidden = false;

    // Restart the CSS animation each time
    stamp.style.animation = "none";
    // Force reflow so the animation can be re-triggered
    void stamp.offsetWidth;
    stamp.style.animation = "";

    stampRingParent.classList.remove("approve", "reject");
    stampRingParent.classList.add(status === "Approved" ? "approve" : "reject");
    stampText.textContent = status === "Approved" ? "APPROVED" : "REJECTED";
  }

  function showProbabilities(approvalPct, rejectionPct) {
    probabilityBlock.hidden = false;
    approvalProb.textContent = approvalPct.toFixed(2) + "%";
    rejectionProb.textContent = rejectionPct.toFixed(2) + "%";

    // trigger transition
    requestAnimationFrame(() => {
      approvalBar.style.width = approvalPct + "%";
      rejectionBar.style.width = rejectionPct + "%";
    });
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    btnLabel.hidden = isLoading;
    btnLoading.hidden = !isLoading;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    clearAllErrors();

    const formData = new FormData(form);
    const values = Object.fromEntries(formData.entries());

    if (!validate(values)) return;

    setLoading(true);

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        formError.hidden = false;
        formError.textContent = data.error || "Something went wrong. Please try again.";
        return;
      }

      showStamp(data.Loan_Status);
      showProbabilities(data.Approval_Probability, data.Rejection_Probability);
    } catch (err) {
      formError.hidden = false;
      formError.textContent = "Could not reach the prediction service. Please try again.";
    } finally {
      setLoading(false);
    }
  });
})();
