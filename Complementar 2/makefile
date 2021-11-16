CC = gcc
COMPILEFLAGS = -Wall -lglut -lGL -lGLU -lm
LINKFLAGS = -lglut -lGL -lGLU -lm

all: link # atualizar depois

run: run_boneco

run_boneco: 
	./boneco_neve $(ARGS)
# $(ARGS) serve para capturar argumentos da linha de comando ao compilar pelo makefile

link: boneco_compile
	${CC} -o boneco_neve boneco_neve.o ${LINKFLAGS}

boneco_compile: 
	${CC} ${COMPILEFLAGS} -c boneco_neve.c

clean:
	rm *.o main boneco_neve *.out