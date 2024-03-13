nextjs:
	cd ui && yarn build && yarn start
zeromq:
	cd compute/zeromq && source venv/bin/activate && python proxy.py
server:
	./run_server.sh
client:
	sudo ./run_client.sh
setup_server:
	./setup_server.sh
setup_client:
	./setup_client.sh