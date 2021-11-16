CC = gcc
COMPILEFLAGS = -Wall -c
LINKFLAGS = -lglut -lGL -lGLU -lm
.PHONY: clean
all: link_all # atualizar depois

boneco: boneco_link

castelo: ${LINKFLAGS}

# run_all: Arrumar para compilar todos os arquivos de uma vez
# 	./all $(ARGS)

run_boneco: boneco
	./boneco_neve $(ARGS)

run_castelo: castelo
	./castelo $(ARGS)
# $(ARGS) serve para capturar argumentos da linha de comando ao compilar pelo makefile

# link_all: boneco_compile castelo_compile
# 	${CC} -o all boneco_neve.o castelo.o ${LINKFLAGS}

boneco_link: boneco_compile
	${CC} -o boneco_neve boneco_neve.o ${LINKFLAGS}

boneco_compile: 
	${CC} ${COMPILEFLAGS} boneco_neve.c

# castelo_link: castelo_compile
# 	${CC} -o castelo castelo.o ${LINKFLAGS}

# castelo_compile:
# 	${CC} ${COMPILEFLAGS} castelo.c

clean:
	rm *.o boneco_neve castelo all