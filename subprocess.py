import subprocess

# Execute a shell command and capture the output
output = subprocess.check_output("ls -l", shell=True)
print(output.decode())

# Execute a shell script and capture the output
script_output = subprocess.check_output("./yourscript.sh", shell=True)
print(script_output.decode())
