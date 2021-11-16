CC = gcc
FLAGS = -Wall -lglut -lGL -lGLU -lm

all: link # atualizar depois

run: 
	./main
# $(ARGS) 
# $(ARGS) serve para capturar argumentos da linha de comando ao compilar pelo makefile

link: compile
	${CC} -o main boneco_neve.o -lglut -lGL -lGLU -lm

compile: 
	${CC} ${FLAGS} -c boneco_neve.c

clean:
	rm *.o main