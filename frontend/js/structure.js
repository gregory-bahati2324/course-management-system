
let currentCourseId = null;

function loadStructure() {
  const input = document.getElementById("course_id");
  currentCourseId = parseInt(input.value);

  if (!currentCourseId) {
    alert("Please enter a valid Course ID.");
    return;
  }

  get("/courses/" + currentCourseId + "/structure/").then(items => {
    const list = document.getElementById("structure-list");

    if (items.length === 0) {
      list.innerHTML = "<p>No structure found for this course.</p>";
      return;
    }

    list.innerHTML = items.map(item => `
      <div>
        <strong>${item.type.toUpperCase()}:</strong> ${item.title}<br>
        Content: ${item.content}<br>
        Order: ${item.order}
        <hr>
      </div>
    `).join("");
  });
}

document.getElementById("structure-form").onsubmit = function(e) {
  e.preventDefault();

  if (!currentCourseId) {
    alert("Load a course first!");
    return;
  }

  const structure = {
    course_id: currentCourseId,
    type: document.getElementById("type").value,
    title: document.getElementById("title").value,
    content: document.getElementById("content").value,
    order: parseInt(document.getElementById("order").value)
  };

  post("/courses/structure/", structure).then(data => {
    alert("Structure added!");
    loadStructure();
    this.reset();
  });
};
