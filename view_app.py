import os
import json
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
DATA_FILE = 'data.json'

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# HTML template
viewer_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Customer Viewer</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f4f4f4; }
        table { width: 90%; margin: auto; border-collapse: collapse; background: #fff; }
        th, td { padding: 10px; border: 1px solid #ccc; }
        th { background: #007bff; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        a, button { padding: 5px 10px; margin: 2px; text-decoration: none; border: none; border-radius: 5px; }
        .edit { background: orange; color: white; }
        .delete { background: red; color: white; }
    </style>
</head>
<body>
    <h2 style="text-align:center;">Customer Details</h2>
    <table>
        <tr><th>#</th><th>Name</th><th>Email</th><th>Phone</th><th>Address</th><th>Actions</th></tr>
        {% for i, customer in enumerate(data) %}
        <tr>
            <td>{{ i+1 }}</td>
            <td>{{ customer['name'] }}</td>
            <td>{{ customer['email'] }}</td>
            <td>{{ customer['phone'] }}</td>
            <td>{{ customer['address'] }}</td>
            <td>
                <a href="/edit/{{ i }}" class="edit">Edit</a>
                <a href="/delete/{{ i }}" class="delete" onclick="return confirm('Delete this entry?');">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

edit_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Edit Customer</title>
</head>
<body>
    <h2>Edit Customer</h2>
    <form method="POST">
        <label>Name:</label><br>
        <input type="text" name="name" value="{{ customer['name'] }}" required><br>
        <label>Email:</label><br>
        <input type="email" name="email" value="{{ customer['email'] }}" required><br>
        <label>Phone:</label><br>
        <input type="text" name="phone" value="{{ customer['phone'] }}" required><br>
        <label>Address:</label><br>
        <input type="text" name="address" value="{{ customer['address'] }}" required><br><br>
        <input type="submit" value="Update">
    </form>
    <p><a href="/">Back</a></p>
</body>
</html>
'''

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    data = load_data()
    return render_template_string(viewer_template, data=data)

@app.route('/delete/<int:index>')
def delete(index):
    data = load_data()
    if 0 <= index < len(data):
        del data[index]
        save_data(data)
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    data = load_data()
    if request.method == 'POST':
        data[index] = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address']
        }
        save_data(data)
        return redirect(url_for('index'))
    return render_template_string(edit_template, customer=data[index])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
