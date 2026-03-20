function load(){
let s=start.value
let e=end.value
let t=type.value

fetch(`/api/admin?start=${s}&end=${e}&type=${t}`)
.then(r=>r.json())
.then(d=>{
let html=""
d.forEach(c=>{
html+=`
<div style="border:1px solid #ccc;margin:10px;padding:10px">
<b>${c.name}</b> (${c.type})<br>
${c.title}<br>
Status: ${c.status}<br>
<button onclick="update('${c.id}')">Resolve</button>
</div>
`
})
data.innerHTML=html
})
}

function download(){
let s=start.value
let e=end.value
let t=type.value

window.open(`/api/admin?start=${s}&end=${e}&type=${t}&download=excel`)
}
