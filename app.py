from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route("/")
def show_survey_home():
    return render_template("survey.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def submit_answer():
    choice = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:q>")
def show_question(q):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != q):
        flash(f"Invalid question id: {q}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[q]
    return render_template("question.html", question_num = q, question=question)

@app.route("/complete")
def get_complete():
    return render_template("complete.html")