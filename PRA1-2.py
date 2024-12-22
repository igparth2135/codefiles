from flask import Flask, render_template, request
app = Flask(__name__)
def find_closest_pair(arr):
    arr.sort()
    left = 0
    right = len(arr) - 1
    closest_pair = (arr[left], arr[right])
    min_sum = float('inf')
    while left < right:
        current_sum = arr[left] + arr[right]
        if abs(current_sum) < abs(min_sum):
            min_sum = current_sum
            closest_pair = (arr[left], arr[right])
        if current_sum > 0:
            right -= 1
        elif current_sum < 0:
            left += 1
        else:
            return closest_pair
    return closest_pair
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            raw_data = request.form.get('numbers', '')
            numbers = list(map(int, raw_data.split(',')))
            pair = find_closest_pair(numbers)
            return render_template('result.html', pair=pair)
        except ValueError:
            return render_template('index.html', error="Invalid input. Please enter numbers separated by commas.")
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
