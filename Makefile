# Default
all:
	make clean && make run

# Run
run:
	python3 arrange.py
	cp ./meta-file.json ./data
	mkdir results
	python3 koppel11.py -i=./data/ -o=./results

# Remove object files and the executable
clean:
	rm -f .DS_Store
	rm -f jsonhandler.pyc
	rm -fr __pycache__
	rm -fr data
	rm -fr results

# Show the results
show:
	cat ./results/answers.json

# Don't display instructions while running
.SILENT:
	run
