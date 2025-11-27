build:
	docker build -t espinozamg:1.0.1 .

deploy:
	docker stack deploy --with-registry-auth -c stack.yml rugal

rm:
	docker stack rm rugal
