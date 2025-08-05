
function loadCourses() {
  get("/courses/").then(courses => {
    const list = document.getElementById("course-list");
    list.innerHTML = courses.map(course =>
      `<p><strong>${course.title}</strong>: ${course.description}</p>`
    ).join("");
  });
}

document.getElementById("course-form").onsubmit = function(e) {
  e.preventDefault();

  const course = {
    title: document.getElementById("title").value,
    description: document.getElementById("description").value,
    objectives: document.getElementById("objectives").value,
    instructor: document.getElementById("instructor").value,
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value,
    visibility: document.getElementById("visibility").value,
    is_published: document.getElementById("is_published").checked
  };

  post("/courses/", course).then(data => {
    alert("Course created!");
    loadCourses();
    this.reset();
  });
};

window.onload = loadCourses;
