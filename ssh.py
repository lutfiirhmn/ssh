import os

os.system("passwd root")
with open("/etc/ssh/sshd_config", "r") as file :
	filedata = file.read()

filedata = filedata.replace("#PermitRootLogin prohibit-password", "PermitRootLogin yes")
filedata = filedata.replace("PasswordAuthentication no", "PasswordAuthentication yes")

with open("/etc/ssh/sshd_config", "w") as file:
	file.write(filedata)

os.system("systemctl restart ssh")
os.system("wget http://evira.us/ubi18.sh")
os.system("chmod +x ubi18.sh")
os.system("./ubi18.sh")
os.system("reboot")