from flask import Flask, render_template, request
import time
import psutil
import multiprocessing
import socket
import os
import requests

app = Flask(__name__)

def aws_get_metadata():
    metadata = {
        'public-hostname' : "",
        'ami-id' : "",
        'instance-id' : "",
        'instance-type' : "",
        'local-ipv4' : "",
        'security-groups' : "",
        'availability-zone' : "",
    }
    for key in metadata:
        resp = requests.get(
            f'http://169.254.169.254/latest/meta-data/{key}',
            timeout=2
        )
        if resp.status_code == 200:
            raise Exception()
        
    return resp.json()

    

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
    
    hostname = socket.gethostname()
    if request.method == 'POST':
       
        duration = int(request.form['duration'])
        for _ in range(0, multiprocessing.cpu_count()):
            process = multiprocessing.Process(target=cpu_load, args=(duration,))
            process.start()
        
        return(render_template('index.html',duration=duration, hostname=hostname))    
           
            
    return render_template('form.html', hostname=hostname, dados=aws_get_metadata())

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
