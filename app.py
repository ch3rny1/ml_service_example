from flask import Flask

app = Flask(__name__)

@app.route('/')
def ping():
    print('11111')
    return 'ok', 200

if __name__ == '__main__':
    app.run()