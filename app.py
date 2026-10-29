from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

books = []
next_book_id = 1

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System - V1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f4f7fb;
        }
        .card {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
        }
        input, button {
            padding: 10px;
            margin: 6px 0;
        }
        input {
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
            padding: 12px;
            text-align: left;
        }
        th {
            background: #e8eef9;
        }
    </style>
</head>
<body>
    <h1>Library Management System - V1</h1>
    <h2>Add Books</h2>

    <div class="card">
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
                <th>Copies</th>
            </tr>
            {% for book in books %}
            <tr>
                <td>{{ book.id }}</td>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.copies }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No books have been added yet.</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, books=books)


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


@app.get("/health")
def health():
    return {"status": "healthy", "version": "v1"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)