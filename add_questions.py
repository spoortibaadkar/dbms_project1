from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.quizdb
questions_col = db.questions

new_questions = [
    {
        "id": 101,
        "question": "What is the capital of Germany?",
        "options": ["Berlin", "Munich", "Frankfurt", "Hamburg"],
        "answer": "Berlin"
    },
    {
        "id": 102,
        "question": "What is the chemical symbol for Gold?",
        "options": ["Au", "Ag", "Fe", "Pb"],
        "answer": "Au"
    },
    # ... add more questions here up to 15 or more
]

# Insert only if these questions are not already present (to avoid duplicates)
for q in new_questions:
    if questions_col.count_documents({"id": q["id"]}) == 0:
        questions_col.insert_one(q)

print("New questions inserted!")
