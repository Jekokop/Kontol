from flask import Flask, jsonify
import subprocess, sys

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "aktif", "usage": "/search/<username>"})

@app.route('/search/<username>')
def search(username):
    result = subprocess.run(
        [sys.executable, '-m', 'sherlock', username,
         '--print-found', '--no-color'],
        capture_output=True, text=True, timeout=60
    )
    found = [
        line.split('[+]')[-1].strip()
        for line in result.stdout.split('\n')
        if '[+]' in line
    ]
    return jsonify({
        "username": username,
        "total": len(found),
        "found": found
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
