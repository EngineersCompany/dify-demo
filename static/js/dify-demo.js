async function askDify() {
  const query = document.getElementById("user-query").value;
  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  const data = await res.json();
  document.getElementById("output").innerText = data.answer;
}