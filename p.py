import requests, re, time

with open("listemail", "r") as f:
	data = f.readlines()
	
email = data[0].split("@")[0].strip()
password = data[0].split("@")[1].strip()

a = 1
while True:
	check = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email}&domain={password}").json()
	if a == 1:
		print("Waiting.      ", end='\r')
	else:
		print("Waiting" + ("." * a), end='\r')
	a += 1
	if a == 6:
		a = 1
	
	if len(check) != 0:
		a = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={email}&domain={password}&id={check[0]['id']}")
		a = a.text.split(',')[16].split('confirmation_token=')[1].split('&amp;locale=id')[0]
		requests.get(f"https://run.qwiklabs.com/users/confirmation?confirmation_token={a}")
		print(f"{email}@{password} is confirm!!")
		break
	time.sleep(5)
	
with open('listemail', 'r') as fin:
    data = fin.read().splitlines(True)
with open('listemail', 'w') as fout:
    fout.writelines(data[1:])
