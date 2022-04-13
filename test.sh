SHARE=$(pwd)
IMAGE=$1
NAME=$(sudo docker run -d -v ${SHARE}:/host/Users -it ${IMAGE} /bin/bash)
echo '****************'
sudo docker exec -i $NAME ./ask /host/Users/data/set1/hello.txt 3
echo '****************'
sudo docker exec -i $NAME ./answer /host/Users/data/set1/hello.txt /host/Users/data/set1/hello.txt
echo '****************'
sudo docker stop $NAME 
