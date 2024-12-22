import os
from flask import Flask, request, jsonify, render_template_string
import time
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
client_income = 10000
def loop(n):
    total = 0
    for i in range(1, n + 1):
        total += client_income
    return total
def equation(n):
    total_income = n * client_income
    return total_income
def recursion(n):
    total_income = 0
    while n > 0:
        total_income += client_income
        n = n - 1
    return total_income
def measure_time(func, n):
    start_time = time.perf_counter()
    func(n)
    end_time = time.perf_counter()
    return end_time - start_time
def generate_plot(n_values, loop_times, equation_times, recursion_times):
    plt.figure(figsize=(12, 6))
    plt.plot(n_values, loop_times, label='Loop Method', marker='o', color='red')
    plt.plot(n_values, equation_times, label='Equation Method', marker='o', color='blue')
    plt.plot(n_values, recursion_times, label='Recursion Method', marker='o', color='green')
    plt.xlabel('Number of Clients (N)')
    plt.ylabel('Time (seconds)')
    plt.title('Comparative Analysis of Different Methods')
    plt.legend()
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    time_taken = None
    if request.method == 'POST':
        method = request.form.get('method')
        n = int(request.form.get('n'))
        if method == 'loop':
            result = loop(n)
            time_taken = measure_time(loop, n)
        elif method == 'equation':
            result = equation(n)
            time_taken = measure_time(equation, n)
        elif method == 'recursion':
            result = recursion(n)
            time_taken = measure_time(recursion, n)
        else:
            return jsonify({'error': 'Invalid method'}), 400
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Income Calculation</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f8ff;
        color: #333;
        margin: 0;
        padding: 0;
    }
    h1, h2 {
        color: #2e8b57;
        text-align: center;
    }
    form {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    label {
        display: block;
        margin: 10px 0 5px;
        font-weight: bold;
    }
    select, input[type="number"], input[type="submit"] {
        display: block;
        width: 100%;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    input[type="submit"] {
        background-color: #2e8b57;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    input[type="submit"]:hover {
        background-color: #3cb371;
    }
    #result {
        text-align: center;
        margin: 20px 0;
    }
    #plot {
        text-align: center;
        margin: 20px 0;
    }
    button {
        padding: 10px 20px;
        text-align: center;
        margin-left: 710px ;
        border: none;
        background-color: #4682b4;
        color: white;
        font-size: 16px;
        cursor: pointer;
        border-radius: 4px;
    }
    button:hover {
        background-color: #4169e1;
    }
</style>
</head>
<body>
<h1>Income Calculation Methods</h1>
<form action="/" method="post">
<label for="method">Select Calculation Method:</label>
<select id="method" name="method">
<option value="loop">Loop</option>
<option value="equation">Equation</option>
<option value="recursion">Recursion</option>
</select><br>
<label for="n">Number of Clients:</label>
<input type="number" id="n" name="n" min="1" required><br>
<input type="submit" value="Calculate">
</form>
<h2>Calculated Results</h2>
<div id="result">
{% if result is not none %}
<p>Result: {{ result }}</p>
<p>Time Taken: {{ time_taken }} seconds</p>
{% endif %}
</div>
<h2>Performance Plot</h2>
<button onclick="loadPlot()">Load Plot</button>
<div id="plot"></div>
<script>
function loadPlot() {
    fetch('/plot')
    .then(response => response.json())
    .then(data => {
        const plotDiv = document.getElementById('plot');
        const img = document.createElement('img');
        img.src = 'data:image/png;base64,' + data.plot;
        plotDiv.innerHTML = '';
        plotDiv.appendChild(img);
    });
}
</script>
</body>
</html>
''', result=result, time_taken=time_taken)
@app.route('/plot', methods=['GET'])
def plot():
    n_values = [10, 100, 1000, 5000, 10000]
    loop_times = [measure_time(loop, n) for n in n_values]
    equation_times = [measure_time(equation, n) for n in n_values]
    recursion_times = [measure_time(recursion, n) for n in n_values]
    img_base64 = generate_plot(n_values, loop_times, equation_times, recursion_times)
    return jsonify({'message': "Plot generated", 'plot': img_base64})
if __name__ == "__main__":
    app.run(debug=True)
