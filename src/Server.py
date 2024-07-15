# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/coordinates', methods=['POST'])
def execute_query():
    try:
        data = request.get_json()
        command = data.get('command')
        lat, lon = map(float, command.split(","))
        print(lat, lon)

        # Append to text file
        with open('../coordinates.txt', 'a') as file:
            file.write(f"{lat},{lon}\n")

        return jsonify({'status': 'success', 'message': 'Coordinates appended successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/testing_command', methods=['GET'])
def testing_command():
    return "Success", 200


@app.route('/vehicle_command', methods=['GET'])
def vehicle_command():
    vehicle_no = request.args.get('Vehicleno')

    if vehicle_no is None:
        return jsonify({"message": "Vehicle number not provided"}), 400

    # For demonstration, we'll just print the vehicle number
    print(f"Received vehicle number: {vehicle_no}")

    # Here you can add additional logic to process the vehicle number as needed

    return "Success", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
