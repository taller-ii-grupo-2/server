sudo docker rm $(sudo docker ps -f status=exited -aq)
sudo docker rmi $(sudo docker images -f "dangling=true" -q)
sudo docker volume rm $(sudo docker volume ls -qf dangling=true)
