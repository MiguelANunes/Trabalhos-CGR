#include <GL/glut.h>
#include <stdlib.h>

int shoulder = 0, elbow = 0;

static GLfloat ROTACAO_Y = 0.0f;
static GLfloat ROTACAO_X = 0.0f;

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

void DesenhaCorpo(void){

    // GLfloat posicaoCorpoX, posicaoCorpoY, posicaoCorpoZ;
    GLfloat tamanhoCorpoX, tamanhoCorpoY; 

    tamanhoCorpoX = 1.0f;
    tamanhoCorpoY = 1.75f;

    glTranslatef(-0.5f,0,0);

    glPushMatrix();
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Frontal
    glPopMatrix();

    glPushMatrix();
        glTranslatef(tamanhoCorpoX,0.0f,tamanhoCorpoX);
        glRotatef(180,0.0f,1.0f,0.0f);
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Fundo Frontal
    glPopMatrix();

    glPushMatrix();
        glTranslatef(0.0f,0.0f,tamanhoCorpoX);
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Traseiro
    glPopMatrix();

    glPushMatrix();
        glTranslatef(tamanhoCorpoX,0.0f,0.0f);
        glRotatef(180,0.0f,1.0f,0.0f);
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Fundo Traseiro
    glPopMatrix();

    glPushMatrix();
        // glTranslatef(0.0f,0.0f,1.0f);
        glRotatef(-90,0.0f,1.0f,0.0f);
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Parede Esquerda
    glPopMatrix();

    glPushMatrix();
        glTranslatef(0.0f,0.0f,tamanhoCorpoX);
        glRotatef(-270,0.0f,1.0f,0.0f);
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Fundo Parede Esquerda
    glPopMatrix();

    glPushMatrix();
        glTranslatef(tamanhoCorpoX,0.0f,tamanhoCorpoX);
        glRotatef(90,0.0f,1.0f,0.0f);
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Parede Direita
    glPopMatrix();

    glPushMatrix();
        glTranslatef(tamanhoCorpoX,0.0f,0.0f);
        glRotatef(-90,0.0f,1.0f,0.0f);
        glRectf(0.0f,0.0f,tamanhoCorpoX,tamanhoCorpoY); // Retângulo Fundo Parede Direita
    glPopMatrix();

    glPushMatrix();
        glColor3f(1.0f,0.0f,0.0f);
        glTranslatef(0.0f,-tamanhoCorpoX,0.0f);
        glRotatef(90,1.0f,0.0f,0.0f);
        glTranslatef(0,tamanhoCorpoX-(2*tamanhoCorpoY),-(tamanhoCorpoX+tamanhoCorpoY));
        glRectf(0.0f,2*tamanhoCorpoY,tamanhoCorpoX,tamanhoCorpoX+tamanhoCorpoY-.25); // Retangulo Tampa Superior
    glPopMatrix();

    glPushMatrix();
        glColor3f(0.0f,1.0f,0.0f);
        glTranslatef(0.0f,-tamanhoCorpoX,0.0f);
        glRotatef(-90,1.0f,0.0f,0.0f);
        glTranslatef(0,-2*tamanhoCorpoY,tamanhoCorpoX);
        glRectf(0,2*tamanhoCorpoY,tamanhoCorpoX,tamanhoCorpoX+tamanhoCorpoY-.25); // Retangulo Tampa Inferior
    glPopMatrix();
}

void display(void){
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glColor3f (1.0, 1.0, 1.0);
    glPushMatrix(); // 1
        glTranslatef(0.0f, -1.0f, -5.0f); // faz uma translação na matriz de modelos
        glRotatef(ROTACAO_Y, 0.0f, 1.0f, 0.0f);  // faz uma rotação na matriz de modelos
        glRotatef(ROTACAO_X, 1.0f, 0.0f, 0.0f);

        DesenhaCorpo();
        
        
        //     glTranslatef (-1.0, 0.0, 0.0);
        //     glRotatef ((GLfloat) shoulder, 0.0, 0.0, 1.0);
        //     glTranslatef (1.0, 0.0, 0.0);
        //     glBegin(GL_QUADS);
        //         glVertex2f(1.0, 0.1);
        //         glVertex2f(1.0, -0.1);
        //         glVertex2f(-1.0, -0.1);
        //         glVertex2f(-1.0, 0.1);
        //     glEnd();

        // glPushMatrix(); // 2
        //     glTranslatef (1.0, 0.0, 0.0);
        //     glRotatef ((GLfloat) elbow, 0.0, 0.0, 1.0);
        //     glTranslatef (1.0, 0.0, 0.0);
        //     glBegin(GL_QUADS);
        //         glVertex2f(1.0, 0.1);
        //         glVertex2f(1.0, -0.1);
        //         glVertex2f(-1.0, -0.1);
        //         glVertex2f(-1.0, 0.1);
        //     glEnd();
        // glPopMatrix(); // 2

    glPopMatrix(); // 1

    glutSwapBuffers();
}


void keyboard (unsigned char key, int x, int y){
    switch (key) {
        case 's':
        case 'S':
            shoulder = (shoulder - 5) % 360;
            glutPostRedisplay();
            break;
        case 'e':
        case 'E':
            elbow = (elbow - 5) % 360;
            glutPostRedisplay();
            break;
        case 'q':
        case 'Q':
        case 27:
            exit(0);
            break;

        default:
            break;
    }
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

int main(int argc, char** argv){
   glutInit(&argc, argv);
   glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
   glutInitWindowSize (1300, 700); 
   glutCreateWindow("Robo");
   SetupRC();
   glutDisplayFunc(display); 
   glutReshapeFunc(ChangeSize);
   glutKeyboardFunc(keyboard);
   glutSpecialFunc(SpecialKeys);
   glutMainLoop();
   return 0;
}