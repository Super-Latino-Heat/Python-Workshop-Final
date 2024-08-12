from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = 'todo.db'


def create_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, task TEXT)''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, task FROM items')
    items = c.fetchall()
    conn.close()
    return render_template('items.j2', items=items)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        todo_item = request.form['new_item']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO items (task) VALUES (?)', (todo_item,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.j2')


def get_item(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    item = c.execute('SELECT * FROM items WHERE id = (?)', (id,)).fetchone()
    conn.close()
    return item


@app.route('/update/<int:item_id>', methods=('GET', 'POST'))
def update(item_id):
    item = get_item(item_id)
    if request.method == 'POST':
        updated_item = request.form['update_item']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('UPDATE items SET task=(?) WHERE id = (?)', (updated_item, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update.j2', item=item, item_id=item_id)


@app.route('/delete/<int:item_id>', methods=('GET', 'POST'))
def delete(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    items = c.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('items.j2', items=items)


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
