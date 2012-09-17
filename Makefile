doc:
	pip install samsa[docs]
	cd doc/ && make html

lint:
	pip install --use-mirrors samsa[lint]
	pyflakes ./samsa
	pyflakes ./tests
	pep8 ./samsa ./tests

unit:
	python setup.py nosetests --attr=!integration

integration:
	python setup.py nosetests --attr=integration

clean:
	find . -name \*.pyc -delete

test: clean
	python setup.py nosetests

vendor:
	make -C vendor


.PHONY: doc unit integration test lint vendor clean
