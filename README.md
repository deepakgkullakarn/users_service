1.	Navigate to command prompt and run the minikube using below command

minikube start

2.	Create a deployment to pull the image from docker hub

kubectl create deployment my-cool-service --image=deepakgkcang/my-cool-service:latest


3.	Expose the above deployment as a service on port 8000 using below command

kubectl expose deployment my-cool-service --type=NodePort --port=8000 --target-port=8000

4.	Execute below command to check the service URL 
minikube service my-cool-service --url
If you see message like for example -http://127.0.0.1:60811
Take the IP address and add to etc/host file like mentioned below
127.0.0.1 my-cool-service

5.	Port redirection setting
For windows open powershell and use below command to make entry to redirect Port to 8000 (Make sure to update the entry of connectport in below command to the above received port)
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=<MINIKUBE_SERVICE_IP> connectport=<MINIKUBE_SERVICE_PORT> connectaddress=<MINIKUBE_SERVICE_IP>


For Linux and equivalent use below command
sudo iptables -t nat -A PREROUTING -p tcp --dport 8000 -j REDIRECT --to-port <MINIKUBE_SERVICE_PORT>
sudo iptables -t nat -A OUTPUT -p tcp -d <MINIKUBE_SERVICE_IP> --dport 8000 -j REDIRECT --to-port <MINIKUBE_SERVICE_PORT>
