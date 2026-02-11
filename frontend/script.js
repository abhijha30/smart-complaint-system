const API = "https://YOUR-VERCEL-BACKEND.vercel.app"; // NO slash at end

document.getElementById("complaintForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const msg = document.getElementById("msg");
  msg.innerText = "Submitting complaint...";

  const form = e.target;

  const data = {
    name: form.name.value.trim(),
    age: Number(form.age.value),
    email: form.email.value.trim(),
    contact: form.contact.value.trim(),
    designation: form.designation.value.trim(),
    company: form.company.value.trim(),
    complaint: form.complaint.value.trim()
  };

  try {
    const res = await fetch(API + "/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    const result = await res.json();

    msg.style.color = "green";
    msg.innerText = result.message || "Complaint submitted successfully";

    form.reset();

  } catch (error) {
    msg.style.color = "red";
    msg.innerText = "Something went wrong. Please try again.";
  }
});
