.PHONY: all
all:
	for dir in about play; do mkdir -p $$dir && cp index.html $$dir/index.html; done
