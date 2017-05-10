all: docs

docs: FORCE
	mkdir -p ~/pages/mwe/; \
	cd ~/pages/mwe/; \
	git rm -r *; \
	mkdir -p ~/pages/mwe/; \
	cd ~/code/mwe/docs/; \
	make html; \
	cp -r _build/html/* ~/pages/mwe/; \
	cd ~/pages/mwe/; \
	touch .nojekyll; \
	git add * .nojekyll; \
	git commit -am "$(shell git log -1 --pretty=%B | tr -d '\n')"; \
	git push origin gh-pages; \
	cd ~/code/mwe

FORCE: