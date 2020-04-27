var question_index = 0;
var score = 0;

const images = [
'taiwan-languageQuiz.jpg','australia-languageQuiz.jpg','norway-languageQuiz.jpg','colombia-languageQuiz.jpg','pakistan-languageQuiz.jpg','ukraine-languageQuiz.jpg','malaysia-languageQuiz.jpg','mexico-languageQuiz.jpg','iran-languageQuiz.jpg','indonesia-languageQuiz.jpg'
]

const questions = [
    {
        question: 'What is the offical language of Taiwan',
        answers:[ 'Taiwanese','Japanese','Mandarin','Cantonese'], answer: 'Mandarin'
    },
    {
        question: 'What is offical language of Australia',
        answers:[ 'English', 'German', 'Korean', 'Russian'], answer: 'English'
    },
    {
        question: 'What is a offical language of Norway ',
        answers:[ 'German', 'Spanish','English','Romani'], answer: 'Romani'
    },
    {
        question: 'What is the offical language of Colombia ',
        answers:[ 'Spanish', 'Irish','Dutch','French'], answer: 'Spanish'
    },
    {
        question: 'What is a offical language of Pakistan ',
        answers:[ 'Perish', 'Hindi','Arabic','Urdu'], answer: 'Urdu'
    },
    {
        question: 'What is the offical language of Ukraine ',
        answers:[ 'Ukrainian', 'Russian','Greenlandic','Galician'], answer: 'Ukrainian'
    },
    {
        question: 'What is a offical language of Malaysia ',
        answers:[ 'Malaysian', 'Malayense','Mandarin','Malay'], answer: 'Malay'
    },
    {
        question: 'What is a offical language of Mexico ',
        answers:[ 'Spanish', 'Mexian','Portuguese','Welsh'], answer: 'Spanish'
    },
    {
        question: 'What is a offical language of Iran ',
        answers:[ 'Arabic', 'Hebrew','Persian','Hindi'], answer: 'Persian'
    },
    {
        question: 'What is a offical language of Indonesia ',
        answers:[ 'Malay', 'Indonesia','Mandarin','thai'], answer: 'Indonesia'
    }
    
]

function correctAnswer(choice){
    return choice === questions[question_index].answer; 
}

function isEnded() {
    return questions.length === question_index;
}

function newQuestion(answer){
    if(correctAnswer(answer)){
        score++;
    } 
    question_index++;
}

function populate(){
    if(isEnded()){
        showScores();
    }
    else{

        //shows image
        var image = document.getElementById("image");
        image.src = images[question_index];
        
        //shows question
        document.getElementById("p1").innerHTML = questions[question_index].question;

        //show choices
        for( var i = 0; i<4; i++){
            document.getElementById("btn"+i).innerHTML = questions[question_index].answers[i];
            selectedAnswer("btn" +i, questions[question_index].answers[i]);
        }
        showProgress();
    }
}

function selectedAnswer(id,answer){    
    var button = document.getElementById(id);
    button.onclick = function() {
        
        newQuestion(answer);
        populate();
    }

}

function showProgress() {
    var position = question_index +1;
    document.getElementById("question-index").innerHTML = "Question " + position  + " of " + questions.length;
    document.getElementById("current-score").innerHTML = "score: " + score +"/"+ position;
}


function showScores(){
    document.getElementById("initial-div").classList.add("hide");
    document.getElementById("final-div").classList.remove("hide");
    document.getElementById("final-score").innerHTML = score + "/" + questions.length;
}

populate();

