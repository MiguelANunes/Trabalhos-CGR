#include <GL/glut.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <unistd.h>

int rotacaoBracoE = 0;
int rotacaoBracoD = 0;
int rotacaoCotoveloE = 0;
int rotacaoCotoveloE_EixoY = 0;
int rotacaoCotoveloE_EixoZ = 0;
int rotacaoCotoveloD = 0;
int rotacaoCotoveloD_EixoY = 0;
int rotacaoCotoveloD_EixoZ = 0;
int rotacaoPernaE = 0;
int rotacaoPernaD = 0;
int rotacaoJoelhoE = 0;
int rotacaoJoelhoD = 0;

int flagAndar = 0;
int flagAcenar = 0;
int apexWalk = 0;
int apexWave = 0;
int waveReady = 0;
int total_flips = 0;

static GLfloat ROTACAO_X = 0.0f;
static GLfloat ROTACAO_Y = 0.0f;
static GLfloat ROTACAO_Z = 0.0f;
static GLfloat tamanhoCorpoX = 0.75f;
static GLfloat tamanhoCorpoY = 1.5f;

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


void giraBracoE(void){
    glRotatef((GLfloat) rotacaoBracoE, 1, 0, 0); 
}

void giraCotoveloE(void){
    glRotatef((GLfloat) rotacaoCotoveloE, 1, 0, 0); 
}

void giraCotoveloE_EixoY(void){
    glRotatef((GLfloat) rotacaoCotoveloE_EixoY, 0, 1, 0); 
}

void giraCotoveloE_EixoZ(void){
    glRotatef((GLfloat) rotacaoCotoveloE_EixoZ, 0, 0, 1); 
}

void giraPernaE(void){
    glRotatef((GLfloat) rotacaoPernaE, 1,0,0); 
}

void giraJoelhoE(void){
    glRotatef((GLfloat) rotacaoJoelhoE, 1,0,0); 
}

void giraBracoD(void){
    glRotatef((GLfloat) rotacaoBracoD, 1, 0, 0); 
}

void giraCotoveloD(void){
    glRotatef((GLfloat) rotacaoCotoveloD, 1, 0, 0); 
}

void giraCotoveloD_EixoY(void){
    glRotatef((GLfloat) rotacaoCotoveloD_EixoY, 0, 1, 0); 
}

void giraCotoveloD_EixoZ(void){
    glRotatef((GLfloat) rotacaoCotoveloD_EixoZ, 0, 0, 1); 
}

void giraPernaD(void){
    glRotatef((GLfloat) rotacaoPernaD, 1,0,0); 
}

void giraJoelhoD(void){
    glRotatef((GLfloat) rotacaoJoelhoD, 1,0,0); 
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

    tamanhoCorpoX = 0.75f;
    tamanhoCorpoY = 1.5f;

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
        // glColor3f(1.0f,0.0f,0.0f);
        glTranslatef(0.0f,-tamanhoCorpoX,0.0f);
        glRotatef(90,1.0f,0.0f,0.0f);
        glTranslatef(0,tamanhoCorpoX-(2*tamanhoCorpoY),-(tamanhoCorpoX+tamanhoCorpoY));
        glRectf(0.0f,2*tamanhoCorpoY,tamanhoCorpoX,tamanhoCorpoX+tamanhoCorpoY); // Retangulo Tampa Superior
    glPopMatrix();

    glPushMatrix();
        // glColor3f(0.0f,1.0f,0.0f);
        glTranslatef(0.0f,-tamanhoCorpoX,0.0f);
        glRotatef(-90,1.0f,0.0f,0.0f);
        glTranslatef(0,-2*tamanhoCorpoY,tamanhoCorpoX);
        glRectf(0,2*tamanhoCorpoY,tamanhoCorpoX,tamanhoCorpoX+tamanhoCorpoY); // Retangulo Tampa Inferior
    glPopMatrix();
}

void DesenhaCabeca(void){
    GLfloat tamanhoCabeca; 

    tamanhoCabeca = 0.4f;

    glPushMatrix();
        glTranslatef(-0.125f, tamanhoCorpoY+.125, -0.625f);
        // glColor3f(1.0f, 0.0f, 1.0f);
        glutSolidCube(tamanhoCabeca);
    glPopMatrix();

    glPushMatrix();
        glTranslatef(-.25f, tamanhoCorpoY+.175f, -.45);
        glColor3f(1,0,0);
        glutSolidCube(tamanhoCabeca/5);
    glPopMatrix();

    glPushMatrix();
        glTranslatef(0, tamanhoCorpoY+.175f, -.45);
        glColor3f(1,0,0);
        glutSolidCube(tamanhoCabeca/5);
    glPopMatrix();
}

void DesenhaBracoEsquerdo(void){
    GLfloat raioBraco, comprimentoBraco, tamanhoOmbro, tamanhoCotovelo, raioAnteBraco, comprimentoAnteBraco; 
    GLUquadricObj *Ombro, *Braco, *Cotovelo, *AnteBraco, *Mao;

    Ombro = gluNewQuadric();
    Braco = gluNewQuadric();
    AnteBraco = gluNewQuadric();
    Cotovelo = gluNewQuadric();
    Mao = gluNewQuadric();
	gluQuadricNormals(Ombro, GLU_SMOOTH);  
    gluQuadricNormals(Braco, GLU_SMOOTH);  
    gluQuadricNormals(Cotovelo, GLU_SMOOTH); 
    gluQuadricNormals(AnteBraco, GLU_SMOOTH);
    gluQuadricNormals(Mao, GLU_SMOOTH);

    raioBraco = 0.10f;
    comprimentoBraco = 0.6f;
    tamanhoOmbro = 0.15f;
    tamanhoCotovelo = 0.125f;
    raioAnteBraco = raioBraco;
    comprimentoAnteBraco = (2*comprimentoBraco)/3;

    glPushMatrix();
        glTranslatef(-tamanhoCorpoX+.25,tamanhoCorpoY-.25,-0.55);
        gluSphere(Ombro, tamanhoOmbro, 30, 15);
    glPopMatrix();

    glPushMatrix();
        glTranslatef(-tamanhoCorpoX+.18,tamanhoCorpoY-.25,-0.55);
        giraBracoE();
        glRotatef(45, 0, 0, 1);
        glRotatef(-45, -1, 1, 0);
        gluCylinder(Braco, raioBraco, raioBraco, comprimentoBraco, 4, 2);

        glPushMatrix();
            glTranslatef(-tamanhoCorpoX+.75,tamanhoCorpoY-1.5,.53);
            gluSphere(Cotovelo, tamanhoCotovelo, 30, 15);
        glPopMatrix();

        glPushMatrix();
            glTranslatef(-tamanhoCorpoX+.75,tamanhoCorpoY-1.5,.53);
            glRotatef(-45, 0, 0, 1);
            giraCotoveloE();
            giraCotoveloE_EixoY();
            giraCotoveloE_EixoZ();
            glRotatef(-45, 0, 0, 1);
            gluCylinder(AnteBraco, raioAnteBraco, raioAnteBraco, comprimentoAnteBraco, 4, 2);
            
            glPushMatrix();
                glTranslatef(-tamanhoCorpoX+.75,tamanhoCorpoY-1.5,.43);
                gluSphere(Mao, raioAnteBraco, 30, 15);
            glPopMatrix();
        glPopMatrix();

    glPopMatrix();


    glutSwapBuffers();
}

void DesenhaBracoDireito(void){
    GLfloat raioBraco, comprimentoBraco, tamanhoOmbro, tamanhoCotovelo, raioAnteBraco, comprimentoAnteBraco; 
    GLUquadricObj *Ombro, *Braco, *Cotovelo, *AnteBraco, *Mao;

    Ombro = gluNewQuadric();
    Braco = gluNewQuadric();
    AnteBraco = gluNewQuadric();
    Cotovelo = gluNewQuadric();
    Mao = gluNewQuadric();
	gluQuadricNormals(Ombro, GLU_SMOOTH);  
    gluQuadricNormals(Braco, GLU_SMOOTH);  
    gluQuadricNormals(Cotovelo, GLU_SMOOTH); 
    gluQuadricNormals(AnteBraco, GLU_SMOOTH);
    gluQuadricNormals(Mao, GLU_SMOOTH);

    raioBraco = 0.10f;
    comprimentoBraco = 0.6f;
    tamanhoOmbro = 0.15f;
    tamanhoCotovelo = 0.125f;
    raioAnteBraco = raioBraco;
    comprimentoAnteBraco = (2*comprimentoBraco)/3;

    glPushMatrix();
        glTranslatef(tamanhoCorpoX-.5,tamanhoCorpoY-.25,-0.55);
        gluSphere(Ombro, tamanhoOmbro, 30, 15);
    glPopMatrix();

    glPushMatrix();
        glTranslatef(tamanhoCorpoX-.44,tamanhoCorpoY-.25,-0.55);
        giraBracoD();
        glRotatef(45, 0, 0, 1);
        glRotatef(-45, -1, 1, 0);
        gluCylinder(Braco, raioBraco, raioBraco, comprimentoBraco, 4, 2);

        glPushMatrix();
            glTranslatef(tamanhoCorpoX-.75,tamanhoCorpoY-1.5,0.53);
            gluSphere(Cotovelo, tamanhoCotovelo, 30, 15);
        glPopMatrix();

        glPushMatrix();
            glTranslatef(tamanhoCorpoX-.75,tamanhoCorpoY-1.5,0.53);
            glRotatef(-45, 0, 0, 1);
            giraCotoveloD();
            giraCotoveloD_EixoY();
            giraCotoveloD_EixoZ();
            glRotatef(-45, 0, 0, 1);
            gluCylinder(AnteBraco, raioAnteBraco, raioAnteBraco, comprimentoAnteBraco, 4, 2);

            glPushMatrix();
                glTranslatef(tamanhoCorpoX-.75,tamanhoCorpoY-1.5,0.43);
                gluSphere(Mao, raioAnteBraco, 30, 15);
            glPopMatrix();

        glPopMatrix();

    glPopMatrix();


    glutSwapBuffers();
}

void DesenhaPernaEsquerda(void){
    GLfloat raioCoxa, comprimentoCoxa, tamanhoQuadril, tamanhoJoelho, raioPerna, comprimentoPerna; 
    GLUquadricObj *Quadril, *Coxa, *Joelho, *Perna, *Pe;

    GLfloat altura = 0;

    Quadril = gluNewQuadric();
    Coxa = gluNewQuadric();
    Perna = gluNewQuadric();
    Joelho = gluNewQuadric();
    Pe = gluNewQuadric();
	gluQuadricNormals(Quadril, GLU_SMOOTH);  
    gluQuadricNormals(Coxa, GLU_SMOOTH);  
    gluQuadricNormals(Joelho, GLU_SMOOTH); 
    gluQuadricNormals(Perna, GLU_SMOOTH);
    gluQuadricNormals(Pe, GLU_SMOOTH);

    raioCoxa = 0.10f;
    comprimentoCoxa = 0.4f;
    tamanhoQuadril = 0.15f;
    tamanhoJoelho = 0.125f;
    raioPerna = raioCoxa;
    comprimentoPerna = (2*comprimentoCoxa)/3;

    glPushMatrix();
        glTranslatef(-tamanhoCorpoX+.40,altura,-0.4);
        gluSphere(Quadril, tamanhoQuadril, 30, 15);
    glPopMatrix();

    altura -= tamanhoQuadril/2;
    
    glPushMatrix();
        glTranslatef(-tamanhoCorpoX+.40,altura,-0.4);
        giraPernaE();
        glRotatef(90, 1, 0, 0);
        glRotatef(45, 0, 0, 1);
        gluCylinder(Coxa, raioCoxa, raioCoxa, comprimentoCoxa, 4, 2);

        glPushMatrix();
            glTranslatef(-tamanhoCorpoX+.76,altura+.08,0.39);
            gluSphere(Joelho, tamanhoJoelho, 30, 15);
        glPopMatrix();

        glPushMatrix();
            glTranslatef(-tamanhoCorpoX+.76,altura+.08,0.39);
            glRotatef(-45, 0, 0, 1);
            giraJoelhoE();
            glRotatef(-45, 0, 0, 1);
            gluCylinder(Perna, raioPerna, raioPerna, comprimentoPerna, 4, 2);

            glPushMatrix();
                glTranslatef(-tamanhoCorpoX+.75,altura+.07,0.30);
                gluSphere(Pe, raioPerna, 30, 15);
            glPopMatrix();

        glPopMatrix();

    glPopMatrix();


    // altura -= comprimentoPerna;


    glutSwapBuffers();
}

void DesenhaPernaDireita(void){
    GLfloat raioCoxa, comprimentoCoxa, tamanhoQuadril, tamanhoJoelho, raioPerna, comprimentoPerna; 
    GLUquadricObj *Quadril, *Coxa, *Joelho, *Perna, *Pe;

    GLfloat altura = 0;

    Quadril = gluNewQuadric();
    Coxa = gluNewQuadric();
    Perna = gluNewQuadric();
    Joelho = gluNewQuadric();
    Pe = gluNewQuadric();
	gluQuadricNormals(Quadril, GLU_SMOOTH);  
    gluQuadricNormals(Coxa, GLU_SMOOTH);  
    gluQuadricNormals(Joelho, GLU_SMOOTH); 
    gluQuadricNormals(Perna, GLU_SMOOTH);
    gluQuadricNormals(Pe, GLU_SMOOTH);

    raioCoxa = 0.10f;
    comprimentoCoxa = 0.4f;
    tamanhoQuadril = 0.15f;
    tamanhoJoelho = 0.125f;
    raioPerna = raioCoxa;
    comprimentoPerna = (2*comprimentoCoxa)/3;

    glPushMatrix();
        glTranslatef(tamanhoCorpoX-.65,altura,-0.4);
        gluSphere(Quadril, tamanhoQuadril, 30, 15);
    glPopMatrix();

    altura -= tamanhoQuadril/2;

    glPushMatrix();
        glTranslatef(tamanhoCorpoX-.65,altura,-0.4);
        giraPernaD();
        glRotatef(90, 1, 0, 0);
        glRotatef(45, 0, 0, 1);
        gluCylinder(Coxa, raioCoxa, raioCoxa, comprimentoCoxa, 4, 2);
        
        glPushMatrix();
            glTranslatef(-tamanhoCorpoX+.76,altura+.08,.39);
            gluSphere(Joelho, tamanhoJoelho, 30, 15);
        glPopMatrix();

        glPushMatrix();
            glTranslatef(-tamanhoCorpoX+.76,altura+.08,.39);
            glRotatef(-45, 0, 0, 1);
            giraJoelhoD();
            glRotatef(-45, 0, 0, 1);
            gluCylinder(Perna, raioPerna, raioPerna, comprimentoPerna, 4, 2);

            glPushMatrix();
                glTranslatef(-tamanhoCorpoX+.75,altura+.07,.30);
                gluSphere(Pe, raioPerna, 30, 15);
            glPopMatrix();

        glPopMatrix();

    glPopMatrix();

    // 

    // altura -= tamanhoJoelho/2;


    // altura -= comprimentoPerna;


    glutSwapBuffers();
}

void andar(void){
    int flip, angle;

    flip = 0;
    angle = 360;

    usleep(1000);

    if(!apexWalk)
        flip = 0;

    if(apexWalk)
        flip = 1;
    
    // printf("%d %d %d\n", rotacaoBracoE, flip, apexWalk);

    if(!flip){
        rotacaoBracoE = (rotacaoBracoE + 1) % angle;
        rotacaoPernaD = (rotacaoPernaD + 1) % angle;

        rotacaoBracoD = (rotacaoBracoD - 1) % angle;
        rotacaoPernaE = (rotacaoPernaE - 1) % angle;

        if(rotacaoBracoE == 45){
            apexWalk = 1;
        }

    }else{
        rotacaoBracoE = (rotacaoBracoE - 1) % angle;
        rotacaoPernaD = (rotacaoPernaD - 1) % angle;

        rotacaoBracoD = (rotacaoBracoD + 1) % angle;
        rotacaoPernaE = (rotacaoPernaE + 1) % angle;

        if(rotacaoBracoE == -45)
            apexWalk = 0;
    }
    glutPostRedisplay();

}

void wave(){
    int flip = 0;

    if(total_flips == 3){
        if(rotacaoBracoE < 0)
            rotacaoBracoE = (rotacaoBracoE + 1) % 360;

        if(rotacaoBracoE > 0)
            rotacaoBracoE = (rotacaoBracoE - 1) % 360;

        if(rotacaoBracoD < 0)
            rotacaoBracoD = (rotacaoBracoD + 1) % 360;

        if(rotacaoBracoD > 0)
            rotacaoBracoD = (rotacaoBracoD - 1) % 360;

        if(rotacaoCotoveloE > 0)
            rotacaoCotoveloE = (rotacaoCotoveloE - 1) % 360;

        if(rotacaoCotoveloE < 0)
            rotacaoCotoveloE = (rotacaoCotoveloE + 1) % 360;

        if(rotacaoCotoveloD > 0)
            rotacaoCotoveloD = (rotacaoCotoveloD - 1) % 360;

        if(rotacaoCotoveloD < 0)
            rotacaoCotoveloD = (rotacaoCotoveloD + 1) % 360;

        if(rotacaoCotoveloE_EixoY < 0)
            rotacaoCotoveloE_EixoY = (rotacaoCotoveloE_EixoY + 1) % 360;

        if(rotacaoCotoveloE_EixoY > 0)
            rotacaoCotoveloE_EixoY = (rotacaoCotoveloE_EixoY - 1) % 360;

        if(rotacaoCotoveloD_EixoY < 0)
            rotacaoCotoveloD_EixoY = (rotacaoCotoveloD_EixoY + 1) % 360;

        if(rotacaoCotoveloD_EixoY > 0)
            rotacaoCotoveloD_EixoY = (rotacaoCotoveloD_EixoY - 1) % 360;

        glutPostRedisplay();
        return;
    }
    
    usleep(1000);

    if(!apexWave)
        flip = 0;
    
    if(apexWave)
        flip = 1;
    

    if(rotacaoBracoE > -60)
        rotacaoBracoE = (rotacaoBracoE - 1) % 360;

    if(rotacaoBracoD > -60)
        rotacaoBracoD = (rotacaoBracoD - 1) % 360;

    if(rotacaoCotoveloE > -60)
        rotacaoCotoveloE = (rotacaoCotoveloE - 1) % 360;

    if(rotacaoCotoveloD > -60)
        rotacaoCotoveloD = (rotacaoCotoveloD - 1) % 360;

    if(rotacaoBracoE == rotacaoBracoD && rotacaoBracoD == -60){

        if(!flip){
            rotacaoCotoveloE_EixoY = (rotacaoCotoveloE_EixoY + 1) % 360;
            rotacaoCotoveloD_EixoY = (rotacaoCotoveloD_EixoY + 1) % 360;

            if(rotacaoCotoveloE_EixoY == 45){
                apexWave = 1;
                total_flips++;
            }

        }else{
            rotacaoCotoveloE_EixoY = (rotacaoCotoveloE_EixoY - 1) % 360;
            rotacaoCotoveloD_EixoY = (rotacaoCotoveloD_EixoY - 1) % 360;

            if(rotacaoCotoveloE_EixoY == -45){
                apexWave = 0;
                total_flips++;
            }
        }
    }
    glutPostRedisplay();

}

void display(void){
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glColor3f (1.0, 1.0, 1.0);

    glPushMatrix(); // 1
        glTranslatef(0.0f, -0.5f, -6.0f);
        glRotatef(ROTACAO_X, 1.0f, 0.0f, 0.0f);
        glRotatef(ROTACAO_Y, 0.0f, 1.0f, 0.0f);
        glRotatef(ROTACAO_Z, 0.0f, 0.0f, 1.0f);

        glPushMatrix();
            glTranslatef(-0.5f,0,-1);
            DesenhaCorpo();
        glPopMatrix();
        
        glColor3f (1.0, 1.0, 1.0);

        glPushMatrix();
            DesenhaCabeca();
        glPopMatrix();

        glColor3f (1.0, 1.0, 1.0);

        glPushMatrix();
            DesenhaBracoEsquerdo();
        glPopMatrix();

        glColor3f (1.0, 1.0, 1.0);

        glPushMatrix();
            DesenhaBracoDireito();
        glPopMatrix();

        glColor3f (1.0, 1.0, 1.0);

        glPushMatrix();
            DesenhaPernaEsquerda();
        glPopMatrix();

        glColor3f (1.0, 1.0, 1.0);

        glPushMatrix();
            DesenhaPernaDireita();
        glPopMatrix();

        if(flagAndar)
            andar();

        if(flagAcenar)
            wave();
        
    glPopMatrix();

    glutSwapBuffers();
}

void keyboard (unsigned char key, int x, int y){
    switch (key) {
        case 32:
            flagAndar = flagAndar == 0 ? 1 : 0;
            andar();
            glutPostRedisplay();
            break;

        case 127: // delete
            total_flips = 0;
            flagAcenar = flagAcenar == 0 ? 1 : 0;
            wave();
            glutPostRedisplay();
            break;
        // case 'w':
        // case 'W':
        //     rotacaoBracoE = (rotacaoBracoE + 5) % 360;
        //     glutPostRedisplay();
        //     break;
        // case 's':
        // case 'S':
        //     rotacaoBracoE = (rotacaoBracoE - 5) % 360;
        //     glutPostRedisplay();
        //     break;

        // case 'e':
        // case 'E':
        //     rotacaoCotovelo = (rotacaoCotovelo + 5) % 360;
        //     glutPostRedisplay();
        //     break;
        // case 'd':
        // case 'D':
        //     rotacaoCotovelo = (rotacaoCotovelo - 5) % 360;
        //     glutPostRedisplay();
        //     break;

        // case 'r':
        // case 'R':
        //     rotacaoPerna = (rotacaoPerna + 5) % 360;
        //     glutPostRedisplay();
        //     break;
        // case 'f':
        // case 'F':
        //     rotacaoPerna = (rotacaoPerna - 5) % 360;
        //     glutPostRedisplay();
        //     break;

        // case 't':
        // case 'T':
        //     rotacaoJoelho = (rotacaoJoelho + 5) % 360;
        //     glutPostRedisplay();
        //     break;
        // case 'g':
        // case 'G':
        //     rotacaoJoelho = (rotacaoJoelho - 5) % 360;
        //     glutPostRedisplay();
        //     break;

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
    if(key == GLUT_KEY_LEFT)  
        ROTACAO_Y -= 5.0f;  
  
    if(key == GLUT_KEY_RIGHT)  
        ROTACAO_Y += 5.0f;  
    
    if(key == GLUT_KEY_UP)
        ROTACAO_X += 5.0f;

    if(key == GLUT_KEY_DOWN)
        ROTACAO_X -= 5.0f;

    if(key == GLUT_KEY_HOME)
        ROTACAO_Z += 5.0F;
    
    if(key == GLUT_KEY_END)
        ROTACAO_Z -= 5.0F;

    ROTACAO_X = (GLfloat)((const int)ROTACAO_X % 360);  
    ROTACAO_Y = (GLfloat)((const int)ROTACAO_Y % 360);  
    ROTACAO_Z = (GLfloat)((const int)ROTACAO_Z % 360);  
  
    // Refresh the Window  
    glutPostRedisplay();  
}

int main(int argc, char** argv){
   glutInit(&argc, argv);
   glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
   glutInitWindowSize (1300, 700); 
   glutCreateWindow("Robo");
   glutDisplayFunc(display); 
   glutReshapeFunc(ChangeSize);
   glutKeyboardFunc(keyboard);
   glutSpecialFunc(SpecialKeys);
   SetupRC();
   glutMainLoop();
   return 0;
}
