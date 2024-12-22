from flask import Flask, request, render_template_string
import sys

app = Flask(__name__)

# Dijkstra's Algorithm Implementation
def dijkstra(graph, start):
    num_nodes = len(graph)
    distances = [sys.maxsize] * num_nodes
    distances[start] = 0
    visited = [False] * num_nodes
    previous = [-1] * num_nodes

    for _ in range(num_nodes):
        # Find the unvisited node with the smallest distance
        min_distance = sys.maxsize
        min_index = -1
        for i in range(num_nodes):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                min_index = i

        # Mark the node as visited
        visited[min_index] = True

        # Update distances to neighboring nodes
        for neighbor in range(num_nodes):
            if graph[min_index][neighbor] != sys.maxsize and not visited[neighbor]:
                new_distance = distances[min_index] + graph[min_index][neighbor]
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = min_index

    return distances, previous

def construct_path(previous, target, cities):
    path = []
    while target != -1:
        path.insert(0, cities[target])
        target = previous[target]
    return " → ".join(path)

# City names and cost matrix
cities = ['A', 'B', 'C', 'D', 'E']
graph = [
    [0, 20, 30, 35, 45],
    [sys.maxsize, 0, sys.maxsize, 15, 25],
    [sys.maxsize, sys.maxsize, 0, sys.maxsize, 25],
    [sys.maxsize, sys.maxsize, sys.maxsize, 0, 10],
    [sys.maxsize, sys.maxsize, sys.maxsize, sys.maxsize, 0],
]

@app.route('/')
def index():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Shortest Path Finder</title>
            <style>
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

    header {
 font-family: 'Arial', sans-serif;
        background: linear-gradient(135deg, #ff7e5f, #feb47b, #ff6f61, #d76d77, #3a7bd5, #00d2d3);
        animation: gradient 10s ease infinite;
        background-size: 600% 600%;
        justify-content: center;
        align-items: center;        
        color: Black;
        text-align: center;
        font-size: 1.5rem;
        letter-spacing: 1px;
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

    form {
        margin-bottom: 30px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    label {
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }

    input[type="text"] {
        padding: 12px;
        font-size: 16px;
        width: 100px;
        margin-top: 5px;
        border-radius: 4px;
        border: 1px solid #ccc;
        transition: border-color 0.3s ease;
    }

    input[type="text"]:focus {
        border-color: #007bff;
        outline: none;
    }

    button {
        padding: 12px 25px;
        font-size: 16px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #0056b3;
    }

    table {
        width: 100%;
        margin-top: 30px;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
    }

    th, td {
        padding: 14px;
        text-align: center;
        border: 1px solid #ddd;
    }

    th {
        background-color: #f8f9fa;
        font-weight: bold;
        color: #495057;
    }

    td {
        background-color: #fdfdfd;
        font-size: 14px;
    }

    tr:nth-child(even) td {
        background-color: #f1f1f1;
    }

    tr:hover td {
        background-color: #e9ecef;
    }

    .result {
        margin-top: 40px;
    }

    .result h3 {
        font-size: 1.5rem;
        margin-bottom: 15px;
        color: #007bff;
    }

    .form-group input, button {
        width: auto;
        margin-right: 10px;
    }
                                  #start_city {
    padding: 12px;
    font-size: 16px;
    width: 100%;
    margin-top: 5px;
    border-radius: 4px;
    border: 1px solid #ccc;
    transition: border-color 0.3s ease;
    background-color: #fff;
}

#start_city:focus {
    border-color: #007bff;
    outline: none;
}


    @media (max-width: 768px) {
        .container {
            width: 95%;
            padding: 15px;
        }

        table {
            font-size: 12px;
        }

        th, td {
            padding: 10px;
        }
    }            </style>
        </head>
        <body>
            <header>
                <h1>Find Shortest Path Between Cities</h1>
            </header>
            <div class="container">
                <h3 style="color: #007bff;">Cost Matrix:</h3>
                <table class="cost-matrix">
                    <tr>
                        <th></th>
                        <th>A</th>
                        <th>B</th>
                        <th>C</th>
                        <th>D</th>
                        <th>E</th>
                    </tr>
                    <tr>
                        <th>A</th>
                        <td>0</td>
                        <td>20</td>
                        <td>30</td>
                        <td>35</td>
                        <td>45</td>
                    </tr>
                    <tr>
                        <th>B</th>
                        <td>∞</td>
                        <td>0</td>
                        <td>∞</td>
                        <td>15</td>
                        <td>25</td>
                    </tr>
                    <tr>
                        <th>C</th>
                        <td>∞</td>
                        <td>∞</td>
                        <td>0</td>
                        <td>∞</td>
                        <td>25</td>
                    </tr>
                    <tr>
                        <th>D</th>
                        <td>∞</td>
                        <td>∞</td>
                        <td>∞</td>
                        <td>0</td>
                        <td>10</td>
                    </tr>
                    <tr>
                        <th>E</th>
                        <td>∞</td>
                        <td>∞</td>
                        <td>∞</td>
                        <td>∞</td>
                        <td>0</td>
                    </tr>
                </table>
                                  <br>
                <form action="/calculate" method="POST">
                    <label for="start_city">Enter the Starting City:</label>
                    <select name="start_city" id="start_city">
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                        <option value="E">E</option>
                    </select>
                                  <br><br>
                    <button type="submit">Calculate</button>
                </form>
            </div>
        </body>
        </html>
    """)

@app.route('/calculate', methods=['POST'])
def calculate():
    start_city = request.form['start_city']
    start_node = cities.index(start_city)

    # Get the shortest distances and paths using Dijkstra's algorithm
    distances, previous = dijkstra(graph, start_node)

    result = []
    for i in range(len(cities)):
        if distances[i] == sys.maxsize:
            result.append((cities[i], '∞', 'No path'))
        else:
            path = construct_path(previous, i, cities)
            result.append((cities[i], distances[i], path))

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Shortest Path Results</title>
            <style>
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

                table {
                    width: 100%;
                    margin-top: 20px;
                    border-collapse: collapse;
                }

                th, td {
                    padding: 12px;
                    text-align: center;
                    border: 1px solid #ddd;
                }

                th {
                    background-color: #f8f9fa;
                    font-weight: bold;
                    color: #495057;
                }

                td {
                    background-color: #fdfdfd;
                }

                tr:nth-child(even) td {
                    background-color: #f1f1f1;
                }

                .back-button {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }

                .back-button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            
            <div class="container">
            <h1>Shortest Path from {{ start_city }}</h1>

                <table>
                    <tr>
                        <th>Destination</th>
                        <th>Cost</th>
                        <th>Path</th>
                    </tr>
                    {% for city, cost, path in result %}
                        <tr>
                            <td>{{ city }}</td>
                            <td>{{ cost }}</td>
                            <td>{{ path }}</td>
                        </tr>
                    {% endfor %}
                </table>
                <a href="/" class="back-button">Back</a>
            </div>
        </body>
        </html>
    """, result=result, start_city=start_city)

if __name__ == '__main__':
    app.run(debug=True)
