from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, create_table
from datetime import date

app = Flask(__name__)

# Create database table
create_table()


# Home page - display all beneficiaries
@app.route("/")
def index():
    connection = get_db_connection()

    beneficiaries = connection.execute(
        "SELECT * FROM beneficiaries ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        beneficiaries=beneficiaries
    )


# Add beneficiary
@app.route("/add", methods=["GET", "POST"])
def add_beneficiary():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]
        category = request.form["category"]
        assistance = request.form["assistance"]
        date_added = date.today().isoformat()

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO beneficiaries
            (name, age, gender, phone, address, category, assistance, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            gender,
            phone,
            address,
            category,
            assistance,
            date_added
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    return render_template("add.html")


# Search beneficiary
@app.route("/search")
def search():

    query = request.args.get("query", "")

    connection = get_db_connection()

    beneficiaries = connection.execute("""
        SELECT * FROM beneficiaries
        WHERE name LIKE ?
        OR phone LIKE ?
        OR category LIKE ?
    """, (
        "%" + query + "%",
        "%" + query + "%",
        "%" + query + "%"
    )).fetchall()

    connection.close()

    return render_template(
        "search.html",
        beneficiaries=beneficiaries,
        query=query
    )


# Edit beneficiary
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_beneficiary(id):

    connection = get_db_connection()

    beneficiary = connection.execute(
        "SELECT * FROM beneficiaries WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]
        category = request.form["category"]
        assistance = request.form["assistance"]

        connection = get_db_connection()

        connection.execute("""
            UPDATE beneficiaries
            SET name = ?,
                age = ?,
                gender = ?,
                phone = ?,
                address = ?,
                category = ?,
                assistance = ?
            WHERE id = ?
        """, (
            name,
            age,
            gender,
            phone,
            address,
            category,
            assistance,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        beneficiary=beneficiary
    )


# Delete beneficiary
@app.route("/delete/<int:id>")
def delete_beneficiary(id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM beneficiaries WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)