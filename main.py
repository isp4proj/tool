import requests
import json
import os
from subprocess import call
import subprocess
from colorama import Fore, Style
from requests import get

def cis_bechmark_check():
    print(f"{Fore.BLUE}# --------------------------------------------------------------------------------------------{Style.RESET_ALL}")
    print(f"{Fore.BLUE}# Docker CIS bechmarks check{Style.RESET_ALL}")
    print(f"{Fore.BLUE}# Checks for dozens of common best-practices around deploying Docker containers in production.{Style.RESET_ALL}")
    print(f"{Fore.BLUE}# Based on the CIS Docker Benchmark 1.3.1{Style.RESET_ALL}")
    print(f"{Fore.BLUE}# --------------------------------------------------------------------------------------------{Style.RESET_ALL}")

    call("./main.sh", shell=True)

def finish():
    print(f"{Fore.BLUE}\n# --------------------------------------------------------------------------------------------{Style.RESET_ALL}")
    print(f"{Fore.BLUE}# Finishing Scan{Style.RESET_ALL}")
    print(f"{Fore.BLUE}# Checks for system information.{Style.RESET_ALL}")
    print(f"{Fore.BLUE}# --------------------------------------------------------------------------------------------{Style.RESET_ALL}")
    
    logdata = {}

    info = subprocess.run(['lsb_release', '-a'], capture_output=True, text=True).stdout
    
    ip = get('https://api.ipify.org').content.decode('utf8')
    print(f"{Fore.YELLOW}[DEBUG] Public IP address is: {ip}{Style.RESET_ALL}")

    with open("results/output.log.json","r") as logfile:
        logdata = json.load(logfile)

    d = {
        "info": str(info),
        "ip": str(ip),
    }

    logdata["info"] = d

    with open("results/output.log.json","w") as logfile:
        print(f"{Fore.YELLOW}[DEBUG] Writing result to the log file{Style.RESET_ALL}")
        json.dump(logdata, logfile, ensure_ascii=False, indent=4)

    with open("results/output.log.json", "r") as logfile:
        data = json.loads(logfile.read())
        # print(data)
        
        url = 'https://54.238.175.157:5000/results'
        print(f"{Fore.YELLOW}[DEBUG] Sending results to the server {url}{Style.RESET_ALL}")

        r = requests.post(url, json=data,verify=False)

        if(r.status_code == 200):
            print(f"{Fore.YELLOW}[DEBUG] Successfully sent{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[DEBUG] Something went wrong, please try again{Style.RESET_ALL}")

def main():
    print(f"{Fore.BLUE}\n# Docker Security Framework v1.0 \n{Style.RESET_ALL}")

    #set permissions on results folder
    subprocess.call(['chmod', '+rw', 'results/'])
    subprocess.call(['chmod', '+x', 'main.sh'])
    # subprocess.call(['chmod', '+rwx', 'functions/'])

    print(f"{Fore.YELLOW}[DEBUG] Cleaning previous scans \n{Style.RESET_ALL}")

    if os.path.exists("./results/output.log.json"):
        os.remove("results/output.log.json")
    if os.path.exists("results/output.log"):
        os.remove("results/output.log")

    cis_bechmark_check()
    finish()

if __name__ == '__main__':
    main()

