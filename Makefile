.PHONY: publish
.SILENT:

publish:
	rm -rf build dist *egg-info
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*