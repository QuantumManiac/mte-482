default:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

pushbutton:
	sudo GPIOZERO_PIN_FACTORY=rpigpio python3 pushbutton_test.py
