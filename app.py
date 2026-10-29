from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

books = []
issued_books = []
next_book_id = 1
next_issue_id = 1

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System - V2</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 35px auto;
            padding: 20px;
            background: #f4f7fb;
        }
        .card {
            background: white;
            padding: 22px;
            margin: 20px 0;
            border-radius: 10px;
        }
        input, select, button {
            padding: 10px;
            margin: 6px 0;
        }
        input, select {
            width: 95%;
        }
        button {
            background: #2457a7;
            color: white;
            border: none;
            cursor: pointer;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background: #e8eef9;
        }
        .message {
            padding: 10px;
            background: #e2f5e8;
        }
    </style>
</head>
<body>
    <h1>Library Management System - V2</h1>
    <p>Manage books and issue them to students.</p>

    {% if message %}
        <p class="message">{{ message }}</p>
    {% endif %}

    <div class="card">
        <h2>Add Books</h2>
        <form method="POST" action="/add">
            <label>Book title:</label><br>
            <input name="title" required maxlength="120"><br>

            <label>Author:</label><br>
            <input name="author" required maxlength="100"><br>

            <label>Number of copies:</label><br>
            <input name="copies" type="number" min="1" max="10000"
                   value="1" required><br>

            <button type="submit">Add Book</button>
        </form>
    </div>

    <div class="card">
        <h2>Available Books</h2>
        {% if books %}
        <table>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Author</th>
                <th>Available Copies</th>
                <th>Issue Book</th>
            </tr>
            {% for book in books %}
            <tr>
                <td>{{ book.id }}</td>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.copies }}</td>
                <td>
                    {% if book.copies > 0 %}
                    <form method="POST" action="/issue">
                        <input type="hidden" name="book_id"
                               value="{{ book.id }}">
                        <input name="student" placeholder="Student name"
                               required maxlength="100">
                        <button type="submit">Issue</button>
                    </form>
                    {% else %}
                    No copies available
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No books have been added yet.</p>
        {% endif %}
    </div>

    <div class="card">
        <h2>Issued Books History</h2>
        {% if issued_books %}
        <table>
            <tr>
                <th>Issue ID</th>
                <th>Book</th>
                <th>Student</th>
                <th>Status</th>
            </tr>
            {% for item in issued_books %}
            <tr>
                <td>{{ item.id }}</td>
                <td>{{ item.title }}</td>
                <td>{{ item.student }}</td>
                <td>Issued</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No books have been issued yet.</p>
        {% endif %}
    </div>
</body>
</html>
"""


def render_home(message=""):
    return render_template_string(
        HTML,
        books=books,
        issued_books=issued_books,
        message=message
    )


@app.route("/")
def home():
    return render_home()


@app.route("/add", methods=["POST"])
def add_book():
    global next_book_id

    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()

    try:
        copies = int(request.form.get("copies", "1"))
    except ValueError:
        return "Copies must be a whole number.", 400

    if not title or not author or not 1 <= copies <= 10000:
        return "Please provide valid book details.", 400

    books.append({
        "id": next_book_id,
        "title": title,
        "author": author,
        "copies": copies
    })

    next_book_id += 1
    return redirect(url_for("home"))


@app.route("/issue", methods=["POST"])
def issue_book():
    global next_issue_id

    try:
        book_id = int(request.form.get("book_id", "0"))
    except ValueError:
        return "Invalid book ID.", 400

    student = request.form.get("student", "").strip()

    if not student:
        return "Student name is required.", 400

    book = next(
        (item for item in books if item["id"] == book_id),
        None
    )

    if book is None:
        return "Book not found.", 404

    if book["copies"] <= 0:
        return "No copies are available.", 400

    book["copies"] -= 1

    issued_books.append({
        "id": next_issue_id,
        "book_id": book["id"],
        "title": book["title"],
        "student": student,
        "status": "issued"
    })

    next_issue_id += 1
    return redirect(url_for("home"))


@app.get("/health")
def health():
    return {"status": "healthy", "version": "v2"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)