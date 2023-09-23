
build:
	sudo docker build -t ftapp .


quick_run:
	sudo docker build -t ftapp .
	sudo docker run ftapp
run:
	sudo docker run ftapp

stop:
	sudo docker stop $$(docker ps -a -q --filter "ancestor=ftapp)


clean:
	sudo docker rmi ftapp


