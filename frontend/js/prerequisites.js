document.getElementById("prereq-form").onsubmit = function (e) {
  e.preventDefault();

  const structureId = document.getElementById("structure_id").value;
  const prerequisiteId = document.getElementById("prerequisite_id").value;

  const formData = new FormData();
  formData.append("structure_id", structureId);
  formData.append("prerequisite_id", prerequisiteId);

  fetch("http://127.0.0.1:8000/courses/structure/prerequisite/", {
    method: "POST",
    body: formData
  })
    .then(res => {
      if (!res.ok) {
        throw new Error("Failed to add prerequisite");
      }
      return res.json();
    })
    .then(data => {
      alert("Prerequisite set successfully!");
      document.getElementById("prereq-form").reset();
    })
    .catch(err => {
      alert("Error: " + err.message);
    });
};

function viewPrerequisites() {
  const structureId = document.getElementById("view_structure_id").value;
  const list = document.getElementById("prereq-list");
  list.innerHTML = "";

  fetch(`http://127.0.0.1:8000/courses/structure/${structureId}/prerequisites/`)
    .then(res => {
      if (!res.ok) {
        throw new Error("Could not fetch prerequisites");
      }
      return res.json();
    })
    .then(data => {
      if (data.length === 0) {
        list.innerHTML = "<li>No prerequisites found.</li>";
      } else {
        data.forEach(pr => {
          const item = document.createElement("li");
          item.textContent = `Structure ${pr.structure_id} depends on Structure ${pr.prerequisite_id}`;
          list.appendChild(item);
        });
      }
    })
    .catch(err => {
      alert("Error: " + err.message);
    });
}
