from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, peer TEXT, availability BOOLEAN)')
    print("Table created successfully")
    conn.close()

init_db()

peers = ['Albert Einstein', 
    'Isaac Newton', 
    'Galileo Galilei', 
    'Marie Curie', 
    'Nikola Tesla', 
    'Thomas Edison', 
    'Alan Turing']
manager_availability = {peer: False for peer in peers}

@app.route('/')
def index():
    return render_template('index.html', peers=peers)

@app.route('/submit', methods=['POST'])
def submit():
    peer = request.form['peer']
    availability = request.form['availability'] == 'yes'
    manager_availability[peer] = availability

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO history (peer, availability) VALUES (?, ?)", (peer, availability))
        con.commit()

    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', availability=manager_availability)

@app.route('/history')
def history():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM history WHERE date >= datetime('now', '-1 month')")
        history_data = cur.fetchall()
    return render_template('history.html', history=history_data)

@app.route('/delete_history')
def delete_history():
    return render_template('delete_history.html')

@app.route('/delete_history_confirm', methods=['POST'])
def delete_history_confirm():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM history")
        con.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
