const API = "/api/hello";

/* =========================
   🟢 REGISTER
========================= */
function register() {
  fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      action: "register",
      name: name.value,
      email: email.value,
      password: pass.value
    })
  })
  .then(r => r.json())
  .then(d => alert(d.message));
}

/* =========================
   🔐 LOGIN
========================= */
function login() {
  fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      action: "login",
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
  fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      action: "complaint",
      email: document.getElementById("email").value,
      title: document.getElementById("title").value,
      description: document.getElementById("remark").value
    })
  })
  .then(r => r.json())
  .then(d => alert(d.message));
}

/* =========================
   🧑‍💼 ADMIN LOAD + FILTER
========================= */
function load() {
  let s = document.getElementById("start").value;
  let e = document.getElementById("end").value;
  let t = document.getElementById("type").value;

  fetch(`${API}?start=${s}&end=${e}&type=${t}`)
    .then(r => r.json())
    .then(data => {
      let html = "";

      data.forEach(c => {
        html += `
        <div style="border:1px solid #000;padding:10px;margin:10px">
          <b>${c.title}</b><br>
          Category: ${c.category}<br>
          Status: ${c.status}
        </div>
        `;
      });

      document.getElementById("data").innerHTML = html;
    });
}

/* =========================
   📥 DOWNLOAD EXCEL
========================= */
function download() {
  let s = document.getElementById("start").value;
  let e = document.getElementById("end").value;
  let t = document.getElementById("type").value;

  window.open(`${API}?start=${s}&end=${e}&type=${t}&download=excel`);
}

/* =========================
   🔍 TRACK COMPLAINT
========================= */
function track() {
  let cid = document.getElementById("cid").value;

  fetch(`${API}?id=${cid}`)
    .then(r => r.json())
    .then(data => {
      if (data.length) {
        let c = data[0];
        document.getElementById("res").innerHTML = `
          <div>
            Status: ${c.status}<br>
            Category: ${c.category}
          </div>
        `;
      } else {
        document.getElementById("res").innerHTML = "Not found";
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
