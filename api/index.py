<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Smart Complaint System</title>
<script>
const API_URL = "/api"; // Vercel serverless route

async function submitComplaint() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const complaint = document.getElementById("complaint").value;

    const res = await fetch(`${API_URL}/submit`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, email, complaint })
    });
    const data = await res.json();
    alert(data.message);
}
</script>
</head>
<body>
<h1>Submit Complaint</h1>
<form onsubmit="event.preventDefault(); submitComplaint();">
    <input type="text" id="name" placeholder="Your Name" required/><br/>
    <input type="email" id="email" placeholder="Your Email" required/><br/>
    <textarea id="complaint" placeholder="Your Complaint" required></textarea><br/>
    <button type="submit">Submit</button>
</form>
</body>
</html>
