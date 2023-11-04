from flask import Flask, render_template, url_for, request, redirect
import time
import psutil
import multiprocessing
import socket
import os
import requests

app = Flask(__name__)



def aws_get_metadata():
    URL_AZ = 'http://169.254.169.254/latest/meta-data/placement/availability-zone'
    URL_HOSTNAME = 'http://169.254.169.254/latest/meta-data/hostname'
    ID=os.getenv('HOSTNAME')
    resp_az = requests.get(URL_AZ)
    resp_hostname = requests.get(URL_HOSTNAME)
    meta_fields = {
        "AZ": resp_az.text.split('\n'),
        "hostname": resp_hostname.text.split('\n'),
        "id": ID
    }
    return meta_fields

def cpu_load(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        #render_template('index.html')
        pass


@app.route('/show_cpu')
def show_cpu():
    cpu = psutil.cpu_percent(4)
    return render_template('show_cpu.html', cpu=cpu)


@app.route('/', methods=['GET', 'POST'])
def form():
    
    info = aws_get_metadata()
    if request.method == 'POST':
       
        duration = int(request.form['duration'])
        for _ in range(0, multiprocessing.cpu_count()):
            process = multiprocessing.Process(target=cpu_load, args=(duration,))
            process.start()
        return(render_template('form.html',duration=duration, hostname=info["hostname"], AZ=info["AZ"], ID=info["id"]))    
    
    return render_template('form.html', hostname=info["hostname"], AZ=info["AZ"], ID=info["id"])

if __name__ == '__main__':
    
    app.run(debug=True, port=5000, host='0.0.0.0')
