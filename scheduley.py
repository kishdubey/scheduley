from flask import Flask, render_template, request, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/return_calendar_schedule", methods=['POST'])
def return_calendar_schedule():
    file = request.form['scheduleFile']
    term = request.form['term']
    year = request.form['year']

    print(year)
    return year

if __name__ == "__main__":
    app.run(debug=True)
