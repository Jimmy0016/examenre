build:
	docker build -t jimmy:3.0.0 .

deploy:
	docker stack deploy --with-registry-auth -c stack.yml rugal

rm:
	docker stack rm rugal
