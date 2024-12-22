from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key_for_flash_messages'

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

def practical_10(char_freq):
    nodes = [Node(char, freq) for char, freq in char_freq.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = Node(None, left.freq + right.freq, left, right)
        nodes.append(merged)
    return nodes[0]

def huffman(root, current_code="", codes={}):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
    huffman(root.left, current_code + "0", codes)
    huffman(root.right, current_code + "1", codes)
    return codes

def encode(text, codes):
    try:
        return ''.join([codes[char] for char in text])
    except KeyError:
        return "Error: Invalid character in input."

def decode(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root
    return decoded_text

@app.route('/', methods=['GET', 'POST'])
def index():
    huffman_codes = {}
    encoded_text = ""
    decoded_text = ""
    char_freq = {}
    if request.method == 'POST':
        try:
            freq_input = request.form['char_freq'].strip().split(',')
            for pair in freq_input:
                char, freq = pair.split(':')
                char = char.strip().upper()
                freq = float(freq.strip())
                char_freq[char] = freq
            huffman_tree = practical_10(char_freq)
            huffman_codes = huffman(huffman_tree)
            action = request.form['action']
            input_text = request.form['input_text'].strip().upper()
            if action == 'encode':
                encoded_text = encode(input_text, huffman_codes)
            elif action == 'decode':
                decoded_text = decode(input_text, huffman_tree)
        except ValueError as e:
            flash(f"Error: {e}. Please enter valid character frequencies.")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Unexpected Error: {e}")
            return redirect(url_for('index'))
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Huffman tree</title>
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
            h2 {
                margin-top: 20px;
            }
            p {
                margin: 15px 0; /* Add margin for spacing */
                padding: 10px;
                background: #f8f9fa; /* Light background for text */
                border-radius: 4px;
                border: 1px solid #ddd;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Huffman tree</h1>
            <h2>Enter Character Frequencies</h2>
            <form method="POST">
                <label for="char_freq">Character Frequencies (Format: A:0.5, B:0.35, C:0.1, ...):</label><br>
                <input type="text" id="char_freq" name="char_freq" required><br><br>
                <label for="input_text">Enter Text to Encode/Decode:</label><br>
                <input type="text" id="input_text" name="input_text" required><br><br>
                <button type="submit" name="action" value="encode">Encode</button><br><br>
                <button type="submit" name="action" value="decode">Decode</button>
            </form>
            <h2>Huffman Codes:</h2>
            <ul>
                {% for char, code in huffman_codes.items() %}
                <li>{{ char }}: {{ code }}</li>
                {% endfor %}
            </ul>
            <h2>Encoded Text</h2>
            <p>{{ encoded_text }}</p>
            <h2>Decoded Text</h2>
            <p>{{ decoded_text }}</p>
            {% with messages = get_flashed_messages() %}
            {% if messages %}
            <ul>
                {% for message in messages %}
                <li style="color: red;">{{ message }}</li>
                {% endfor %}
            </ul>
            {% endif %}
            {% endwith %}
        </div>
    </body>
    </html>
    ''', huffman_codes=huffman_codes, encoded_text=encoded_text, decoded_text=decoded_text)

if __name__ == '__main__':
    app.run(debug=True)
