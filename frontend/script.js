const API = "/api";

/* =========================
   🟢 REGISTER
========================= */
function register() {
  fetch(API + "/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: name.value,
      email: email.value,
      password: pass.value
    })
  })
  .then(r => r.json())
  .then(d => {
    alert(d.message);
  });
}

/* =========================
   🔐 LOGIN (USER + ADMIN)
========================= */
function login() {
  fetch(API + "/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: lemail.value,
      password: lpass.value
    })
  })
  .then(r => r.json())
  .then(d => {
    if (d.role === "admin") {
      alert("Admin Login Success");
      localStorage.setItem("user", lemail.value);
      location.href = "admin.html";
    } else {
      alert("User Login Success");
      localStorage.setItem("user", lemail.value);
      location.href = "index.html";
    }
  })
  .catch(() => alert("Login Failed"));
}

/* =========================
   📝 SUBMIT COMPLAINT
========================= */
function submit() {
  fetch(API + "/complaint", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      contact: document.getElementById("contact").value,
      title: document.getElementById("title").value,
      type: document.getElementById("type").value,
      remark: document.getElementById("remark").value
    })
  })
  .then(r => r.json())
  .then(d => {
    alert(d.message);
  });
}

/* =========================
   👤 USER VIEW OWN COMPLAINTS
========================= */
function myComplaints() {
  let email = localStorage.getItem("user");

  fetch(API + "/my?email=" + email)
    .then(r => r.json())
    .then(data => {
      let html = "";
      data.forEach(c => {
        html += `
        <div style="border:1px solid #ccc;padding:10px;margin:10px">
          <b>${c.title}</b><br>
          Type: ${c.type}<br>
          Status: ${c.status}
        </div>`;
      });

      document.getElementById("data").innerHTML = html;
    });
}

/* =========================
   🧑‍💼 ADMIN LOAD + FILTER
========================= */
function load() {
  let s = document.getElementById("start").value;
  let e = document.getElementById("end").value;
  let t = document.getElementById("type").value;

  fetch(`${API}/admin?start=${s}&end=${e}&type=${t}`)
    .then(r => r.json())
    .then(data => {
      let html = "";

      data.forEach(c => {
        html += `
        <div style="border:1px solid #000;padding:10px;margin:10px">
          <b>${c.name}</b> (${c.type})<br>
          Email: ${c.user_email}<br>
          Title: ${c.title}<br>
          Status: ${c.status}<br>

          <button onclick="update('${c.id}','Resolved')">Resolve</button>
          <button onclick="update('${c.id}','In Progress')">In Progress</button>
        </div>
        `;
      });

      document.getElementById("data").innerHTML = html;
    });
}

/* =========================
   🔄 UPDATE STATUS (ADMIN)
========================= */
function update(id, status) {
  fetch(API + "/update", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: id,
      status: status
    })
  })
  .then(r => r.json())
  .then(d => {
    alert(d.message);
    load(); // reload list
  });
}

/* =========================
   📥 DOWNLOAD EXCEL
========================= */
function download() {
  let s = document.getElementById("start").value;
  let e = document.getElementById("end").value;
  let t = document.getElementById("type").value;

  window.open(`${API}/admin?start=${s}&end=${e}&type=${t}&download=excel`);
}

/* =========================
   🔍 TRACK COMPLAINT BY ID
========================= */
function track() {
  let cid = document.getElementById("cid").value;

  fetch(API + "/track?id=" + cid)
    .then(r => r.json())
    .then(data => {
      if (data.length) {
        let c = data[0];
        document.getElementById("res").innerHTML = `
          <div style="border:1px solid #ccc;padding:10px">
            <b>Status:</b> ${c.status}<br>
            <b>Type:</b> ${c.type}<br>
            <b>Remark:</b> ${c.description}
          </div>
        `;
      } else {
        document.getElementById("res").innerHTML = "No complaint found";
      }
    });
}

/* =========================
   🚪 LOGOUT
========================= */
function logout() {
  localStorage.removeItem("user");
  location.href = "index.html";
}
