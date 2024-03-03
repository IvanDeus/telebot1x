#python3 script to start bot process
import subprocess
import sys
# Config import
from telebot_hook1x_cfg import *
# Help message
if len(sys.argv) == 1:
    print("Usage: {} [start|stop|status]".format(sys.argv[0]))
    sys.exit(1)
# status
def filter_processes_by_port(bot_lport):
    # Run the ps aux command to get a list of all processes
    ps_output = subprocess.check_output(["ps", "aux"])
    # Split the output into lines
    ps_lines = ps_output.decode().split('\n')
    # Filter the lines based on the local port
    filtered_lines = [line for line in ps_lines if ":{} ".format(bot_lport) in line]    
    return filtered_lines

# Start, stop, or check status of Gunicorn
action = sys.argv[1]
if action == "start":
    filtered_processes = filter_processes_by_port(bot_lport)
    if filtered_processes:
        print ("Bot is already running.")
    else:
        subprocess.Popen(
        ["gunicorn", "-b", "localhost:{}".format(bot_lport), "-w", "2", "-t", "222", "--log-file={}".format(logfpath), "telebot1x:app"]
        )
        print("Bot started.")
elif action == "stop":
    # Get the PID of the Gunicorn process and kill it
    try:
        gunicorn_pid = subprocess.check_output(["pgrep", "-f", "gunicorn"]).splitlines()[0]
        subprocess.call(["kill", gunicorn_pid.decode()])
        print("Bot stopped.")
    except subprocess.CalledProcessError:
        print("Bot is not running.")
elif action == "status":
    # Show the status of Gunicorn processes
    try:
        filtered_processes = filter_processes_by_port(bot_lport)
        if filtered_processes:
            print('\n'.join(filtered_processes))
        else:
            print ("Bot is not running.")
    except subprocess.CalledProcessError:
        print("Error while checking Gunicorn status.")
else:
    print("Usage: {} [start|stop|status]".format(sys.argv[0]))
    sys.exit(1)
