from flask import Flask, request, jsonify
import subprocess
import time
import subprocess
import shlex
import os
import signal
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)

# Initialize a subprocess for a shell
shell_process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    if request.is_json:
        data = request.get_json()
        command = data.get('command')
        if command:
            try:
                # Execute Command
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                time.sleep(10)
                output, error = process.communicate()
		
                return jsonify({"output": output, "error": error})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No command provided"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/execute_terminal_command', methods=['POST'])
def execute_terminal_command():
    if request.is_json:
        data = request.get_json()
        command = data.get('command')
        if command:
            try:
                # Send command to the shell
                shell_process.stdin.write(command + "\n")
                shell_process.stdin.flush()
                time.sleep(100)
		
                # Read response (this might need refinement for long outputs)
                output = shell_process.stdout.readline()

                return jsonify({"output": output})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No command provided"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400
        
@app.route('/run-script')
def run_script():
    try:
        # Replace with the path to your script
        script_path = '/home/mkovelamudi/workspaces/isaac_ros-dev/src/Scripts/container_launch.sh'

        # Ensure your script is executable
        subprocess.run(['chmod', '+x', script_path])
        # Run the script
        result = subprocess.run([script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        

        # Return the script output
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        # Return error output if script execution fails
        return jsonify({"error": e.stderr}), 500
        
@app.route('/run-docker')
def run_docker():
    try:
        # Replace with the path to your script
        script_path = '/home/mkovelamudi/workspaces/isaac_ros-dev/src/Scripts/docker.sh'

        # Ensure your script is executable
        subprocess.run(['chmod', '+x', script_path])
        # Run the script
        result = subprocess.run([script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(50)

        # Return the script output
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        # Return error output if script execution fails
        return jsonify({"error": e.stderr}), 500
        
@app.route('/run-camera')
def run_camera():
    try:
        # Replace with the path to your script
        script_path = '/home/mkovelamudi/workspaces/isaac_ros-dev/src/Scripts/launchCamera.sh'

        # Ensure your script is executable
        subprocess.run(['chmod', '+x', script_path])
        # Run the script
        result = subprocess.run([script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Return the script output
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        # Return error output if script execution fails
        return jsonify({"error": e.stderr}), 500

@app.route('/stop-script', methods=['GET'])
def stop_script():
    pid_file = '/home/mkovelamudi/workspaces/isaac_ros-dev/processes.txt'
    try:
        with open(pid_file, 'r') as file:
            pid = int(file.read().strip())
        os.kill(pid, signal.SIGTERM)  # Send SIGTERM signal to the process
        return jsonify({"message": "Script stopped"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/copy-model', methods=['POST'])
def copy_model():
    pid_file = '/home/mkovelamudi/workspaces/isaac_ros-dev/processes.txt'
    
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    request_data = request.get_json()
    s3_url = request_data.get('url')
    if not s3_url:
        return jsonify({"error": "Missing URL parameter"}), 400

    bucket_name = 'masterprojectbucket'  # Replace with your bucket name
    s3_file_key = s3_url  # Extract the file key from the URL
    local_file_path = '/home/mkovelamudi/workspaces/isaac_ros-dev/' + s3_file_key.split("/")[-1]  # Define your local file path

    s3_client = boto3.client('s3', aws_access_key_id="AKIARWZZ67ATZUF5ROV6", aws_secret_access_key="SS56EIg0c7O5PD1U9SAcs/gXxp09oFE96KmMXpad")
    try:
        s3_client.download_file(bucket_name, s3_file_key, local_file_path)
        return jsonify({"message": f"File downloaded successfully to {local_file_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)