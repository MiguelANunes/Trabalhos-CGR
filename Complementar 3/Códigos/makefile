CC = gcc
COMPILEFLAGS = -Wall -c
LINKFLAGS = -lglut -lGL -lGLU -lm
.PHONY: clean

neve: ${LINKFLAGS}

run: neve
	./neve

clean:
	rm *.o neve
