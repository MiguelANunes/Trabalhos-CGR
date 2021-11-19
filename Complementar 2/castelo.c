#include<stdlib.h>
#include<stdio.h>
#include<GL/glut.h>

static GLfloat ROTACAO_Y = 0.0f;
static GLfloat ROTACAO_X = 0.0f;

float coordenadaX = 0.9f;
float coordenadaZ = 1.5f;

/*
    torres

    1---2
    |-3-|
    4-5-6
    ^^^^^ 
    frente
*/


void ChangeSize(int comprimento, int altura){  
    GLfloat fAspect;  
  
    // Prevent a divide by zero  
    if(altura == 0)  
        altura = 1;  
  
    // Set Viewport to window dimensions  
    glViewport(0, 0, comprimento, altura);  
  
    fAspect = (GLfloat)comprimento/(GLfloat)altura;  
  
    // Reset coordinate system  
    glMatrixMode(GL_PROJECTION);  
    glLoadIdentity();  
  
    // Produce the perspective projection  
    gluPerspective(35.0f, fAspect, 1.0, 40.0);  
  
    glMatrixMode(GL_MODELVIEW);
    // Applies subsequent matrix operations to the modelview matrix stack. 
    glLoadIdentity();  
}  

void SetupRC(){  

    // Light values and coordinates  
    GLfloat  whiteLight[] = { 0.05f, 0.05f, 0.05f, 1.0f };  
    GLfloat  sourceLight[] = { 0.25f, 0.25f, 0.25f, 1.0f };  
    GLfloat  lightPos[] = { -10.f, 5.0f, 5.0f, 1.0f };  
  
    glEnable(GL_DEPTH_TEST);    // Hidden surface removal  
    glFrontFace(GL_CCW);        // Counter clock-wise polygons face out  
    glEnable(GL_CULL_FACE);     // Do not calculate inside  
  
    // Enable lighting  
    glEnable(GL_LIGHTING);  
  
    // Setup and enable light 0  
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight);  
    glLightfv(GL_LIGHT0,GL_AMBIENT,sourceLight);  
    glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight);  
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos);  
    glEnable(GL_LIGHT0);  
  
    // Enable color tracking  
    glEnable(GL_COLOR_MATERIAL);  
      
    // Set Material properties to follow glColor values  
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);  
  
    // Black blue background  
    glClearColor(0.25f, 0.25f, 0.50f, 1.0f);  

}  

void SpecialKeys(int key, int x, int y){  
    // lida com o input de teclas do teclado
    if(key == GLUT_KEY_LEFT)  
        ROTACAO_Y -= 5.0f;  
  
    if(key == GLUT_KEY_RIGHT)  
        ROTACAO_Y += 5.0f;  
    
    if(key == GLUT_KEY_UP)
        ROTACAO_X += 5.0f;

    if(key == GLUT_KEY_DOWN)
        ROTACAO_X -= 5.0f;

    ROTACAO_Y = (GLfloat)((const int)ROTACAO_Y % 360);  
    ROTACAO_X = (GLfloat)((const int)ROTACAO_X % 360);  
  
    // Refresh the Window  
    glutPostRedisplay();  
}

void RenderScene(void){  

    GLUquadricObj *ObjetoPrincipal;  // Cria um objeto quádrico
      
    // Clear the window with current clearing color  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  
  
    // Save the matrix state and do the rotations  
    glPushMatrix(); // salva a matriz de modelos 

	// Move object back and do in place rotation  
	glTranslatef(0.0f, -1.0f, -5.0f); // faz uma translação na matriz de modelos
	glRotatef(ROTACAO_Y, 0.0f, 1.0f, 0.0f);  // faz uma rotação na matriz de modelos
    glRotatef(ROTACAO_X, 1.0f, 0.0f, 0.0f);
    // essas operações só se aplicam aos modelos existentes, I guess

	// Desenha o objeto
	ObjetoPrincipal = gluNewQuadric();  
	gluQuadricNormals(ObjetoPrincipal, GLU_SMOOTH);  
    glColor3f(1.0f, 1.0f, 1.0f);
    // desenharei da esquerda pra direita
    // assumindo que a torre de trás da parede, que está no fundo e tem um telhado não cônico, está na posição 0,0

    // chao
    
    glPushMatrix();
        glTranslatef(0.0f, 0.125f, -4.0f); 
        glRotatef(90, 0.0f, 0.0f, 1.0f);
        //glTranslatef(0.10f,0.22f,-0.75f); // -0.5 pois agora essa retângulo está de cabeiça p/ baixo
        gluCylinder(ObjetoPrincipal, 2.0f, 2.0f, 5.0f, 2, 1);
    glPopMatrix();
    

    // Torre esquerda, fundo 
    // torre 1
    glPushMatrix();
        glTranslatef(-1.0, 0.625f, -1.5);
        glRotatef(90,1,0,0);             // rotaciona
        glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
        gluCylinder(ObjetoPrincipal, 0.15f, 0.15f, 0.5f, 30, 15);
    glPopMatrix();

        // Telhado da torre
        glPushMatrix();
            glTranslatef(-1.0f, 0.625f, -1.5f);
            glRotatef(-90,1,0,0);             // rotaciona
            glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
            gluCylinder(ObjetoPrincipal, 0.18f, 0.0f, 0.35f, 30, 15);
        glPopMatrix();

    // Parede entre torre esquerda atras e torre esquerda frente
    // parede 1-4
    glPushMatrix();
        glTranslatef(-1.0f, 0.28f, -1.5f); 
        //glRotatef(-180, 1, 0, -0.30f);
        //glTranslatef(0.10f,0.22f,-0.75f); // -0.5 pois agora essa retângulo está de cabeiça p/ baixo
        gluCylinder(ObjetoPrincipal, 0.175f, 0.175f, 1.5f, 2, 1);
    glPopMatrix();

    // Torre esquerda, fundo 
    // torre 2
    glPushMatrix();
        glTranslatef(1.0, 0.625f, -1.5);
        glRotatef(90,1,0,0);             // rotaciona
        glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
        gluCylinder(ObjetoPrincipal, 0.15f, 0.15f, 0.5f, 30, 15);
    glPopMatrix();

        // Telhado da torre
        glPushMatrix();
            glTranslatef(1.0f, 0.625f, -1.5f);
            glRotatef(-90,1,0,0);             // rotaciona
            glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
            gluCylinder(ObjetoPrincipal, 0.18f, 0.0f, 0.35f, 30, 15);
        glPopMatrix();
    // Parede entre torre esquerda atras e torre esquerda frente
    // parede 2-6
    glPushMatrix();
        glTranslatef(1.0f, 0.28f, -1.5f); 
        //glRotatef(-180, 1, 0, -0.30f);
        //glTranslatef(0.10f,0.22f,-0.75f); // -0.5 pois agora essa retângulo está de cabeiça p/ baixo
        gluCylinder(ObjetoPrincipal, 0.175f, 0.175f, 1.5f, 2, 1);
    glPopMatrix();

    // Parede entre torre esquerda atras e torre esquerda frente
    // parede 1-2
    glPushMatrix();
        glTranslatef(-1.0f, 0.28f, -1.5f); 
        glRotatef(90, 0, 1, 0);
        //glTranslatef(0.10f,0.22f,-0.75f); // -0.5 pois agora essa retângulo está de cabeiça p/ baixo
        gluCylinder(ObjetoPrincipal, 0.175f, 0.175f, 2.0f, 2, 1);
    glPopMatrix();

    // Torre centro-esquerda
    // torre 4
    glPushMatrix();
        glTranslatef(-1.0f, 0.625f, 0.0f);
        glRotatef(90,1,0,0);             // rotaciona
        glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
        gluCylinder(ObjetoPrincipal, 0.15f, 0.15f, 0.5f, 30, 15);
    glPopMatrix();

        // Telhado da Torre
        glPushMatrix();
            glTranslatef(-1.0f, 0.625f, 0.0f);
            glRotatef(-90,1,0,0);             // rotaciona
            glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
            gluCylinder(ObjetoPrincipal, 0.18f, 0.0f, 0.35f, 30, 15);
        glPopMatrix();

    // Parede entre torre centro-esquerda e gate house e torre direita
    // parede 4-5-6
    glPushMatrix();
        glTranslatef(-0.0f, 0.125f, -0.0f); 
        glRotatef(-90, 1.0f, 0.0f, 0.0f);
        glRotatef(-90, 0.0f, 0.0f, 1.0f);
        //glTranslatef(0.10f,0.22f,-0.75f); // -0.5 pois agora essa retângulo está de cabeiça p/ baixo
        gluCylinder(ObjetoPrincipal, 1.0f, 1.0f, 0.35f, 2, 1);
    glPopMatrix();


    // Torre atrás da gate-house
    // torre do meio
    // torre 3
    glPushMatrix();
        glTranslatef(-1.0f, 1.0f, -0.75f);
        glRotatef(90,1,0,0);
        glTranslatef(1.0f, 0.0f, 0.0f);
        gluCylinder(ObjetoPrincipal, 0.15f, 0.15f, 0.85f, 4, 2);
    glPopMatrix();

        // Telhado da Torre atrás da gate-house
        glPushMatrix();
            //glTranslatef(-1.0f, 1.0f, -0.75f);
            glTranslatef(0.0f,1.0f,-0.75f);
            glRotatef(90,1,0,1);
            
            //glTranslatef(0.0f,-0.75f,0.75f);
            //glTranslatef(0.0f,0.0f,0.0f);
            glutSolidCube(0.17f);
            // glRotatef(90,1,0,1);
            // glTranslatef(0.5f, -0.7f, 0.5f);
            // gluSphere(ObjetoPrincipal, 0.16f, 4, 2);
        glPopMatrix();

    // Gate-house
    // torre 5
    glPushMatrix();
        glTranslatef(-1.0f, 0.625f, 0.0f);
        glRotatef(90,1,0,0);
        glTranslatef(1.0f, 0.0f, 0.0f);
        gluCylinder(ObjetoPrincipal, 0.2f, 0.2f, 0.5f, 4, 2);
    glPopMatrix();

        // Telhado da Gate-House
        glPushMatrix();
            glTranslatef(-1.0f, 0.625f, 0.0f);
            glRotatef(-90,1,0,0);
            glTranslatef(1.0f, 0.0f, 0.0f);
            gluCylinder(ObjetoPrincipal, 0.2f, 0.0f, 0.25f, 4, 2);
        glPopMatrix();

    

    // Torre da Direita
    // torre 6
    glPushMatrix();
        glTranslatef(1.0f, 0.625f, 0.0f);
        glRotatef(90,1,0,0);             // rotaciona
        glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
        gluCylinder(ObjetoPrincipal, 0.15f, 0.15f, 0.5f, 30, 15);
    glPopMatrix();

    // Telhado da Torre
        glPushMatrix();
            glTranslatef(1.0f, 0.625f, 0.0f);
            glRotatef(-90,1,0,0);           // rotaciona
            glTranslatef(0.0f, 0.0f, 0.0f); // para que esteja orientado no eixo y
            gluCylinder(ObjetoPrincipal, 0.18f, 0.0f, 0.35f, 30, 15);
        glPopMatrix();

        // laje do telhado da torre        
        glPushMatrix();
            glTranslatef(0.0f, 1.0f, -0.75f); 
            glRotatef(90, 0.0f, 0.0f, 1.0f);
            glRotatef(45, 1.0f, 0.0f, 0.0f);
            glTranslatef(0.0f, 0.0f, -0.11f); 
            gluCylinder(ObjetoPrincipal, 0.11f, 0.11f, 0.22f, 2, 1);
        glPopMatrix();
        


// gluCylinder(pObj, RaioBase, RaioTopo, Altura, Lat, Long);
// glRect(x1, y1, x2, y2)
         
    // Restore the matrix state  
    glPopMatrix();  
    // Buffer swap  
    glutSwapBuffers();  

}  

int main(int argc, char *argv[]){

    glutInit(&argc, argv);  
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);  // define o modo de display
    glutInitWindowSize(1300, 700);  // inicializa a janela, com tamanho sendo o argumento passado
    glutCreateWindow("Castelo");  // cria a janela
    glutReshapeFunc(ChangeSize);  // da resize na janela, se necessário
    glutSpecialFunc(SpecialKeys); // define o que fazer ao receber um input
    glutDisplayFunc(RenderScene); // cria a cena e renderiza ela
    SetupRC();  
    glutMainLoop();  
    
    return 0;
}