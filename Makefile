.PHONY: run install clean

install: venv
	. venv/bin/activate && pip install -r requirements.txt
