document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:8000/courses/")
    .then(res => res.json())
    .then(courses => {
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
          <p><strong>Start:</strong> ${course.start_date} → <strong>End:</strong> ${course.end_date}</p>
          <p><strong>Objectives:</strong> ${course.objectives}</p>
          <div class="resources" id="res-${course.id}">
            <p><strong>Resources:</strong></p>
            <p>Loading resources...</p>
          </div>
        `;

        container.appendChild(card);

        fetch(`http://127.0.0.1:8000/courses/structure/${course.id}/resources/`)
          .then(res => res.json())
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
            });
          })
          .catch(() => {
            const resBox = document.getElementById("res-" + course.id);
            resBox.innerHTML = "<p><em>Failed to load resources.</em></p>";
          });
      });
    })
    .catch(err => {
      document.getElementById("catalog-container").innerHTML =
        "<p>Error loading courses. Please try again later.</p>";
      console.error("Catalog load error:", err);
    });
});