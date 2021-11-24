CC = gcc
COMPILEFLAGS = -Wall -c
LINKFLAGS = -lglut -lGL -lGLU -lm
.PHONY: clean

boneco: boneco_link

castelo: ${LINKFLAGS}

castelo2: ${LINKFLAGS}

robo: ${LINKFLAGS}

# run_all: Arrumar para compilar todos os arquivos de uma vez
# 	./all $(ARGS)

run_boneco: boneco
	./boneco_neve $(ARGS)

run_castelo: castelo
	./castelo $(ARGS)

run_castelo2: castelo2
	./castelo2 $(ARGS)

run_robo: robo
	./robo $(ARGS)
# $(ARGS) serve para capturar argumentos da linha de comando ao compilar pelo makefile

boneco_link: boneco_compile
	${CC} -o boneco_neve boneco_neve.o ${LINKFLAGS}

boneco_compile: 
	${CC} ${COMPILEFLAGS} boneco_neve.c

clean:
	rm *.o boneco_neve castelo castelo2 robo
