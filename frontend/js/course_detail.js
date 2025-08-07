document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const courseId = params.get("id");

  if (!courseId) {
    alert("Course ID not found.");
    return;
  }

  // Fetch course details
  fetch(`http://127.0.0.1:8000/courses/${courseId}`)
    .then(res => res.json())
    .then(course => {
      document.getElementById("course-title").textContent = course.title;
      document.getElementById("course-description").textContent = course.description || "No description.";
      document.getElementById("course-objectives").textContent = course.objectives || "None";
      document.getElementById("course-instructor").textContent = course.instructor || "N/A";
      document.getElementById("course-dates").textContent = `${course.start_date || "?"} to ${course.end_date || "?"}`;
    });

  // Fetch course modules (structure)
  fetch(`http://127.0.0.1:8000/courses/${courseId}/structure/`)
    .then(res => res.json())
    .then(structures => {
      const container = document.getElementById("modules-container");
      if (structures.length === 0) {
        container.innerHTML = "<p>No modules available.</p>";
        return;
      }

      structures.forEach(s => {
        const div = document.createElement("div");
        div.className = "module";
        div.innerHTML = `
          <h3>${s.title}</h3>
          <p>${s.description || "No description."}</p>
          <div class="resources" id="res-${s.id}"><em>Loading resources...</em></div>
        `;
        container.appendChild(div);

        // Load resources for this module
        fetch(`http://127.0.0.1:8000/courses/structure/${s.id}/resources/`)
          .then(res => res.json())
          .then(resources => {
            const resBox = document.getElementById("res-" + s.id);
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
            });
          })
          .catch(() => {
            document.getElementById("res-" + s.id).innerHTML = "<p><em>Failed to load resources.</em></p>";
          });
      });
    })
    .catch(() => {
      document.getElementById("modules-container").innerHTML = "<p>Error loading modules.</p>";
    });
});
