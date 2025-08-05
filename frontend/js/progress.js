document.getElementById("progress-form").onsubmit = function (e) {
  e.preventDefault();

  const student = document.getElementById("student").value.trim();
  const structureId = parseInt(document.getElementById("structure_id").value);

  if (!student || isNaN(structureId)) {
    alert("Please provide both student and structure ID.");
    return;
  }

  const formData = new FormData();
  formData.append("student", student);
  formData.append("structure_id", structureId);

  fetch("http://127.0.0.1:8000/courses/structure/progress/", {
    method: "POST",
    body: formData
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to save progress.");
      return res.json();
    })
    .then(() => {
      alert("Progress marked!");
      document.getElementById("progress-form").reset();
    })
    .catch(err => {
      alert("Error: " + err.message);
    });
};

function viewProgress() {
  const student = document.getElementById("progress_viewer").value.trim();
  const list = document.getElementById("progress-list");

  if (!student) {
    alert("Enter a student name to view progress.");
    return;
  }

  fetch("http://127.0.0.1:8000/courses/structure/progress/" + student)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch progress.");
      return res.json();
    })
    .then(items => {
      if (items.length === 0) {
        list.innerHTML = "<p>No progress recorded yet.</p>";
        return;
      }

      list.innerHTML = items
        .map(item => `<p><strong>${item.student}</strong> completed structure ID: ${item.structure_id}</p>`)
        .join("");
    })
    .catch(err => {
      alert("Error: " + err.message);
    });
}