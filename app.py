from flask import Flask, render_template, request, jsonify, redirect, url_for
import linear as ln

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        username = data.get('username', '')
        otp = data.get('otp', '')
        hidden_name = bool(data.get('hidden_name', ''))
        mouse_movements = data.get('mouse_movements', [])
        device_type = data.get('device_type', 'unknown')
        gyroscope_data = data.get('gyroscope_data', [])
        touch_events = data.get('touch_events', [])

        x_data = [movement['x'] for movement in mouse_movements]
        y_data = [movement['y'] for movement in mouse_movements]

        print(f"Username: {username}, OTP: {otp}, Hidden Name: {hidden_name}")
        print(f"Device Type: {device_type}")
        print("Mouse Movement X Coordinates:", x_data)
        print("Mouse Movement Y Coordinates:", y_data)
        print("Touch Event Data:", touch_events)  # Fix: Ensure touch data is logged

        bot = 'Yes' if hidden_name else 'No'

        if device_type == "mobile":
            if len(touch_events) > 0:
                touch = 'Yes'
            else :
                touch= 'No'
            result = ln.predict_user_mobile(bot, touch)[0]
        else:
            if ((len(x_data) & len(y_data))== 0):
                l = 'non Linear'
            else:
                a = ln.s(x_data, y_data)
                l = ln.find(a)

            result = ln.predict_user(bot, l)[0]

        print("Prediction Result:", result)

        return jsonify({
            "redirect": url_for('result_page', username=username, result=result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/result')
def result_page():
    username = request.args.get("username", "")
    result = request.args.get("result", "")
    return render_template('result.html', username=username, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
