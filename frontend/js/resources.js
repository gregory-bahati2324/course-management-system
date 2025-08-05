let currentStructureId = null;

function loadResources() {
  const id = parseInt(document.getElementById("structure_id").value);
  if (!id) {
    alert("Please enter a valid structure ID.");
    return;
  }

  currentStructureId = id;

  get("/courses/structure/" + id + "/resources/").then(resources => {
    const list = document.getElementById("resource-list");

    if (!resources.length) {
      list.innerHTML = "<p>No resources found.</p>";
      return;
    }

    list.innerHTML = resources.map(r => {
      const fileLink = r.url
        ? `<a href="${r.url}" target="_blank">${r.title}</a>`
        : r.title;
      return `<div>
        <strong>${r.type.toUpperCase()}</strong>: ${fileLink}<br>
        ${r.notes || ""}
        <hr>
      </div>`;
    }).join("");
  });
}

document.getElementById("upload-form").onsubmit = function(e) {
  e.preventDefault();

  if (!currentStructureId) {
    alert("Load a structure first!");
    return;
  }

  const formData = new FormData();
  formData.append("structure_id", currentStructureId);
  formData.append("title", document.getElementById("resource_title").value);
  formData.append("type", document.getElementById("resource_type").value);
  formData.append("notes", document.getElementById("resource_notes").value);

  const url = document.getElementById("resource_url").value;
  if (url) {
    formData.append("url", url);
  }

  const file = document.getElementById("resource_file").files[0];
  if (file) {
    formData.append("file", file);
  }

  fetch("http://127.0.0.1:8000/courses/structure/upload/", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    alert("Resource uploaded!");
    loadResources();
    this.reset();
  });
};
