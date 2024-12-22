from flask import Flask, render_template, request
app = Flask(__name__,)
@app.route('/', methods=['GET', 'POST'])
def index():
    rating1 = 0
    rating2 = 0
    if request.method == 'POST':
        chef1 = list(map(int, request.form.get('chef1').split()))
        chef2 = list(map(int, request.form.get('chef2').split()))
        if len(chef1) == len(chef2):
            for i in range(len(chef1)):
                if chef1[i] > chef2[i]:
                    rating1 += 1
                elif chef1[i] < chef2[i]:
                    rating2 += 1
    rating_list = [rating1, rating2]
    return render_template('result.html', rating1=rating1, rating2=rating2, rating_list=rating_list) if request.method == 'POST' else render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
