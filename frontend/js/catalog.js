function viewDetails(courseId) {
  window.location.href = `course_detail.html?id=${courseId}`;
}

function enroll(courseId, buttonElement) {
  alert("Enrolled in course ID: " + courseId);
  buttonElement.textContent = "Enrolled";
  buttonElement.disabled = true;
  buttonElement.style.backgroundColor = "gray";
}

document.addEventListener("DOMContentLoaded", () => {
  get("/courses/").then(courses => {
    const container = document.getElementById("catalog-container");

    if (courses.length === 0) {
      container.innerHTML = "<p>No courses available right now.</p>";
      return;
    }

    courses.forEach(course => {
      const card = document.createElement("div");
      card.className = "course-card";

      card.innerHTML = `
        <h2>${course.title}</h2>
        <p><strong>Instructor:</strong> ${course.instructor}</p>
        <p><strong>Start:</strong> ${course.start_date || "TBD"} → <strong>End:</strong> ${course.end_date || "TBD"}</p>
        <p><strong>Objectives:</strong> ${course.objectives || "None"}</p>

        <div class="button-group">
          <button onclick="enroll('${course.id}', this)">Enroll</button>
          <button onclick="viewDetails(${course.id})">View Details</button>
        </div>

        <div class="resources" id="res-${course.id}">
          <p><strong>Resources:</strong></p>
          <p>Loading resources...</p>
        </div>
      `;

      container.appendChild(card);

      // Load resources for each course
      get(`/courses/structure/${course.id}/resources/`)
        .then(resources => {
          const resBox = document.getElementById("res-" + course.id);
          if (resources.length === 0) {
            resBox.innerHTML = "<p><em>No resources uploaded yet.</em></p>";
            return;
          }

          resBox.innerHTML = "<p><strong>Resources:</strong></p>";
          resources.forEach(r => {
            const link = document.createElement("a");
            link.href = r.file_url || "#";
            link.textContent = r.title || r.file_url;
            link.target = "_blank";
            resBox.appendChild(link);
            resBox.appendChild(document.createElement("br"));
          });
        })
        .catch(() => {
          const resBox = document.getElementById("res-" + course.id);
          resBox.innerHTML = "<p><em>Failed to load resources.</em></p>";
        });
    });
  }).catch(err => {
    document.getElementById("catalog-container").innerHTML =
      "<p>Error loading courses. Please try again later.</p>";
    console.error("Catalog load error:", err);
  });
});
