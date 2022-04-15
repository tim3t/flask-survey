from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def show_survey_home():
    return render_template("survey.html", survey=survey)

@app.route("/questions/<int:q>")
def show_question(q):
    question = survey.questions[q]
    return render_template("question.html", question_num = q, question=question)