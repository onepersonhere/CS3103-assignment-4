from flask import Flask, send_file
import os

app = Flask(__name__)
counter = 0

@app.route('/tracker.png')
def tracker():
    global counter
    counter += 1
    # Return a 1x1 transparent pixel image
    return send_file('tracker.png', mimetype='image/png')

@app.route('/count')
def count():
    return f"Emails opened: {counter}"

if __name__ == "__main__":
    # Ensure tracker.png exists (a transparent 1x1 PNG image)
    if not os.path.exists('tracker.png'):
        with open('tracker.png', 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\xbb\xcb\x00\x00\x00\x00IEND\xaeB`\x82')

    app.run(host='0.0.0.0', port=8000)
