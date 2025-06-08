from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "quiz_secret"

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client.quizdb
questions_col = db.questions
scores_col = db.scores

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start', methods=['POST'])
def start_quiz():
    session['username'] = request.form.get("username")
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    questions = list(questions_col.find({}, {"_id": 0}))
    return render_template("quiz.html", questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    answers = request.form
    questions = list(questions_col.find({}, {"_id": 0}))
    correct = 0
    results = []

    for q in questions:
        qid = str(q["id"])
        user_answer = answers.get(qid)
        is_correct = (user_answer == q["answer"])
        if is_correct:
            correct += 1
        results.append({
            "question": q["question"],
            "user_answer": user_answer,
            "correct_answer": q["answer"],
            "is_correct": is_correct
        })

    scores_col.insert_one({
        "username": session.get('username'),
        "score": correct,
        "total": len(questions)
    })

    return render_template("result.html", score=correct, total=len(questions), results=results)

@app.route('/review')
def review():
    user_scores = list(scores_col.find({}, {"_id": 0}))
    usernames = list({entry['username'] for entry in user_scores})  # Unique usernames
    return render_template("review.html", scores=user_scores, users=usernames)

if __name__ == '__main__':
    app.run(debug=True)
