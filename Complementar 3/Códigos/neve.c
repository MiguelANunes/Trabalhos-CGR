// gcc fireworks_glut.c -lglut -lGL -lGLU -lm -o fireworks_glut
#include <GL/glut.h>  // Header File For The GLUT Library 
#include <GL/gl.h>	  // Header File For The OpenGL32 Library
#include <GL/glu.h>	  // Header File For The GLu32 Library
#include <math.h>
#include <unistd.h>
#include <stdio.h>

#define ESCAPE 27
#define NUM_PARTICLES 10000
#define GRAVITY 0.0003

struct s_pf {// colocar um campo de cor
    float x, y, veloc_x, veloc_y;
    unsigned lifetime;
} particles[NUM_PARTICLES];

int window; 
long curretParticles = NUM_PARTICLES;

// Inicializando todos os pixels
void InitAllParticles(int pause){
    int i;
    curretParticles = NUM_PARTICLES;

    if(pause) usleep(20000 + rand() % 200000);

    for(i=0;i<NUM_PARTICLES;i++) {
        if(particles[i].lifetime > 0)
            continue;
        float velocity = 0.0001;
        int angle = rand() % 360;
        particles[i].veloc_x = cos((M_PI * angle/180.0)) * velocity;
        particles[i].veloc_y = fabs(sin((M_PI * angle/180.0)) * velocity);
        particles[i].x = 0;
        particles[i].y = 2.25;
        particles[i].lifetime = 50;
    }
}

// Inicializando apenas um pixel
void InitParticle(int index){
    float velocity = 0.0001;
    int angle = rand() % 360;
    particles[index].veloc_x = cos((M_PI * angle/180.0)) * velocity;
    particles[index].veloc_y = fabs(sin((M_PI * angle/180.0)) * velocity);
    particles[index].x = 0;
    particles[index].y = 2.25;
    particles[index].lifetime = 50;
    curretParticles++;
}

// Desenhando a cena
void DrawGLScene(){

    int i, active_particles=0, RandDirecao, RandMovimentoX, DeslocamentoX, r;
    double Delta;
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);		// Clear The Screen And The Depth Buffer
    glLoadIdentity();				// Reset The View
    glTranslatef(0.0f,0.0f,-6.0f); // Cria as particulas 3 unidades acima da origem, 6 atrás dela

    glColor3f(1,1,1);

    glBegin(GL_POINTS);
    for(i=0;i<curretParticles;i++){
        r = rand() % 5;
        r = r%2 == 0 ? r : -r;
        particles[i].y += r * (0.075);
        r = rand() % 15;
        r = r%2 == 0 ? r : -r;
        particles[i].x += r * (0.1);
        particles[i].veloc_x += r * (0.1);
    }

    for(i=0;i<curretParticles;i++){
        Delta = (rand() % 10) * (55-particles[i].lifetime); // Faz com que as particulas se dispercem mais com o decorrer da simulação
        RandMovimentoX = rand() % 4 == 0 ? 1 : 0; // se rolou 0, RandMovimentoX recebe 1, 0 otherwise
        RandDirecao = rand() % 2 == 0 ? 1 : -1; // se rolou 0, RandDirecao recebe 1, -1 otherwise

        if(particles[i].lifetime > 0){
            active_particles++;
            
            particles[i].x += RandMovimentoX * RandDirecao * (Delta/100.0);
            particles[i].y -= (particles[i].veloc_y + GRAVITY + (Delta/100.0));
            particles[i].lifetime--;

            glVertex3f(particles[i].x, particles[i].y, 0.0f);
            usleep(0.5);

            if(particles[i].y < -2.25){ // se passou da parte de baixo da tela
                particles[i].lifetime = 0;
                active_particles--;
                curretParticles--;
                InitParticle(i); // cria uma nova partícula
            }
        }else{ // se ele morreu antes de chegar em y = -2.25
            InitParticle(i);
        }
    }
    glEnd();

    glutSwapBuffers();

    if(!active_particles) InitAllParticles(0); // reset particles
}

/* A general OpenGL initialization function.  Sets all of the initial parameters. */
void InitGL(int Width, int Height){
    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);// This Will Clear The Background Color To Black
    glClearDepth(1.0);				     // Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS);				 // The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST);			 // Enables Depth Testing
    glShadeModel(GL_SMOOTH);			 // Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();				// Reset The Projection Matrix

    gluPerspective(45.0f,(GLfloat)Width/(GLfloat)Height,0.1f,100.0f);	// Calculate The Aspect Ratio Of The Window

    glMatrixMode(GL_MODELVIEW);

    InitAllParticles(0); // Primeiro floco de neve
}

/* The function called when our window is resized (which shouldn't happen, because we're fullscreen) */
void ReSizeGLScene(int Width, int Height){
    if (Height==0)				// Prevent A Divide By Zero If The Window Is Too Small
        Height=1;

    glViewport(0, 0, Width, Height);		// Reset The Current Viewport And Perspective Transformation

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluPerspective(45.0f,(GLfloat)Width/(GLfloat)Height,0.1f,100.0f);
    glMatrixMode(GL_MODELVIEW);
}

/* The function called whenever a key is pressed. */
void keyPressed(unsigned char key, int x, int y){
    usleep(100);
    if (key == ESCAPE){ 
        glutDestroyWindow(window); 

        exit(0);                   
    }
}

int main(int argc, char **argv){  
    glutInit(&argc, argv);  
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH);  
    glutInitWindowSize(800, 700);  
    glutInitWindowPosition(0, 0);  
    window = glutCreateWindow("Neve");  
    glutDisplayFunc(&DrawGLScene);  
    // glutFullScreen();
    glutIdleFunc(&DrawGLScene);
    glutReshapeFunc(&ReSizeGLScene);
    glutKeyboardFunc(&keyPressed);
    InitGL(800, 700); 
    glutMainLoop();  
  return 0;
}