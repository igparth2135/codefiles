from flask import Flask, render_template_string, request
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
def calculate_pairs_loop():
    total_pairs = 0
    months = 12
    results = []
    for i in range(1, months + 1):
        formula = 2 ** i
        total_pairs = formula
        results.append((i, formula))
    return results, total_pairs
def calculate_pairs_recursion(month, current=1):
    if current > month:
        return [], 0
    formula = 2 ** current
    results = [(current, formula)]
    next_results, total_pairs = calculate_pairs_recursion(month, current + 1)
    results.extend(next_results)
    if current == month:
        total_pairs += formula
    return results, total_pairs
def generate_plot(results):
    months, pairs = zip(*results)  
    plt.figure(figsize=(10, 6))
    plt.plot(months, pairs, marker='o', linestyle='-', color='b')
    plt.xlabel('Month')
    plt.ylabel('Pairs Produced')
    plt.title('Pairs Produced Over Months')
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  
    plt.close()
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Choose Method</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        form {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        select, button {
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: calc(100% - 22px); 
        }
        button {
            background-color: #007BFF;
            color: #fff;
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <form action="/result" method="post">
        <h1>Choose a Method</h1>
        <label for="choice">Choose method:</label>
        <select name="choice" id="choice">
            <option value="1">FOR LOOP</option>
            <option value="2">FOR RECURSION</option>
        </select>
        <button type="submit">Submit</button>
    </form>
</body>
</html>

"""

result_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 160vh;
            margin: 0;
            flex-direction: column;
        }
        .content {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 800px;
            width: 100%;
        }
        h1 {
            margin-bottom: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        li {
            margin: 10px 0;
        }
        p {
            font-weight: bold;
            margin: 10px 0;
        }
        h2 {
            margin-top: 20px;
        }
        img {
            margin-top: 20px;
            max-width: 100%;
            height: auto;
        }
        a {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007BFF;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }
        a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Results for {{ method }}</h1>
        <ul>
            {% for month, pairs in results %}
            <li>For month {{ month }} pairs produced = {{ pairs }}</li>
            {% endfor %}
        </ul>
        <p>Total no. of pairs: {{ total_pairs }}</p>
        <h2>Graph of Pairs Produced</h2>
        <img src="data:image/png;base64,{{ img_data }}" alt="Pairs Produced Graph">
        <a href="/">Go back</a>
    </div>
</body>
</html>

"""
@app.route('/')
def index():
    return render_template_string(index_html)
@app.route('/result', methods=['POST'])
def result():
    choice = request.form.get('choice')
    if choice == '1':
        results, total_pairs = calculate_pairs_loop()
    elif choice == '2':
        results, total_pairs = calculate_pairs_recursion(12, 1)
    else:
        return "Invalid choice", 400
    img_base64 = generate_plot(results)
    return render_template_string(result_html, method='FOR LOOP' if choice == '1' else 'FOR RECURSION', results=results, total_pairs=total_pairs, img_data=img_base64)
if __name__ == '__main__':
    app.run(debug=True)
