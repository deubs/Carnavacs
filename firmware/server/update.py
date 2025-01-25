#!/usr/bin/env python3

import paramiko
import pyodbc
import configparser
import subprocess
import time

# Leer el archivo de configuración
config = configparser.ConfigParser()
config.read('config.ini')

# Obtener datos de configuración
db_server = config['database']['server']
db_database = config['database']['database']
db_username = config['database']['username']
db_password = config['database']['password']
public_key = config['git']['public_key']
git_repo_url = config['general']['git_repo_url']

# Conexión a la base de datos SQL Server
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_server};DATABASE={db_database};UID={db_username};PWD={db_password}')
cursor = conn.cursor()

def get_devices():
    cursor.execute("SELECT ip, hostname FROM devices")
    rows = cursor.fetchall()
    devices = {}
    for row in rows:
        devices[row.ip] = row.hostname
    return devices

def configure_hostname_and_git(ip, hostname, git_repo_url, public_key):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='pi', password='your_password')
    
    # Comprobar si el hostname ya ha sido configurado
    stdin, stdout, stderr = ssh.exec_command("cat /etc/hostname")
    current_hostname = stdout.read().decode().strip()
    if current_hostname != hostname:
        commands = [
            f"echo {hostname} | sudo tee /etc/hostname",
            f"sudo sed -i 's/127.0.1.1.*/127.0.1.1 {hostname}/' /etc/hosts"
        ]
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
    
    # Comprobar si el repositorio Git ya ha sido clonado
    stdin, stdout, stderr = ssh.exec_command(f"ls /path/to/your/project")
    project_exists = stdout.read().decode().strip()
    if not project_exists:
        commands = [
            "mkdir -p ~/.ssh",
            f"echo '{public_key}' >> ~/.ssh/authorized_keys",  # Agrega tu clave pública al archivo authorized_keys
            f"git clone {git_repo_url} /path/to/your/project"
        ]
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            print(stdout.read().decode())
    else:
        ssh.exec_command(f"cd /path/to/your/project && git pull origin main")

    # Actualizar los paquetes de Debian y instalar dependencias de Python
    update_commands = [
        "sudo apt-get update",
        "sudo apt-get upgrade -y",
        "sudo apt-get install -y python3-pip",  # Instalar pip3 si no está instalado
        "pip3 install -r /path/to/your/project/requirements.txt"  # Instalar dependencias desde requirements.txt
    ]
    for command in update_commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
    
    ssh.exec_command("sudo reboot")
    ssh.close()

def update_local_repo():
    result = subprocess.run(["git", "fetch"], capture_output=True, text=True)
    if "Your branch is up to date" in result.stdout:
        return False
    else:
        subprocess.run(["git", "pull"], capture_output=True, text=True)
        return True

def deploy_update():
    devices = get_devices()
    for ip, hostname in devices.items():
        if ping_device(ip):
            configure_hostname_and_git(ip, hostname, git_repo_url, public_key)


def ping_device(ip):
    result = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
    return "1 packets transmitted, 1 received" in result.stdout


if _name_ == "_main_":
    devices = get_devices()
    for ip, hostname in devices.items():
        if ping_device(ip):
            print("device {ip} is online")	

if _name_ == "_moin_":
    while True:
        if update_local_repo():
            print("Actualización detectada, desplegando...")
            deploy_update()
        else:
            print("No hay actualizaciones disponibles.")
        time.sleep(3600)  # Verifica cada hora
