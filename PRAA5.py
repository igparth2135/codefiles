from flask import Flask, render_template_string, request
from collections import Counter

app = Flask(__name__)

def min_coins(coins, value):
    dp = [[float('inf')] * (value + 1) for _ in range(len(coins) + 1)]
    dp[0][0] = 0  

    for i in range(1, len(coins) + 1):
        dp[i][0] = 0  # 0 coins are needed to make 0 value
        for j in range(1, value + 1):
            if coins[i - 1] <= j:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - coins[i - 1]] + 1)
            else:
                dp[i][j] = dp[i - 1][j]

    # Replace float('inf') with '∞' for display purposes
    dp_for_display = [
        ['∞' if cell == float('inf') else cell for cell in row]
        for row in dp
    ]

    # Backtracking to find the coins used
    result = []
    row, col = len(coins), value
    while col > 0 and row > 0:
        if dp[row][col] != dp[row - 1][col]:
            result.append(coins[row - 1])
            col -= coins[row - 1]
        else:
            row -= 1

    coin_count = Counter(result)

    return dp[-1][-1], coin_count, dp_for_display

@app.route('/', methods=['GET', 'POST'])
def index():
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Minimum Coins Calculator</title>
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
            min-height: 100vh;  /* Change from height: 100vh; to min-height: 100vh; */
        }
        .container {
            background: rgba(255, 255, 255, 0.395);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #4a90e2;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-top: 20px;
            color: #4a4a4a;
            font-size: 1.1em;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }
        button {
            background-color: #50e3c2;
            border: none;
            color: white;
            padding: 10px 20px;
            margin-top: 20px;
            font-size: 1.2em;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background-color: #32a89b;
        }
        .result-table, .dp-table {
            margin-top: 20px;
            width: 100%;
            border-collapse: collapse;
        }
        .result-table th, .result-table td, .dp-table th, .dp-table td {
            padding: 12px;
            border: 1px solid #ddd;
            color: #333;
        }
        .result-table th, .dp-table th {
            background-color: #f8e71c;
        }
        .result-table td, .dp-table td {
            background-color: #f0f8ff;
        }
    </style>
    </head>
    <body>
        <div class="container">
            <h1>Minimum Coins Calculator</h1>
            <form method="POST">
                <label for="value">Value (Rs.):</label>
                <input type="text" id="value" name="value" required>
                <label for="coins">Coin Denominations (comma separated):</label>
                <input type="text" id="coins" name="coins" required>
                <button type="submit">Calculate</button>
            </form>

            {% if min_coin_count is not none %}
                <h2 style="color: #4a90e2; margin-top: 20px;">Result</h2>
                <p style="color: #333;">Minimum number of coins required: <strong>{{ min_coin_count }}</strong></p>
                <table class="result-table">
                    <thead>
                        <tr>
                            <th>Coin</th>
                            <th>Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for coin, quantity in coins_used.items() %}
                        <tr>
                            <td>{{ coin }}</td>
                            <td>{{ quantity }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>

                <h2 style="color: #4a90e2; margin-top: 20px;">Dynamic Programming Table</h2>
                <table class="dp-table">
                    <thead>
                        <tr>
                            <th>Coins</th>
                            {% for j in range(dp_table[0]|length) %}
                                <th>{{ j }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for i in range(dp_table|length) %}
                        <tr>
                            <td>{{ coins[i-1] if i > 0 else '' }}</td>
                            {% for j in range(dp_table[i]|length) %}
                            <td>{{ dp_table[i][j] }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% elif error %}
                <p style="color: #ff5f6d;">{{ error }}</p>
            {% endif %}
        </div>
    </body>
    </html>
    '''

    if request.method == 'POST':
        try:
            value = int(request.form['value'])
            coins = list(map(int, request.form['coins'].split(',')))
            min_coin_count, coins_used, dp_table = min_coins(coins, value)
            return render_template_string(html_template, min_coin_count=min_coin_count, coins_used=coins_used, dp_table=dp_table, coins=coins)
        except ValueError:
            return render_template_string(html_template, error="Please enter valid integers for value and coins.")

    return render_template_string(html_template, min_coin_count=None)

if __name__ == '__main__':
    app.run(debug=True)
