from flask import Flask, render_template, request

app = Flask(__name__)


items = [
    'Buy Food',
    'Go to Gym',
    'Watch Movie'
]


@app.route('/')
def index():
    return render_template('items.j2', items=items)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        todo_item = request.form['new_item']
        items.append(todo_item)
        return render_template('items.j2', items=items)
    return render_template('create.j2')


@app.route('/update/<int:item_id>', methods=('GET', 'POST'))
def update(item_id):
    if request.method == 'POST':
        updated_item = request.form['update_item']
        items[item_id] = updated_item
        return render_template('items.j2', items=items)
    return render_template('update.j2', item=items[item_id], item_id=item_id)


@app.route('/delete/<int:item_id>', methods=('GET', 'POST'))
def delete(item_id):
        items.pop(item_id)
        return render_template('items.j2', items=items)
