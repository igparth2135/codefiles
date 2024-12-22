from flask import Flask, render_template_string, request
import time
import random
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
def BubbleSort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
def SelectionSort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
def InsertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
def MeasureTime(sort_function, arr):
    start_time = time.time()
    sort_function(arr)
    end_time = time.time()
    return end_time - start_time
def generate_plot(sizes, bubble_times, selection_times, insertion_times):
    plt.figure(figsize=(12, 8))
    plt.plot(sizes, bubble_times, label="Bubble Sort", marker='o')
    plt.plot(sizes, selection_times, label="Selection Sort", marker='o')
    plt.plot(sizes, insertion_times, label="Insertion Sort", marker='o')
    plt.xlabel('List Size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Sorting Algorithm Performance')
    plt.legend()
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url
@app.route('/', methods=['GET', 'POST'])
def index():
    plot_url = None
    if request.method == 'POST':
        sizes_str = request.form.get('sizes', '100,200,300,400,500')
        sizes = [int(size) for size in sizes_str.split(',')]
        bubble_times = []
        selection_times = []
        insertion_times = []
        for size in sizes:
            arr = [random.randint(0, 10000) for _ in range(size)]
            arr_copy = arr.copy()
            bubble_times.append(MeasureTime(BubbleSort, arr_copy))
            arr_copy = arr.copy()
            selection_times.append(MeasureTime(SelectionSort, arr_copy))
            arr_copy = arr.copy()
            insertion_times.append(MeasureTime(InsertionSort, arr_copy))
        plot_url = generate_plot(sizes, bubble_times, selection_times, insertion_times)
    html = '''
    <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sorting Algorithm Performance</title>
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background: linear-gradient(-45deg, #ff7e5f, #feb47b, #ff6f61, #d76d77, #3a7bd5, #00d2d3);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #333;
    }
    h1 {
        color: #ffffff;
        text-align: center;
        margin-top: 50px;
        font-size: 3em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 20px;
        padding: 30px;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: 0 auto;
    }
    label {
        font-size: 1.5em;
        color: #333;
        margin-bottom: 15px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    input[type="text"] {
        padding: 12px;
        border: 2px solid #ddd;
        border-radius: 8px;
        width: 100%;
        max-width: 500px;
        margin-bottom: 20px;
        font-size: 1.2em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    button {
        background: linear-gradient(to right, #ff7e5f, #feb47b);
        color: #fff;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1.2em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: background 0.3s ease;
    }
    button:hover {
        background: linear-gradient(to right, #feb47b, #ff7e5f);
    }
    h2 {
        color: #333;
        text-align: center;
        margin-top: 30px;
        font-size: 2em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    img {
        display: block;
        margin: 0 auto;
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    @keyframes gradient {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
</style>
</head>
<body>
<h1>Sorting Algorithm Performance</h1>
<form method="POST">
    <label for="sizes">Enter list sizes (comma-separated):</label>
    <input type="text" id="sizes" name="sizes" value="100,200,300,400,500">
    <button type="submit">Generate Plot</button>
</form>
{% if plot_url %}
<h2>Performance Plot:</h2>
<img src="data:image/png;base64,{{ plot_url }}" alt="Performance Plot">
{% endif %}
</body>
</html>
    '''  
    return render_template_string(html, plot_url=plot_url)
if __name__ == "__main__":
    app.run(debug=True)
