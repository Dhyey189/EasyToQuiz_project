# EasyToQuiz

It is a online Quiz Web App created using django frame work.

This project is at website : https://easytoquiz.pythonanywhere.com/EasyToQuiz/


## Features of EasyToQuiz

Users can create their account by signup. 

Users (test-taker) can create new quiz containing Questions with their Option for other users (students) and can also set answer if needed for particular quiz. 

Users (students) can give exam online and submit it.

User (quiz-owner) can see all responses with marks for particular students for particular quiz which he/she has created and consider it for evolution.

<b>1. Create Quiz :</b> Any logged in users can create quiz containing Questions with their Option. every creation of a quiz generates a unique quiz ID which will be mailed to the user for the future references.

<b>2. Quiz code :</b> As mentioned before every quiz have there unique ID. only using that other users can give the answer to that quiz and this ID also used by quiz owner for trekking answer of the quiz.

<b>3. On/Off Response :</b> If any quiz are created for examination purpose then the time for submission of quiz is very important. for that we added a button through which a quiz owner can stop accepting quiz submission. more on that feature we implemented it such that he/she can again tern it back if needed.

<b>4. Score Calculation :</b> There is an option for quiz owner to set answer for the quiz. if answer is set then there is a score calculator which calculates the correct answer out of marked answers and give the statistics about it.


More Details can be found in [project report](https://github.com/Dhyey189/EasyToQuiz_project/blob/main/Project_Report.pdf).

## Tech Stack

Used python Django Framework for backend and frontend and MySql for database.
