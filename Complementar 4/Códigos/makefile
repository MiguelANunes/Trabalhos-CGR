CC = gcc
COMPILEFLAGS = -Wall -c
LINKFLAGS = -lglut -lGL -lGLU -lm
.PHONY: clean

boids: ${LINKFLAGS}

run: boids
	./boids

clean:
	rm *.o boids
