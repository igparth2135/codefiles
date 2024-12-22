from flask import Flask, render_template_string, request
import numpy as np
app = Flask(__name__)
def tsp(graph):
    n = len(graph)
    dp = {}  
    def visit(city, visited):
        if visited == (1 << n) - 1:  
            return graph[city][0]         
        if (city, visited) in dp:
            return dp[(city, visited)]        
        ans = float('inf')
        for next_city in range(n):
            if visited & (1 << next_city) == 0:  
                ans = min(ans, graph[city][next_city] + visit(next_city, visited | (1 << next_city)))        
        dp[(city, visited)] = ans
        return ans    
    min_cost = visit(0, 1)    
    def get_path():
        path = []
        visited = 1
        city = 0        
        while visited != (1 << n) - 1:
            for next_city in range(n):
                if visited & (1 << next_city) == 0:
                    new_cost = graph[city][next_city] + visit(next_city, visited | (1 << next_city))
                    if new_cost == dp[(city, visited)]:
                        path.append((city, next_city))
                        visited |= (1 << next_city)
                        city = next_city
                        break        
        path.append((city, 0)) 
        return path    
    path = get_path()
    return min_cost, path
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TSP Solver</title>
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
        animation: gradient 10s ease infinite;
        background-size: 600% 600%;
        justify-content: center;
        align-items: center;
        min-height: 100vh;        
        margin: 0;
        padding: 0;
        color: #495057;
    }
.container {
        width: 90%;
        max-width: 900px;
        margin: 30px auto;
        padding: 20px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
        h2 {
            font-size: 30px;
            color: #4A90E2;
            margin-bottom: 30px;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            font-size: 16px;
            color: #333;
            text-align: left;
            margin-bottom: 10px;
            display: block;
        }
        textarea {
            width: 100%;
            height: 160px;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ccc;
            border-radius: 8px;
            box-sizing: border-box;
            margin-bottom: 20px;
            resize: none;
            transition: border-color 0.3s ease;
        }
        textarea:focus {
            border-color: #4A90E2;
            outline: none;
        }
        button {
            padding: 14px 24px;
            background-color: #4A90E2;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #357ABD;
        }
        .result {
            background: #F1F7FB;
            border: 2px solid #E1E8ED;
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: left;
        }
        .result h3 {
            margin-top: 0;
            color: #4A90E2;
            font-size: 22px;
        }
        .result ul {
            list-style-type: none;
            padding: 0;
            font-size: 16px;
        }
        .result ul li {
            padding: 8px 0;
            border-bottom: 1px solid #E1E8ED;
        }
        .result ul li:last-child {
            border-bottom: none;
        }
        .path {
            font-weight: bold;
            font-size: 18px;
            color: #333;
        }
        .error {
            color: #E74C3C;
            font-size: 16px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Traveling Salesman Problem Solver</h2>
        <form method="POST">
            <div>
                <label for="matrix">Enter distance matrix (comma-separated rows):</label>
                <textarea id="matrix" name="matrix">{{ matrix }}</textarea>
            </div>
            <button type="submit">Solve</button>
        </form>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        {% if min_cost is not none %}
        <div class="result">
            <h3>Solution</h3>
            <ul>
                {% for i in range(path|length - 1) %}
                    <li>{{ path[i][0] + 1 }} → {{ path[i][1] + 1 }} = {{ distances[path[i][0]][path[i][1]] }}</li>
                {% endfor %}
            </ul>
            <div class="path">
                <h4>Minimum Cost: <span>{{ min_cost }}</span></h4>
                <h4>Path Taken: 
                    {% for city in path %}
                        {{ city[0] + 1 }}{% if not loop.last %} → {% endif %}
                    {% endfor %}
                </h4>
            </div>
        </div>
        {% endif %}        
    </div>
</body>
</html>
'''
@app.route('/', methods=['GET', 'POST'])
def index():
    min_cost = None
    path = []
    matrix = ''
    distances = []
    error = None    
    if request.method == 'POST':
        try:
            input_matrix = request.form['matrix'].strip().split('\n')
            distances = [list(map(int, row.split(','))) for row in input_matrix]
            if len(distances) < 2 or any(len(row) != len(distances) for row in distances):
                raise ValueError("The matrix must be square and at least 2x2.")
            min_cost, path = tsp(distances)
            matrix = request.form['matrix']
        except Exception as e:
            error = f"Error: {str(e)}"    
    return render_template_string(HTML_TEMPLATE, min_cost=min_cost, path=path, distances=distances, matrix=matrix, error=error)
if __name__ == '__main__':
    app.run(debug=True)



#10, 20, 30, 10, 11
#15, 10, 16, 4, 2
#3, 5, 10, 2, 4
#19, 6, 18, 10, 3
#16, 4, 7, 16, 10