from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql!evapharma'
app.config['MYSQL_DB'] = 'manager_tracker'
mysql = MySQL(app)

peers = {
    'Albert Einstein', 
    'Isaac Newton', 
    'Galileo Galilei', 
    'Marie Curie', 
    'Nikola Tesla', 
    'Thomas Edison', 
    'Alan Turing'
}
manager_availability = {peer: False for peer in peers}

@app.route('/')
def index():
    return render_template('index.html', peers=peers)

@app.route('/submit', methods=['POST'])
def submit():
    peer = request.form['peer']
    availability = request.form['availability'] == 'yes'
    manager_availability[peer] = availability

    # Save to history
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO history (peer, availability) VALUES (%s, %s)", (peer, availability))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', availability=manager_availability)

@app.route('/history')
def history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM history WHERE date >= NOW() - INTERVAL 1 MONTH")
    history_data = cur.fetchall()
    cur.close()
    return render_template('history.html', history=history_data)

@app.route('/delete_history')
def delete_history():
    return render_template('delete_history.html')

@app.route('/delete_history_confirm', methods=['POST'])
def delete_history_confirm():
    print("Delete history request received")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM history")
    mysql.connection.commit()
    cur.close()
    print("History deleted successfully")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
