import numpy as np
import pygame
import time
import random

def generarLaberintoDFS(nxC,nyC):
    stack=[]
    estado=np.ones((nxC,nyC))
    visited=np.zeros((nxC,nyC))
    stack.append((0,0))
    visited[0,0]=1
    estado[0,0]=0
    while len(stack) > 0:
        vecinos=[]
        cell=stack.pop()
        aux=[(0,2),(2,0),(0,-2),(-2,0)]
        random.shuffle(aux)
        i=0
        while i<4:
            cx = cell[0] + aux[i][0]
            cy = cell[1] + aux[i][1]
            if cx >= 0 and cx < nxC and cy >= 0 and cy < nyC:
                newcell=(cell[0]+aux[i][0],cell[1]+aux[i][1])
                if visited[newcell[0],newcell[1]] == 0:
                    vecinos.append(newcell)
            i+=1


        if len(vecinos)>1:
            stack.append(cell)
        if len(vecinos)>0:
            newcell=vecinos[0]
            visited[newcell[0],newcell[1]]=1
            estado[newcell[0],newcell[1]]=0
            estado[int((cell[0]+newcell[0])/2),int((cell[1]+newcell[1])/2)]=0
            stack.append(newcell)

    return(estado)




pygame.init()

width, height = 500, 500
screen = pygame.display.set_mode((width, height + 100))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 45, 45
dimCW = width / nxC
dimCH = height / nyC



# Estado de las celdas: Muro=1 Vacio=0 Visitado=2 Inicio=3
state = np.zeros((nxC, nyC))


pausa = True

while True:

    newState = np.copy(state)

    screen.fill(bg)
    time.sleep(0.1)

    #Boton de reset
    reset = [(25.0, width + 25.0),
             (height / 5 + 25.0, width + 25.0),
             (height / 5 + 25.0, width + 75.0),
             (25.0, width + 75.0)]

    pygame.draw.polygon(screen, (128, 128, 128), reset, width=1)

    font = pygame.font.SysFont(None, 40)
    textoReset = font.render('RESET', True, (128,128,128))
    screen.blit(textoReset, ((reset[0][0]+reset[2][0])/2-45 , (reset[0][1]+reset[2][1])/2-13))


    #Boton de generar laberinto
    generar = [(25.0 + 125.0, height + 25.0 ),
             (width / 5 + 25.0 +125.0, height + 25.0),
             (width / 5 + 25.0+125.0, height + 75.0),
             (25.0+125.0, height + 75.0)]

    pygame.draw.polygon(screen, (128, 128, 128), generar, width=1)

    font = pygame.font.SysFont(None, 38)
    textoReset = font.render('GENER', True, (128, 128, 128))
    screen.blit(textoReset, ((generar[0][0] + generar[2][0]) / 2 - 45, (generar[0][1] + generar[2][1]) / 2 - 13))



    # Pulsaciones de teclado y raton
    evento = pygame.event.get()

    for tecla in evento:
        if tecla.type == pygame.KEYDOWN:
            pausa = not pausa

        click = pygame.mouse.get_pressed()


        if click==(1,0,0):
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            if celY >= 0 and celY < nyC:
                state[celX, celY] = 1
                newState[celX, celY] = 1

            if posX>= reset[0][0] and posX<reset[2][0] and posY>=reset[0][1] and posY<reset[2][1]:
                newState=np.zeros((nxC,nyC))
                state=np.zeros((nxC,nyC))

            if posX>= generar[0][0] and posX<generar[2][0] and posY>=generar[0][1] and posY<generar[2][1]:
                newState=generarLaberintoDFS(nxC,nyC)
                state=np.copy(newState)

        if click==(0,0,1):
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            if celY >= 0 and celY < nyC:
                state[celX, celY] = 0
                newState[celX, celY] = 0

        if click==(0,1,0):
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            if celY >= 0 and celY < nyC:
                state[celX, celY] = 3
                newState[celX, celY] = 3



    for x in range(0, nxC):
        for y in range(0, nyC):

            if not pausa:
                vecinos = 0

                if x + 1 < nxC:
                    if state[x + 1, y] == 2 or state[x + 1, y] == 3:
                        vecinos += 1

                if y - 1 >= 0:
                    if state[x, y - 1] == 2 or state[x, y - 1] == 3:
                        vecinos += 1

                if x - 1 >= 0:
                    if state[x - 1, y] == 2 or state[x - 1, y] == 3:
                        vecinos += 1

                if y + 1 < nyC:
                    if state[x, y + 1] == 2 or state[x, y + 1] == 3:
                        vecinos += 1

                '''
                Las cosas que no cambian no hace falta implementarlas
                #Si eres un muro, sigues siendo un muro
                if state[x,y]==1:
                    newState[x,y]=1
    
                #Si eres el incio, sigues siendo inicio
                if state[x,y]==3:
                    newState[x,y]=3
    
                #Si ya has sido visitado sigues siendo ya visitado
                if state[x,y]==2:
                    newState[x,y]=2
                '''

                # Si eres vacio, seras visitado si hay algun adyacente, en caso contrario sigues siendo vacio
                if state[x, y] == 0:
                    if vecinos > 0:
                        newState[x, y] = 2
                    else:
                        newState[x, y] = 0

            poly = [(x * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x * dimCW, (y + 1) * dimCH)
                    ]

            if state[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, width=1)
            if state[x, y] == 1:
                pygame.draw.polygon(screen, (255, 255, 255), poly, width=0)
            if state[x, y] == 2:
                pygame.draw.polygon(screen, (255, 128, 0), poly, width=0)
            if state[x, y] == 3:
                pygame.draw.polygon(screen, (0, 51, 204), poly, width=0)

    state = np.copy(newState)



    pygame.display.flip()
