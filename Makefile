# 'make' by itself runs the 'all' target
.DEFAULT_GOAL := all

.PHONY: all
all:	fmt lint flake

.PHONY: fmt
fmt:
	@echo "###"
	@echo "----------------"
	@echo "Starting  format"
	black finviz_run.py --line-length 79
	@echo "Completed format"
	@echo "###"
	@echo ""

.PHONY: lint
lint:
	@echo "###"
	@echo "----------------"
	@echo "Starting  lint with pylint"
	pylint finviz_run.py --disable=W0106
	@echo "Completed with pylint"
	@echo "###"
	@echo ""

.PHONY: flake
flake:
	@echo "###"
	@echo "----------------"
	@echo "Starting  lint with flake8"
	flake8 finviz_run.py
	@echo "Completed with flake8"
	@echo "###"
	@echo ""

# .PHONY: test
# test:
# 	@echo "Starting  unit tests"
# 	find . -name "*.pyc" -delete
# 	pytest .
# 	@echo "Completed unit tests"
