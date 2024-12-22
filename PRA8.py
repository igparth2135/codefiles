from flask import Flask, render_template_string, request
app = Flask(__name__)
def practical_8(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for i in range(m + 1)]  
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])    
    lcs = []
    i = m
    j = n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1            
    return lcs[::-1], L
def validate(sequence):
    sequence = sequence.strip().strip('<>').replace(' ', '')
    return sequence.split(',')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seq1 = validate(request.form['sequence1'])
        seq2 = validate(request.form['sequence2'])
        if not seq1 or not seq2:
            return render_template_string(INDEX_HTML, error="Please enter valid character sequences.")        
        lcs, table = practical_8(seq1, seq2)
        return render_template_string(RESULT_HTML, seq1=seq1, seq2=seq2, lcs=lcs, table=table)    
    return render_template_string(INDEX_HTML)
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Practical-8</title>
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
        input[type="text"] {
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
<h2>Enter Two Sequences: </h2>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
<form method="POST">
    <label for="sequence1">Sequence 1:</label>
    <input type="text" name="sequence1" required><br>
    <label for="sequence2">Sequence 2:</label>
    <input type="text" name="sequence2" required><br>
    <button type="submit">Find LCS</button>
</form>
</div>
</body>
</html>
"""

RESULT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Practical-8 Results</title>
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
        table {
            margin: 20px auto;
            border-collapse: collapse;
            width: 100%;
        }
        td {
            border: 1px solid #000000;
            padding: 8px;
            text-align: center;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            text-decoration: none;
            color: #007bff;
        }
    </style>
</head>
<body>
<div class="container">
<h2>Input Sequences</h2>
<p>P = {{ seq1 | join(', ') }}</p>
<p>Q = {{ seq2 | join(', ') }}</p>
<h3>Longest Common Subsequence:</h3>
<p>{{ lcs | join(', ') }}</p>
<h3>LCS Table:</h3>
<table>
{% for row in table %}
<tr>
    {% for col in row %}
    <td>{{ col }}</td>
    {% endfor %}
</tr>
{% endfor %}
</table>
<a href="/">Go Back</a>
</div>
</body>
</html>
"""
if __name__ == '__main__':
    app.run(debug=True)
