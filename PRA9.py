from flask import Flask, render_template_string, request

app = Flask(__name__)

def practical_9(W, n, profits, weights):
    ratio = [(profits[i] / weights[i], i) for i in range(n)]
    ratio.sort(reverse=True, key=lambda x: x[0])
    max_value = 0
    taken_items = []
    
    for r, i in ratio:
        if weights[i] <= W:
            W -= weights[i]
            max_value += profits[i]
            taken_items.append((profits[i], weights[i], 1))
        else:
            max_value += r * W
            taken_items.append((profits[i], weights[i], W / weights[i]))
            break
            
    return max_value, taken_items

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        W = int(request.form['capacity'])
        n = int(request.form['items'])
        profits = list(map(int, request.form['profits'].split(',')))
        weights = list(map(int, request.form['weights'].split(',')))
        max_value, taken_items = practical_9(W, n, profits, weights)
        return render_template_string(RESULT_HTML, max_value=max_value, items=taken_items)
    return render_template_string(INDEX_HTML)

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>knapsack</title>
    <style>
        @keyframes gradient {
            0% { background: #ff7e5f; }
            20% { background: #feb47b; }
            40% { background: #ff6f61; }
            60% { background: #d76d77; }
            80% { background: #3a7bd5; }
            100% { background: #00d2d3; }
        }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #ff7e5f, #feb47b, #ff6f61, #d76d77, #3a7bd5, #00d2d3);
            background-size: 600% 600%;
            animation: gradient 10s ease infinite;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.8);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            width: 100%;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"], input[type="number"] {
            width: calc(100% - 16px);
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Knapsack</h1>
        <form method="POST">
            <label for="capacity">Knapsack Capacity (W):</label>
            <input type="number" id="capacity" name="capacity" required><br><br>
            <label for="items">Number of Items (n):</label>
            <input type="number" id="items" name="items" required><br><br>
            <label for="profits">Profits (comma-separated):</label>
            <input type="text" id="profits" name="profits" placeholder="e.g. 3,4,5,6" required><br><br>
            <label for="weights">Weights (comma-separated):</label>
            <input type="text" id="weights" name="weights" placeholder="e.g. 2,3,4,5" required><br><br>
            <button type="submit">Solve</button>
        </form>
    </div>
</body>
</html>
'''

RESULT_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>knapsack</title>
    <style>
        @keyframes gradient {
            0% { background: #ff7e5f; }
            20% { background: #feb47b; }
            40% { background: #ff6f61; }
            60% { background: #d76d77; }
            80% { background: #3a7bd5; }
            100% { background: #00d2d3; }
        }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #ff7e5f, #feb47b, #ff6f61, #d76d77, #3a7bd5, #00d2d3);
            background-size: 600% 600%;
            animation: gradient 10s ease infinite;
            color: #000000;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.8);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            width: 100%;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #000000;
            padding: 8px;
            text-align: center;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Result</h1>
        <p>Maximum Value: {{ max_value }}</p>
        <table>
            <tr>
                <th>Profit</th>
                <th>Weight</th>
                <th>Fraction Taken</th>
            </tr>
            {% for item in items %}
            <tr>
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
                <td>{{ item[2] }}</td>
            </tr>
            {% endfor %}
        </table>
        <a href="/">Go Back</a>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)