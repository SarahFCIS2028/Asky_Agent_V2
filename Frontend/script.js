let searchForm = document.querySelector("#searchForm");
let quickSearch = document.querySelectorAll(".topic");
let quiz;
let dark = false;
let first = false;
let mode = "beginner";
let data;

const darkMode = {
  "--BG": "#242220",
  "--Heading": "#e8e3dd",
  "--text": "#d5cec6",
  "--black": "#ffffff",
  "--subTitles": "#9a9691",
  "--correct": "#63b866",
  "--wrong": "#d95c5c",
  "--borderQuestion": "#625d58",
  "--card": "#302d2a",
  "--white": "black",
  "--blue": "#626cff",
  '--inputBG': '#2A2624',
  "--img": "url(AskyDark.png)"
};

const lightMode = {
  "--BG": "#d5cec6",
  "--Heading": "#494949",
  "--text": "#4d4d4d",
  "--black": "black",
  "--subTitles": "#929292",
  "--correct": "#60b663",
  "--wrong": "#d65757",
  "--borderQuestion": "#89837d",
  "--card": "#e8e3dd",
  "--white": "white",
  "--blue": "rgb(3, 3, 162)",
   '--inputBG': '#F2EFE9',
  "--img": "url(Asky.png)"
};


function changeDisplayMode() {
  if (!dark)
    Object.entries(darkMode).forEach(([variable, value]) => {
      document.documentElement.style.setProperty(variable, value);
    });
  else {
    Object.entries(lightMode).forEach(([variable, value]) => {
      document.documentElement.style.setProperty(variable, value);
    });
  }
  dark = !dark;
  console.log(dark)
}

quickSearch.forEach(elm => {
  let searchBar = document.querySelector("#Search");

  elm.addEventListener("click", () => {
    searchBar.value = elm.id;
    searchForm.requestSubmit();
  })
});


searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  let topicName = document.querySelector("#Search").value;

  if (topicName == "") {
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/asky", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        topic: topicName,
        mode: mode
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    data = await response.json();

    console.log("Backend response:", data);

    Rearange();
    CardModal();

  } catch (error) {
    console.error("Error:", error);
  }
});

function Rearange() {
  if (first) {
    first = true;
    return;
  }
  else {
    document.querySelector(".body").style.gridTemplateRows = " 75vh 10vh"

    let greet = document.querySelector(".greeting");
    let beg = document.querySelector("#beg");
    let Ac = document.querySelector("#Ac");
    let topics = document.querySelectorAll(".topic");
    let searchBox = document.querySelector("#searchForm");

    beg.classList.add("beg");
    Ac.classList.add("Ac");
    greet.style.opacity = 0;

    topics.forEach(element => {
      element.style.opacity = 0;
    });

    searchBox.classList.add("searchAnim")

    setTimeout(() => {
      Ac.style.display = "none";
      beg.style.display = "none";
      topics.forEach(element => {
        element.style.display = "none";
      });
    }, 500)
    document.querySelector(".body").style.height = "100%";
  }
}

function CardModal() {
  let greet = document.querySelector(".greeting");
  let content = ``;
  content += ` <section class="card" >

                <header>
                    <h5>${data.topic}</h5>
                    <div class="modeChang">
                        <div class="selected ${mode}">${capitalizeFirstLetter(mode)}</div>

                        <span onclick="changemode('beginner')" class="lightText">Beginner</span>
                        <span onclick="changemode('academic')" class="darkText">Academic</span>

                    </div>
                </header>
                <p id="Summary">${data.summary}</p>

                <section class="dataBoxs">
                    <div class="box">
                        <h6>Word Count</h6> <span>${data.reading_metrics.word_count}</span>
                    </div>
                    <div class="box">
                        <h6>Reading Time</h6> <span>${data.reading_metrics.reading_time_minutes} min</span>
                    </div>
                    <div class="box">
                        <h6>Complexity</h6> <span>${data.reading_metrics.complexity}</span>
                    </div>

                </section>
                <h6 id="TopicR">Related Topics</h6>
                <section class="related">
                    <div class="Rtopic">${data.related_topics[0]}</div>
                    <div class="Rtopic">${data.related_topics[1]}</div>
                    <div class="Rtopic">${data.related_topics[2]}</div>
                </section>
                <button class="Generate" onclick="generateQuiz();">Generate Quiz</button>
            </section>`;

  setTimeout(() => {
    greet.style.margin = 0;
    greet.style.opacity = 1;
    greet.innerHTML = content;

  }, 500);


}

function generateQuiz() {
  let greet = document.querySelector(".greeting");
  let content = ``;
  let quiz = data.quiz.questions;
  content += `
    <section class="cardQ">
      <header>
        <h5>Roman Empire</h5>
        <div class="modeChang">
          <div class="selected ${mode}">${capitalizeFirstLetter(mode)}</div>

          <span onclick="changemode('beginner')" class="lightText">Beginner</span>
          <span onclick="changemode('academic')" class="darkText">Academic</span>

        </div>
      </header>
      
      <section class="quizCard">
      <form class="options-container">`;

  quiz.forEach(element => {

    content += ` <p class="question">Q${element.id} :  ${element.question}</p>     `
    element.options.forEach(e => {
      content += `
          <label class="option-item">
            <input type="radio" name="question${element.id}" value="${e}">
            <span class="custom-radio"></span>
            <span class="option-text">${e}</span>
          </label>
        `
    });

  });

  content += `
        </form>
      </section>

      <button type="submit" class="submit-btn">Submit</button>
    </section>`

  greet.innerHTML = content;
}

function changemode(newmode) {
  mode = newmode;
  if (!first) {
    if (newmode == "academic") {
      document.querySelector(".selected").classList.add("academic");
      document.querySelector(".selected").classList.remove("beginner");

    } else {
      document.querySelector(".selected").classList.add("beginner");
      document.querySelector(".selected").classList.remove("academic");

    }
    document.querySelector(".selected").innerHTML = capitalizeFirstLetter(mode);

  }
  searchForm.requestSubmit();
}

function capitalizeFirstLetter(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}


function checkQuiz(answers) {
  let quiz = data.quiz.questions;
  console.log(answers)
  let score = 0;
  let i = 0;
  quiz.forEach(e => {
    if (e.correct_answer == answers[i])
      score++;
    i++;
  }
  )
  document.querySelector(".submit-btn").remove();
  document.querySelector(".score").innerHTML = `<span class="ScoreDesign">${score} / 5</span>`;
}