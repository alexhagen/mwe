all: docs publish

docs: FORCE
	pandoc README.md -o docs/source/README.rst; \
	jupyter nbconvert test.ipynb --to html --template basic --execute; \
	mv test.html docs/source/test.html; \
	cd docs/; \
	sphinx-apidoc -e -f -M -o ./ ../; \
	make html

publish: FORCE
	mkdir -p ~/pages/mwe/; \
	cd ~/pages/mwe/; \
	git rm -r *; \
	mkdir -p ~/pages/mwe/; \
	cp -r ~/code/mwe/docs/build/html/* ~/pages/mwe/; \
	cd ~/pages/mwe/; \
	touch .nojekyll; \
	git add *; \
	git add .nojekyll; \
	git commit -am "$(shell git log -1 --pretty=%B | tr -d '\n')"; \
	git push origin gh-pages; \
	cd ~/code/mwe

FORCE:
