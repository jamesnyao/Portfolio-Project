all: portfolio

run: portfolio
	./portfolio

portfolio:
	g++ Driver.cpp Request.cpp -o portfolio

clean:
	rm -vf portfolio *.o
	