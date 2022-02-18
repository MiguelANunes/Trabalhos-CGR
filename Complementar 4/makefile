CC = gcc
COMPILEFLAGS = -Wall -c
LINKFLAGS = -lglut -lGL -lGLU -lm
.PHONY: clean

robo: ${LINKFLAGS}

run: robo
	./robo

clean:
	rm *.o robo
