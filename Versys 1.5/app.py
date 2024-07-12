from flask import Flask, render_template



app = Flask(__name__)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/contact')
def contacts():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)


