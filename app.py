from flask import Flask, render_template, request, redirect, url_for
import functions as fn
import os
import json
import base64

app = Flask(__name__)

# Load initial todos
todolist = fn.read_todos()

def get_logged_in_user():
    """
    Reads user information injected by Azure App Service Authentication
    """
    user = request.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")

    # Optional: Read full claims if needed
    principal = request.headers.get("X-MS-CLIENT-PRINCIPAL")

    if principal:
        decoded = base64.b64decode(principal)
        claims = json.loads(decoded)
        return user, claims

    return user, None


@app.route("/", methods=["GET", "POST"])
def index():
    global todolist

    user, claims = get_logged_in_user()

    if request.method == "POST":
        # Add new todo
        if "todo" in request.form:
            todo = request.form["todo"].strip()
            if todo:
                todolist.append(todo + "\n")
                fn.add_values(todolist)

        # Remove completed todos
        elif "remove" in request.form:
            todo_to_remove = request.form["remove"]
            todolist = [
                todo for todo in todolist
                if todo.strip() != todo_to_remove
            ]
            fn.add_values(todolist)

        return redirect(url_for('index'))

    return render_template(
        "index.html",
        todolist=todolist,
        user=user
    )


if __name__ == "__main__":
    app.run(debug=True)
