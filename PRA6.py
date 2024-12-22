from flask import Flask, render_template_string, request

app = Flask(__name__)

def matrix_chain_order(dims):
    n = len(dims) - 1
    m = [[0 for _ in range(n)] for _ in range(n)]
    s = [[0 for _ in range(n)] for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s

def optimal_parenthesization(s, i, j):
    if i == j:
        return f"M{i+1}"
    else:
        return f"({optimal_parenthesization(s, i, s[i][j])} x {optimal_parenthesization(s, s[i][j] + 1, j)})"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    parenthesis = None
    m_table = None
    s_table = None
    num_matrices = 0  # Initialize to avoid UnboundLocalError

    if request.method == "POST":
        num_matrices = int(request.form["num_matrices"])
        dims = list(map(int, request.form["dimensions"].split(',')))

        if len(dims) == num_matrices + 1:
            m, s = matrix_chain_order(dims)
            result = m[0][-1]
            parenthesis = optimal_parenthesization(s, 0, num_matrices - 1)
            m_table = m
            s_table = s

    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matrix Chain Multiplication</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #ff7e5f, #feb47b, #ff6f61, #d76d77, #3a7bd5, #00d2d3);
            background-size: 600% 600%;
            animation: gradientAnimation 16s ease infinite;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .container {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 500px;
            text-align: center;
            margin-bottom: 30px;
        }
        h1 {
            margin-bottom: 20px;
        }
        form {
            margin-bottom: 20px;
        }
        input, button {
            padding: 10px;
            margin: 10px 0;
            width: 100%;
            max-width: 100%;
            border-radius: 5px;
            border: none;
            outline: none;
        }
        button {
            background-color: #3a7bd5;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #00d2d3;
        }
        .output-container {
            margin-top: 30px;
            width: 100%;
            max-width: 800px;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: white;
            color: black;
            margin-left: auto;
            margin-right: auto;
        }
        th {
            background-color: #3a7bd5; /* Header row color */
            color: white;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Matrix Chain Multiplication</h1>
        <form method="POST">
            <label for="num_matrices">Enter Number of Matrices:</label><br><br>
            <input type="number" id="num_matrices" name="num_matrices" min="2" required><br><br>
            <label for="dimensions">Enter Matrix Dimensions (comma-separated):</label><br><br>
            <input type="text" id="dimensions" name="dimensions" placeholder="e.g., 5,10,3,12,5,50,6" required><br><br>
            <button type="submit">Calculate</button>
        </form>
    </div>

    {% if result is not none %}
    <div class="output-container">
        <h2>Minimum Number of Multiplications: {{ result }}</h2>
        <h2>Optimal Parenthesization: {{ parenthesis }}</h2>

        <h3>Dynamic Programming Table (m):</h3>
        <table>
            <tr>
                {% for j in range(num_matrices) %}
                    <th>M{{ j+1 }}</th>
                {% endfor %}
            </tr>
            {% for i in range(num_matrices) %}
                <tr>
                    {% for j in range(num_matrices) %}
                        <td>{{ m_table[i][j] if j >= i else '' }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>

        <h3>k Table (s):</h3>
        <table>
            <tr>
                {% for j in range(num_matrices) %}
                    <th>M{{ j+1 }}</th>
                {% endfor %}
            </tr>
            {% for i in range(num_matrices) %}
                <tr>
                    {% for j in range(num_matrices) %}
                        <td>{{ s_table[i][j] + 1 if j >= i else '' }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    </div>
    {% endif %}
</body>
</html>
''', result=result, parenthesis=parenthesis, m_table=m_table, s_table=s_table, num_matrices=num_matrices)

if __name__ == "__main__":
    app.run(debug=True)
