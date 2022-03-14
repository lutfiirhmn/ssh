import os
import shlex
import time
from subprocess import PIPE, Popen

def run_command(command, callback=None):
  with Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, universal_newlines=True) as process:
    while True:
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
        break
      if output:
        print(output.strip())
    rc = process.poll()
    if rc is None:
      process.kill()
    if callback:
      error_output = process.stderr.readlines()
      callback(error_output)

    process.stdout.close()
    process.stderr.close()
    process.terminate()
  return rc

def run_with_pipe(command):
  commands = list(map(shlex.split, command.split("|")))
  ps = Popen(commands[0], stdout=PIPE, stderr=PIPE)
  for command in commands[1:]:
    ps_new = Popen(command, stdin=ps.stdout,
                   stdout=PIPE, stderr=PIPE)
    ps.stdout.close()
    ps.stderr.close()
    ps.wait()
    ps = ps_new

  result = ps.stdout.readlines()
  ps.stdout.close()
  ps.stderr.close()
  ps.wait()
  return result

def get_tunnel_config():
  output = requests.get("http://localhost:4040/api/tunnels").json()
  public_url = output["tunnels"][0]["public_url"]
  groups = re.match(r'(.*?)://(.*?):(\d+)', public_url)
  protocol = groups.group(1)
  domain = groups.group(2)
  port = groups.group(3)
  return {
    "domain":domain,
    "protocol":protocol,
    "port":port
  }

def expose_env_variable(
	env_variable_name, 
	file_path="/etc/environment"):
	if env_variable_name in os.environ:
		os.system(f'echo "export {env_variable_name}=${env_variable_name}" >> {file_path}')

def launch_ssh(token,
               password="",
               publish=True,
               verbose=False,
               region="us",
               remote_addr=None):

  # Ensure the ngrok auth token is not empty
  if(not token):
    raise Exception(
        "Ngrok AuthToken is missing, copy it from https://dashboard.ngrok.com/auth")

  if(not region):
    raise Exception(
        "Region is required. If you do want prefer the default value, don't set the 'region' parameter")

  # Kill any ngrok process if running
  os.system(
      "kill $(ps aux | grep '\\.\\/ngrok tcp' | awk '{print $2}')")

  # Download ngrok
  run_command(
      "wget -q -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip")
  run_command("unzip -qq -n ngrok-stable-linux-amd64.zip")

  # Install the openssh server
  os.system(
      "apt-get -qq update && apt-get -qq install -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null")

  # Set the password
  run_with_pipe("echo root:{} | chpasswd".format(password))

  # Configure the openSSH server
  run_command("mkdir -p /var/run/sshd")
  os.system("echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config")
  if password:
    os.system(
        'echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')

  expose_env_variable("LD_LIBRARY_PATH")
  expose_env_variable("COLAB_TPU_ADDR")
  expose_env_variable("COLAB_GPU")
  expose_env_variable("TBE_CREDS_ADDR")
  expose_env_variable("TF_FORCE_GPU_ALLOW_GROWTH")
  expose_env_variable("TPU_NAME")
  expose_env_variable("XRT_TPU_CONFIG")

  os.system('/usr/sbin/sshd -D &')

  extra_params = []
  if(remote_addr):
    extra_params.append("--remote-addr {}".format(remote_addr))

  # Create tunnel
  proc = Popen(shlex.split(
      './ngrok tcp --authtoken {} --region {} {} 22'.format(
          token, region, " ".join(extra_params))
  ), stdout=PIPE)

  # Get public address
  try:
    info = get_tunnel_config()
  except:
    raise Exception(
        "It looks like something went wrong, please make sure your token is valid")

  if verbose:
    print("DEBUG:", info)

  if info:
    # Extract the host and port
    host = info["domain"]
    port = info["port"]
    print("Successfully running", "{}:{}".format(host, port))
    print("[Optional] You can also connect with VSCode SSH Remote extension using this configuration:")
    print(f'''
  Host google_colab_ssh
    HostName {host}
    User root
    Port {port}
    ''')
  else:
    print(proc.stdout.readlines())
    raise Exception(
        "It looks like something went wrong, please make sure your token is valid")
  proc.stdout.close()
