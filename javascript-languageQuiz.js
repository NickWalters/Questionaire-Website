const startBtn = document.getElementById('start-btn');
const questionContainer = document.getElementById('question-container');

startBtn.addEventListener('click',startQuiz);


function startQuiz(){
startBtn.classList.add('hide')
questionContainer.classList.remove('hide');

}