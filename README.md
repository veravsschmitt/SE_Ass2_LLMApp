## Description of the project: STUDY BUDDY

**Core feature:** This is an application that turns a given pdf file with study notes, lecture slides or something like that into an interactive Q&A session to enhance learning. It will give one question at a time and for each question you can ask for a hint and also check if your given answer is correct or not. The Implementation of this program is in python and for the GUI tkinter was used. As the LLM is used OpenAI's gpt-4o-mini. ALso there are some shortcuts to be able to navigate through the running Q&A session without using the mouse: enter = check my answer; up = give me a hint, right = next question

**Enhancement:** To enhance the performance of the LLM I used a few-shot prompt. 

**Safety/robustness:** There are explicit rules what the LLM should and should not do to avoid attacks. As an example you can take the attack.pdf as an input and try to generate questions. Instead of following the attack it will state that it suspects an attack (at least for all the times I tried). Also all inputs get checked on their file type and length before sending it to the LLM and in case give the user error messages and the ability to change them. 

**Telemetry:** Information on latency, times and tokens will be printed on the terminal while using the application. 

**Architecture diagram:**



## How to run the project:

To run this project you need your own API-Key for OpenAI. Insert your API-Key in the designated marked spot at the top of the openAI_interface.py file.

After this the App can be started with one command. 
In this Repo there are two scripts (Linux: run.sh, Windows: run.bat ) which create a virtual enviroment, install all dependencies and load the data:  <br>
On Linux run "bash run.sh"  <br>
On Windows run ".\run.bat"
Hint: This application was developed on Linux, so on windows there can be some weird proportions or buttons not showing perfectly. 

All packages that need to be installed are listed in the requirements.txt. 
Additionally the following packages which are already included in the standard python package were used: 
- tkinter
- threading
- json
- re
- time
- datetime

After the virtual enviroment is set up and activated you can also run the app with "python app.py" and start the evaluation with "python eval.py".

The App will automatically be shown in an interavtive GUI Window. The additional information like metrics, timestamps and results of the evaluation will be printed in the terminal while it is running. 

If you want to interact with the app in eval_study_notes you will find examples for study notes which will be accepted and can be used to start a Q&A and test the app. 

## Evaluation 

In this repo you will find the file eval.py to evaluate how good the model can check if the given answers are correct or not. For this evaluation I gave example study_notes, questions and answers on different topics and measured if the application can tell if the answers given are correct or not. One of the study_notes even is in german, as I was curious if it still would be able to still work in the english Q&A, which it did. Normally it passed with 15/15 or 14/15 as it was sometimes struggeling with the Computer Graphics-3 test. But try yourself if you are interested.

## Known limits

- So far the evaluation is with a really small and specific dataset, this should be extended.
- The evaluation so far only evaluates how good the application can check the answers, not yet if the hints and questions are good. Here the evaluation should be extended.
- The application still takes some time to load questions, hints and answers. Here I could work on teh latency and also on the costs. This could also be nice as I then could allow longer pdfs and inputs, too. 
- The GUI is still not designed really nicely so in this regard a lot could be improved.
- Also it could be expanded for different files than only pdf.
- Sometimes it spoils the answer to the questions in the hints. This problem should be further worked on. 
- The pdf drop field works, but sometimes it needs a few trys to drop it. Maybe there is also a fix for this problem.
- On windows the proportions and location of the application and its features need to be adjusted. As I don't have a windows laptop this was not yet possible for me to do.  
