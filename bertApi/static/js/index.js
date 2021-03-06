function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

document
  .getElementById("form-wrapper")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = await getSimilarQuestions();
    console.log(data);
    var ulwrapper = document.getElementById("ques-list");
    ulwrapper.innerHTML = "";
    for (var i in data) {
      var item = `<li class="list-group-item">${data[i].question}</li>`;
      ulwrapper.innerHTML += item;
    }
  });
async function getSimilarQuestions() {
  var queryUrl = "http://127.0.0.1:8000/api/queryQuestion/";
  var text = document.getElementById("queryQuestion").value;
  settings = {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      queryQuestion: text,
    }),
  };
  response = await fetch(queryUrl, settings);
  var data = await response.json();
  return data;
}
