it uses openvas and python to scan 

1:create a docker image and start the openvas container
docker volume create openvas

docker run -d -p 9392:9392 -p 9390:9390 -e GMP=9390 -e PASSWORD=”admin” --volume openvas:/data  --name openvas immauss/openvas:latest
2. install python-gvm

3. fire up the program
python vulscan.py
A. it scan localhost for the demo. It will need to change for the target scaned  system 

