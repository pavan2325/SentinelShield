from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Request received:")
    print("URL:", request.url)
    print("Headers:", dict(request.headers))
    print("Args:", request.args.to_dict())
    return "SentinelShield is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)