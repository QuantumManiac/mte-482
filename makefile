nextjs:
	cd ui && yarn build && yarn start
zeromq:
	cd compute/zeromq && source venv/bin/activate && python proxy.py
