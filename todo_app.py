import matplotlib
matplotlib.use('Agg') 

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
DB_NAME = 'todo.db'

def create_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items 
                 (id INTEGER PRIMARY KEY, 
                  task TEXT, 
                  done BOOLEAN DEFAULT 0, 
                  in_progress BOOLEAN DEFAULT 0)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, task, done, in_progress FROM items')
    items = c.fetchall()
    
    # Stats
    c.execute('SELECT COUNT(*) FROM items WHERE done = 1')
    done_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM items WHERE in_progress = 1 AND done = 0')
    in_progress_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM items WHERE in_progress = 0 AND done = 0')
    todo_count = c.fetchone()[0]
    
    conn.close()
    
    stats = {
        'done': done_count,
        'in_progress': in_progress_count,
        'todo': todo_count
    }
    
    pie_chart, bar_chart = generate_charts(stats)
    
    return render_template('items.j2', items=items, pie_chart=pie_chart, bar_chart=bar_chart)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        todo_item = request.form['new_item']
        in_progress = 'in_progress' in request.form
        done = 'done' in request.form
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO items (task, done, in_progress) VALUES (?, ?, ?)', (todo_item, done, in_progress))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.j2')

def get_item(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    item = c.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    conn.close()
    return item

@app.route('/update/<int:item_id>', methods=('GET', 'POST'))
def update(item_id):
    item = get_item(item_id)
    if request.method == 'POST':
        updated_item = request.form['update_item']
        done = 'done' in request.form
        in_progress = 'in_progress' in request.form
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('UPDATE items SET task=?, done=?, in_progress=? WHERE id = ?', 
                  (updated_item, done, in_progress, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update.j2', item=item)

@app.route('/delete/<int:item_id>', methods=('GET', 'POST'))
def delete(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    items = c.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('items.j2', items=items)

def generate_charts(stats):
    # Pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([stats['done'], stats['in_progress'], stats['todo']], 
           labels=['Done', 'In Progress', 'To Do'],
           autopct='%1.1f%%',
           colors=['#4CAF50', '#FFA500', '#2196F3'])
    ax.set_title('Task Status Distribution')
    #Buffer
    pie_buffer = BytesIO()
    fig.savefig(pie_buffer, format='png')
    pie_buffer.seek(0)
    pie_chart = base64.b64encode(pie_buffer.getvalue()).decode()
    plt.close(fig)

    # Bar chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.bar(['Done', 'In Progress', 'To Do'], 
           [stats['done'], stats['in_progress'], stats['todo']],
           color=['#4CAF50', '#FFA500', '#2196F3'])
    ax.set_title('Task Status Count')
    ax.set_ylabel('Number of Tasks')
    #Buffer
    bar_buffer = BytesIO()
    plt.savefig(bar_buffer, format='png')
    bar_buffer.seek(0)
    bar_chart = base64.b64encode(bar_buffer.getvalue()).decode()
    plt.close()

    return pie_chart, bar_chart

if __name__ == '__main__':
    create_database()
    app.run(debug=True)

