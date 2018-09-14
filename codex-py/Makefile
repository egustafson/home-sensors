.PHONY: all clean package test

all: clean test

clean:
	rm -rf `find . -type d -name __pycache__`
	rm -f `find . -name '*.pyc'`
	rm -f `find . -name '*.pyo'`

test:
	python -m unittest discover -v

package:
	python setup.py sdist

docker:
	docker build -t codex .

release:
	@echo "UNIMPLEMENTED - release"
	@echo "--> 'python setup.py sdist register upload'"

local-install:
	@echo "-- prefer virtualenv over user installation --"
	@echo ""
	python setup.py develop --user

install:
## only run install if inside a virtual environment (python virtual_env)
	@if [ "${VIRTUAL_ENV}x" != "x" ]; then \
		python setup.py install; \
	else \
		echo "VIRTUAL_ENV is not set.  run: 'python setup.py install'"; \
	fi

