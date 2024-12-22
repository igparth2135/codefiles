from flask import Flask, render_template_string, request
import matplotlib.pyplot as plt
import io
import base64
import random
app = Flask(__name__)
def linear_search(arr, target_value, key):
    iterations = 0
    for item in arr:
        iterations += 1
        if item[key] == target_value:
            return iterations, item
    return iterations, None
def binary_search(arr, target_value, key, low, high):
    iterations = 0
    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        if arr[mid][key] == target_value:
            return iterations, arr[mid]
        elif arr[mid][key] > target_value:
            high = mid - 1
        else:
            low = mid + 1
    return iterations, None
def generate_employee_data(n):
    return [{'ID': i, 'Name': f'Employee{i}', 'Salary': random.randint(30000, 120000),
             'Age': random.randint(22, 60), 'Mobile': f'123-456-789{i%10}'} for i in range(n)]
@app.route('/', methods=['GET', 'POST'])
def index():
    ns = [100, 500, 1000, 5000, 10000]
    linear_times_best = []
    linear_times_avg = []
    linear_times_worst = []
    binary_times_best = []
    binary_times_avg = []
    binary_times_worst = []  
    for n in ns:
        data = generate_employee_data(n)
        sorted_data = sorted(data, key=lambda x: x['Salary'])
        target_salary = random.choice(data)['Salary']        
        linear_iterations, _ = linear_search(data, data[0]['Salary'], 'Salary')
        binary_iterations, _ = binary_search(sorted_data, sorted_data[0]['Salary'], 'Salary', 0, len(sorted_data) - 1)
        linear_times_best.append(linear_iterations)
        binary_times_best.append(binary_iterations)        
        linear_iterations, _ = linear_search(data, data[-1]['Salary'], 'Salary')
        binary_iterations, _ = binary_search(sorted_data, sorted_data[-1]['Salary'], 'Salary', 0, len(sorted_data) - 1)
        linear_times_worst.append(linear_iterations)
        binary_times_worst.append(binary_iterations)        
        linear_iterations, _ = linear_search(data, target_salary, 'Salary')
        binary_iterations, _ = binary_search(sorted_data, target_salary, 'Salary', 0, len(sorted_data) - 1)
        linear_times_avg.append(linear_iterations)
        binary_times_avg.append(binary_iterations)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(ns, linear_times_best, 'o-', label='Linear Search Best Case', color='tab:blue')
    ax1.plot(ns, linear_times_avg, 's-', label='Linear Search Average Case', color='tab:green')
    ax1.plot(ns, linear_times_worst, 'd-', label='Linear Search Worst Case', color='tab:red')
    ax1.set_xlabel('Number of Employees (n)')
    ax1.set_ylabel('Linear Search Iterations')
    ax1.set_title('Linear Search Iterations for Different Cases')
    ax1.legend()
    ax1.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url_linear = base64.b64encode(img.getvalue()).decode()
    plt.close()
    fig, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(ns, binary_times_best, 'o-', label='Binary Search Best Case', color='tab:blue')
    ax2.plot(ns, binary_times_avg, 's-', label='Binary Search Average Case', color='tab:green')
    ax2.plot(ns, binary_times_worst, 'd-', label='Binary Search Worst Case', color='tab:red')
    ax2.set_xlabel('Number of Employees (n)')
    ax2.set_ylabel('Binary Search Iterations')
    ax2.set_title('Binary Search Iterations for Different Cases')  
    ax2.legend()
    ax2.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url_binary = base64.b64encode(img.getvalue()).decode()
    plt.close()
    table_data = [
        {
            'number_of_employees': n,
            'linear_best': lb,
            'linear_avg': la,
            'linear_worst': lw,
            'binary_best': bb,
            'binary_avg': ba,
            'binary_worst': bw
        }
        for n, lb, la, lw, bb, ba, bw in zip(ns, linear_times_best, linear_times_avg, linear_times_worst, binary_times_best, binary_times_avg, binary_times_worst)
    ]

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search Iterations Comparison</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #e0f7fa;
                color: #000000;
            }
            h1 {
                text-align: center;
                color: #00796b;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .form-container {
                text-align: center;
                margin-top: 20px;
            }
            .chart-container {
                text-align: center;
                margin-top: 30px;
            }
            table {
                width: 90%;
                margin: 20px auto;
                border-collapse: collapse;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
                background-color: #ffffff;
            }
            th, td {
                padding: 15px;
                text-align: center;
                border-bottom: 1px solid #00796b;
            }
            th {
                background-color: #00796b;
                color: white;
                font-size: 1.2em;
            }
            td {
                background-color: #f1f8e9;
                font-size: 1.1em;
            }
            img {
                width: 85%;
                height: auto;
                border: 2px solid #00796b;
                margin: 10px 0;
            }
            button {
                background-color: #00796b;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 1.1em;
                cursor: pointer;
                transition: background-color 0.3s ease;
                border-radius: 5px;
            }
            button:hover {
                background-color: #004d40;
            }
        </style>
    </head>
    <body>
        <h1>Search Iterations Comparison for Linear and Binary Search</h1>
        <div class="form-container">
            <form method="post">
                <button type="submit">Generate Plots and Data</button>
            </form>
        </div>
        {% if plot_url_linear %}
        <div class="chart-container">
            <h2>Linear Search Iterations</h2>
            <img src="data:image/png;base64,{{ plot_url_linear }}" alt="Linear Search Iterations">
        </div>
        {% endif %}
        {% if plot_url_binary %}
        <div class="chart-container">
            <h2>Binary Search Iterations</h2>
            <img src="data:image/png;base64,{{ plot_url_binary }}" alt="Binary Search Iterations">
        </div>
        {% endif %}
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Number of Employees</th>
                        <th>Linear Search Best Case</th>
                        <th>Linear Search Average Case</th>
                        <th>Linear Search Worst Case</th>
                        <th>Binary Search Best Case</th>
                        <th>Binary Search Average Case</th>
                        <th>Binary Search Worst Case</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in table_data %}
                    <tr>
                        <td>{{ row.number_of_employees }}</td>
                        <td>{{ row.linear_best }}</td>
                        <td>{{ row.linear_avg }}</td>
                        <td>{{ row.linear_worst }}</td>
                        <td>{{ row.binary_best }}</td>
                        <td>{{ row.binary_avg }}</td>
                        <td>{{ row.binary_worst }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''

    return render_template_string(html_template, plot_url_linear=plot_url_linear, plot_url_binary=plot_url_binary, table_data=table_data)
if __name__ == '__main__':
    app.run(debug=True)
