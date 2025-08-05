
const BASE_URL = "http://127.0.0.1:8000";

// This sends a GET request
function get(path) {
  return fetch(BASE_URL + path).then(res => res.json());
}

// This sends a POST request
function post(path, data) {
  return fetch(BASE_URL + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }).then(res => res.json());
}
