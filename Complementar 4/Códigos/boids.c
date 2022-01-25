#include <GL/glut.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <math.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define NUM_BOIDS 20
#define RAIO_BOID 0.2
#define STEP_BOID 0.025

int window;
int lider;
static GLfloat ROTACAO_X = 0.0f;
static GLfloat ROTACAO_Y = 0.0f;
static GLfloat ROTACAO_Z = 0.0f;

static GLfloat TRANSLACAO_X = 0.0f;
static GLfloat TRANSLACAO_Y = 0.0f;
static GLfloat TRANSLACAO_Z = 0.0f;

typedef struct{
    float x, y, z;
}coord;

coord pos_boids[NUM_BOIDS]; // vetor que contém as posições de todos os boids
coord lider_target; // para onde o lider quer chegar
typedef struct{
    coord ponto1, ponto2; // pontos reservados
}reserved_coordinates[NUM_BOIDS]; // vetor que contém as coordenadas de pontos reservados para movimento dos boids

// struct boids{// boids serão representados como esferas
//     coord pos; // coordenadas do centro
//     float raio; // raio da esfera
// }boids[NUM_BOIDS];

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

void initCoord(coord *a){
    a->x = -1;
    a->y = -1;
    a->z = -1;
}

int coordInArray(coord a, coord *b, int end){
    for(int i = 0; i++; i<end){
        if(a.x == b[i].x){
            if(a.y == b[i].y){
                if(a.z == b[i].z){
                    return 1;
                }
            }
        }
    }
    return 0;
}

int coordInArrayMinusZ(coord a, coord *b, int end){
    for(int i = 0; i++; i<end){
        if(a.x == b[i].x){
            if(a.y == b[i].y){
                return 1;
            }
        }
    }
    return 0;
}

int checkIntersection(coord boid1, coord boid2){
    if(boid1.x - RAIO_BOID <= boid2.x + RAIO_BOID)
        return 1;
    if(boid1.x + RAIO_BOID >= boid2.x - RAIO_BOID)
        return 1;
    if(boid1.y - RAIO_BOID <= boid2.y + RAIO_BOID)
        return 1;
    if(boid1.y + RAIO_BOID >= boid2.y - RAIO_BOID)
        return 1;
    if(boid1.z - RAIO_BOID <= boid2.z + RAIO_BOID)
        return 1;
    if(boid1.z + RAIO_BOID >= boid2.z - RAIO_BOID)
        return 1;
    return 0;
}

int checkIntersectionArray(coord a, coord *b, int end){
    for(int i = 0; i++; i < end){
        if(checkIntersection(a, b[i])){
            return 1;
        }
    }
    return 0;
}

int checkTouch(coord boid1, coord boid2){ // é necessário?
    if(boid1.x - RAIO_BOID == boid2.x + RAIO_BOID)
        return 1;
    if(boid1.x + RAIO_BOID == boid2.x - RAIO_BOID)
        return 1;
    if(boid1.y - RAIO_BOID == boid2.y + RAIO_BOID)
        return 1;
    if(boid1.y + RAIO_BOID == boid2.y - RAIO_BOID)
        return 1;
    if(boid1.z - RAIO_BOID == boid2.z + RAIO_BOID)
        return 1;
    if(boid1.z + RAIO_BOID == boid2.z - RAIO_BOID)
        return 1;
    return 0;
}

void initScene(void){
    int r, i = 0;
    coord pos;
    initCoord(&pos);
    while(i < NUM_BOIDS){
        do{
            r = rand() % 10;
            r = r%2 == 0 ? 1 : -1;
            pos.x = r * ((float)rand()/(float)(RAND_MAX)) * 2;
            pos.y = r * ((float)rand()/(float)(RAND_MAX)) * 1;
            pos.z = r * ((float)rand()/(float)(RAND_MAX)) * 2;
        }while((coordInArrayMinusZ(pos, pos_boids, i) == 1) || (checkIntersectionArray(pos, pos_boids, i) == 1));
        pos_boids[i].x = pos.x;
        pos_boids[i].y = pos.y;
        pos_boids[i].z = pos.z;
        i++;
    }

    i = 0;
    while(i < NUM_BOIDS){
        reserved_coordinates[i] = {{-99,-99,-99},{-99,-99,-99}}; // inicializando vetor de coordenadas reservadas
    }
    lider = rand()%20;// seleciona um boid aleatóriamente para ser o "lider" do grupo
                      // os outros boids tentarão seguir o lider

    printf("Lider: %d\n", lider);

    r = rand() % 10;
    r = r%2 == 0 ? 1 : -1;
    lider_target.x = r * ((float)rand()/(float)(RAND_MAX)) * 3;
    lider_target.y = r * ((float)rand()/(float)(RAND_MAX)) * 3;
    lider_target.z = r * ((float)rand()/(float)(RAND_MAX)) * 3;
}

void SetupRC(){  

    GLfloat  whiteLight[] = { 0.05f, 0.05f, 0.05f, 1.0f };  
    GLfloat  sourceLight[] = { 0.25f, 0.25f, 0.25f, 1.0f };  
    GLfloat  lightPos[] = { -10.f, 5.0f, 5.0f, 1.0f };  
  
    glEnable(GL_DEPTH_TEST);
    glFrontFace(GL_CCW);
    glEnable(GL_CULL_FACE);
  
    glEnable(GL_LIGHTING);  
  
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight);  
    glLightfv(GL_LIGHT0,GL_AMBIENT,sourceLight);  
    glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight);  
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos);  
    glEnable(GL_LIGHT0);  
  
    glEnable(GL_COLOR_MATERIAL);  
      
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);  
  
    glClearColor(0.25f, 0.25f, 0.50f, 1.0f);  
    initScene();
}  

void keyboard (unsigned char key, int x, int y){
    switch (key) {
        case 'w':
        case 'W':
            TRANSLACAO_X += 0.5f;
            glutPostRedisplay();
            break;
        case 's':
        case 'S':
            TRANSLACAO_X -= 0.5f;
            glutPostRedisplay();
            break;

        case 'e':
        case 'E':
            TRANSLACAO_Y += 0.5f;
            glutPostRedisplay();
            break;
        case 'd':
        case 'D':
            TRANSLACAO_Y -= 0.5f;
            glutPostRedisplay();
            break;

        case 'r':
        case 'R':
            TRANSLACAO_Z += 0.5f;
            glutPostRedisplay();
            break;
        case 'f':
        case 'F':
            TRANSLACAO_Z -= 0.5f;
            glutPostRedisplay();
            break;

        case 27:
            printf("Fechando...\n");
            glutDestroyWindow(window); 
            exit(0);

        case 32:
            printf("Reiniciando...\n");
        
        default:
            break;
    }

}

void SpecialKeys(int key, int x, int y){  
    if(key == GLUT_KEY_UP)
        ROTACAO_X += 5.0f;

    if(key == GLUT_KEY_DOWN)
        ROTACAO_X -= 5.0f;

    if(key == GLUT_KEY_LEFT)  
        ROTACAO_Y -= 5.0f;  
  
    if(key == GLUT_KEY_RIGHT)  
        ROTACAO_Y += 5.0f;  
    
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

void drawObstacle(void){
    GLUquadricObj *Obstaculos;

    Obstaculos = gluNewQuadric();
    gluQuadricNormals(Obstaculos, GLU_SMOOTH);  

}

void moveBoid(coord *boid_orig, coord target, float passo, int boid){  
    // tenta mover o boid em boid_orig para target
    // verifica se o ponto a um "passo" de distancia do boid está livre, se sim, move ele para lá 
    // e reserva os dois próximos pontos
    // se não estiver, procura outro

    float passo_x, passo_y, passo_z;

    if(boid_orig->x >= target.x)
        passo_x = passo;
    else
        passo_x = -1*passo;

    if(boid_orig->y >= target.y)
        passo_y = passo;
    else
        passo_y = -1*passo;

    if(boid_orig->z >= target.z)
        passo_z = passo;
    else
        passo_z = -1*passo;

    if(boid_orig->x - target.x < passo_x) // não funciona, arrumar
        passo_x = boid_orig->x - target.x;

    if(boid_orig->y - target.y < passo_y)
        passo_y = boid_orig->y - target.y;

    if(boid_orig->z - target.z < passo_z)
        passo_z = boid_orig->z - target.z;

    

}

void boidController(void){
    // controla como os boids vão se comportar na cena

    // primeiro a se mover é o lider
    moveBoid(&pos_boids[lider], lider_target, STEP_BOID*2, lider);
}

void drawBoids(void){
    int i = 0;
    GLUquadricObj *Boid[NUM_BOIDS];
    float boid_x, boid_y, boid_z;

    while(i < NUM_BOIDS){
        Boid[i] = gluNewQuadric();
        i++;
    }
    i = 0;

    while(i < NUM_BOIDS){
        gluQuadricNormals(Boid[i], GLU_SMOOTH);  
        i++;
    }
    i = 0;

    glPushMatrix();
        while(i < NUM_BOIDS){
            if(i == lider)
                glColor3f (0.0, 1.0, 0.0);    
            else
                glColor3f (1.0, 1.0, 1.0);
            boid_x = pos_boids[i].x;
            boid_y = pos_boids[i].y;
            boid_z = pos_boids[i].z;

            glTranslatef(boid_x, boid_y, boid_z);
            gluSphere(Boid[i], RAIO_BOID, 30, 15);
            i++;
        }
        i = 0;
    glPopMatrix();
    boidController();
    
}

void RenderScene(void){  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  
    
    glPushMatrix(); 

        glTranslatef(0.0f, -1.0f, -7.0f);
        // glRotatef(90, 0.0f, -1.0f, -7.0f);
        glRotatef(ROTACAO_X, 1.0f, 0.0f, 0.0f);
        glRotatef(ROTACAO_Y, 0.0f, 1.0f, 0.0f);
        glRotatef(ROTACAO_Z, 0.0f, 0.0f, 1.0f);

        glTranslatef(TRANSLACAO_X, 0.0f, 0.0f);
        glTranslatef(0.0f, TRANSLACAO_Y, 0.0f);
        glTranslatef(0.0f, 0.0f, TRANSLACAO_Z);

        glColor3f (1.0, 1.0, 1.0);

        glPushMatrix();
            drawBoids();
        glPopMatrix();

    glPopMatrix();  
    glutSwapBuffers();  

}  

int main(int argc, char *argv[]){
    srand((unsigned int)time(NULL));

    glutInit(&argc, argv);  
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    window = glutCreateWindow("Boids");
    glutReshapeFunc(ChangeSize);
    glutDisplayFunc(RenderScene);
    glutKeyboardFunc(&keyboard);
    glutSpecialFunc(SpecialKeys);
    glutFullScreen();
    SetupRC();
    glutMainLoop();  
    
    return 0;
}
