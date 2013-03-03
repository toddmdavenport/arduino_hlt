from flask import Flask, render_template, request
import subprocess

ctrl_script_path = "/home/tdavenport/working/arduino_hlt/hlt_ctrl.py"

app = Flask(__name__)

def data_parser(data):
    '''returns 3 variables for web front end'''
    system_state = True
    if data[0:3] == "OFF":
        system_state = False 
    data = data.strip()
    sensor_temp = data[data.find(":")+1 : data.find("\r\nset")]
    set_temp = data[data.rfind(":") + 1:]
    return [sensor_temp, set_temp, system_state]

@app.route('/')
def main():
    output = subprocess.check_output([ctrl_script_path, "-w"])
    output = data_parser(output)
    templateData = {
            "sensor_temp" : output[0],
            "set_temp"    : output[1], 
            "system_state": output[2]
            } 
    return render_template('main.html', **templateData)

@app.route('/system_ctrl/<action>', methods=['GET', 'POST'])
def action(action):
    if action == "on":
        subprocess.call([ctrl_script_path, "-n"])
        message ="The system is now ON"
    if action == "off":
        subprocess.call([ctrl_script_path, "-f"])
        message = "The system is now OFF"
    if action == "set":
        set_temp = request.form['set_temp'] 
        subprocess.check_output([ctrl_script_path, "-t"+str(set_temp)] )
        message = "The target temp is now set to %s" %(set_temp)

    templateData = {"message": message}
    return render_template('system_ctrl.html', **templateData)

if __name__ == '__main__':
    app.run(debug=True)
