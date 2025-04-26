rom flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('SELECT * FROM records')
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add():
    type = request.form['type']
    amount = request.form['amount']
    description = request.form['description']
    date = request.form['date']

    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('INSERT INTO records (type, amount, description, date) VALUES (?, ?, ?, ?)',
              (type, amount, description, date))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('DELETE FROM records WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
