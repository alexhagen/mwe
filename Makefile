all: docs

docs: FORCE
	pandoc README.md -o docs/source/README.rst; \
	jupyter nbconvert test.ipynb --to rst --execute; \
	mv test.rst docs/source/test.rst; \
	cd docs/; \
	sphinx-apidoc -e -f -M -o ./ ../; \
	git add *.rst; \
	git commit -am "$(shell git log -1 --pretty=%B | tr -d '\n')"; \
	mkdir -p ~/pages/mwe/; \
	cd ~/pages/mwe/; \
	git rm -r *; \
	mkdir -p ~/pages/mwe/; \
	cd ~/code/mwe/docs/; \
	make html; \
	cp -r build/html/* ~/pages/mwe/; \
	cd ~/pages/mwe/; \
	touch .nojekyll; \
	git add * .nojekyll; \
	git commit -am "$(shell git log -1 --pretty=%B | tr -d '\n')"; \
	git push origin gh-pages; \
	cd ~/code/mwe

FORCE:
