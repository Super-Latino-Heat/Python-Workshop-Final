# Python Flask Workshop
This workshop aims to provide you with the basic concepts of the [Flask Web Framework](https://flask.palletsprojects.com/) using Python. 
We'll build a very simple 'Todo List App' in order to be able to implement these concepts.

Let's start with the basics...

## Install Python
The commands to install Python are very simple, you can refer to this doc https://www.python.org/downloads/ in order to use the proper command for your OS. 
Once Python installed you can run the following command to check if the installation was succesful:

MacOS, Linux: `python3 --version`  
Windows: `python --version`

## Create your project
Let's create a new directory that will be our root work directory (ex: `flask_workshop/`).

### Virtual environment
In Python, it's good practice to set up a "virtual environment" for each project. This will isolate project dependencies, ensuring that different projects can have different versions of packages installed without conflicts.

### Create a virtual environment
To create a virtual environment just `cd` into your work directory (`flask_workshop/` in my example) and type the following command:

MacOS, Linux: `python3 -m venv .venv`  
Windows: `python -m venv .venv`

A new folder should appear at the route of your project (`.venv/`), all packages we install will be stored within it.
But first the virtual environment must be activated...

### Activate the virtual environment
To activate the virtual environment just type the following command:

MacOS, Linux: `. .venv/bin/activate`  
Windows: `.venv\Scripts\activate`

If the virtual environment is activated its name should appear in front of your command prompt like so:

`(.venv) sam@Ubuntu20-04:~/MyProject` &rarr; Note the `(.venv)` at the beginning.

(INFO: To deactivate the virtual environment just type: `deactivate`)

## Create Flask Application
Now that our virtual environment is activated we can install the package we need.

### Install Flask
Python comes with the `pip` package installer (like `npm` in node.js), this will allow us to easily install Flask just by typing this command:

`pip install Flask`

### Code (Hello World)
Let's test if everything is set up correctly by creating a simple "Hello World" app.

At the root of our project, create a python file (ex: `todo_app.py`);  
Import Flask and initialize the application:

```python
from flask import Flask

app = Flask(__name__)
```

Then, add the following function:

```python
@app.route("/")
def index():
    return "<p>Hello, World!</p>"
```
This is our first route, when we'll browse our application at its root (`@app.route("/")`) the plain HTML (as a string) should be rendered.

### Run the server
In your terminal type the following command: 

`flask --app todo_app --debug run`

The `--debug` instruction allows to avoid having to restart the server every time we apply changes in the code.

You can now visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

If 'Hello World' is rendered correctly, we can pass to the next step where we can use Templates !

## Templates

Because returning HTML directly from a Python function is not very optimal we can start rendering HTML pages using templates.

### Update project structure
At the root of the project create a `templates/` directory.
Flask uses the [Jinja template engine](https://jinja.palletsprojects.com/) that is very similar to "blade" in Laravel. With Jinja the html files will have the extension `.j2`.  
Note: I recommend installing "Better Jinja" extension on VS Code to get syntax highlighting.

Within `templates/` create this `base.j2` file:

```html
<!doctype html>
<title>Flask App</title>
<h1>Hello, World!</h1>
```

### Update code

In `todo_app.py` import the `render_template` method:

```python
from flask import Flask, render_template
```

Also, update the `index()` function in order to render our HTML file using `render_template()`:

```python
@app.route('/')
def index():
    return render_template('base.j2')
```

At this point, your project structure should look like this:

```
├── .venv
├── templates
│   └── base.j2
└── todo_app.py
```
You can visit [http://127.0.0.1:5000](http://127.0.0.1:5000) again to see the changes (<u>refresh the page</u>). You should still see the "Hello World" message but the main difference is that now we're rendering a HTML file instead of a simple string.

## ToDo App
Now that we can render HTML files we can go a little further and implement our application.

### ToDo Item List
Let's create a simple Python list (like the Array in javascript) containing our list of items.
In `todo_app.py` add the following list (<u>it must be added before the `index()` routing function</u>):

```python
items = [
    'Buy Food',
    'Go to Gym',
    'Prepare workshop'
]
```
Now we can pass the `items` list in the "context" of our `index()` function.  
We will also replace the name of the html file passed by `items.j2` (we will create this file in the next step):

```python
@app.route('/')
def index():
    return render_template('items.j2', items=items)
```

Let's replace the `base.j2` content with this code:
```jinja
<!doctype html>
<title>{% block title %}{% endblock %} - ToDo App</title>
<nav>
  <h1>ToDo App Logo</h1>
</nav>

<section>

  <header>
    {% block header %}{% endblock %}
  </header>

  {% block content %}{% endblock %}

</section>
```

This represent our base HTML structure that will be implemented by all HTML(.j2) files. All blocks content (`{% block <name> %}`) will be replaced by the content of all HTML files that <u>extend</u> `base.j2` file.  


In `templates/`, let's create `items.j2`:
```jinja
{% extends 'base.j2' %}

{% block header %}
  <h1>{% block title %}Items{% endblock %}</h1>
{% endblock %}

{% block content %}
<div>
    <a class="action" href="{{ url_for('create')}}">Add New Item</a>
  </div>
  {% for item in items %}
    <article class="item">
        <div>
          <p class="body">{{ item }}</p>
        </div>
    </article>
    {% if not loop.last %}
      <hr>
    {% endif %}
  {% endfor %}
{% endblock %}
```

Here we can notice a few things: 
* How this file "extends" from `base.j2`, this will tell Flask to replace all blocks content with the ones in `items.j2`.  
* How we can pass a route function in the `<a>` element (we will create the `create()` function in the next step)
* The implementation of a for loop that iterates through the items of the list we've passed to the context of `index()` function.

Let's also create a `create.j2` file the same way we've created `items.j2`:

```jinja
{% extends 'base.j2' %}

{% block header %}
  <h1>{% block title %}New ToDo Item{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post" action="{{ url_for('create') }}">
    <input name="new_item" type="text" placeholder="Insert text here">
    <input type="submit" value="Add">
  </form>
{% endblock %}
```

Finally, let's update `todo_app.py` and add:
* the `request` object import statement (at the beginning of the file):
```python
from flask import Flask, render_template, request
```
* the function `create()`:

```python
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        todo_item = request.form['new_item']
        items.append(todo_item)
        return render_template('items.j2', items=items)
    return render_template('create.j2')
```

This routing function accepts two methods (`GET` and `POST`), if the method selected is `POST` we'll add a new item to the `items` list and then browse back to `items.j2`. If the method is `GET` we'll be directed to `create.j2` (See `items.j2`).

The same way, we will create the 'Update' part of the code.

First the html (jinja) file `update.j2`:

```jinja
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}New ToDo Item{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="update_item">Update Item:</label>
    <input name="update_item" value="{{ item }}">
    <input type="submit" value="Update">
  </form>
{% endblock %}
```

Then, we add the related method in `todo_app.py`:

```python
@app.route('/update/<int:item_id>', methods=('GET', 'POST'))
def update(item_id):
    if request.method == 'POST':
        updated_item = request.form['update_item']
        items[item_id] = updated_item
        return render_template('items.j2', items=items)
    return render_template('update.j2', item=items[item_id], item_id=item_id)
```

The project structure at this point:
```
├── .venv
├── templates
│   ├── base.j2
│   ├── create.j2
│   ├── items.j2
│   └── update.j2
└── todo_app.py
```

<u>Done! you can test the application!</u>

## Challenge - Your Turn to Code
Now that you have all the basics of the app, try to implement the following:

### Delete Item
* Add a 'Delete' button close to each item in `items.j2`.
* Write the `delete()` function in `todo_app.py`.

Here some doc links that might be helpful:
* [W3s Python tutorial](https://www.w3schools.com/python/)
* [Flask doc](https://flask.palletsprojects.com/en/3.0.x/)

## DB implementation (Bonus)
For those who are interested, we've created another branch in this repo that implements this same ToDo App connected to a Database.  
We've used [SQLite](https://docs.python.org/3/library/sqlite3.html) that is already provided by Python.
The code is simplified and straight forward, the main goal is just to give you the basics to show you how to connect a DB with a Flask application and perform basic SQL operations.
