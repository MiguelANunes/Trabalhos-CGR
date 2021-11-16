CC = gcc
COMPILEFLAGS = -Wall -lglut -lGL -lGLU -lm -c
LINKFLAGS = -lglut -lGL -lGLU -lm

all: link_all # atualizar depois

boneco: boneco_link

castelo: castelo_link

run_all: run_boneco

run_boneco: 
	./boneco_neve $(ARGS)

run_castelo:
	./castelo $(ARGS)
# $(ARGS) serve para capturar argumentos da linha de comando ao compilar pelo makefile

link_all: boneco_compile castelo_compile
	${CC} -o boneco_neve boneco_neve.o castelo construcao.o ${LINKFLAGS}

boneco_link: boneco_compile
	${CC} -o boneco_neve boneco_neve.o ${LINKFLAGS}

boneco_compile: 
	${CC} ${COMPILEFLAGS} boneco_neve.c

castelo_link: castelo_compile
	${CC} -o castelo construcao.o ${LINKFLAGS}

castelo_compile:
	${CC} ${COMPILEFLAGS} construcao.c

clean:
	rm *.o main boneco_neve *.out