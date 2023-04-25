import pygame, sys
import math

screen = pygame.display.set_mode((1200, 700))
fps = 60
clock = pygame.time.Clock()


def endPoint(start,degree):
    d = 1500
    dx = d*math.sin(degree*math.pi/180)
    dy = abs(d*math.cos(degree*math.pi/180))
    x = start[0]+ dx
    y = start[1]+ dy
    if 0<degree<180:
        y -= dy*2
    return [round(x,5),round(y,5)]



def main():
    print(endPoint((400, 700), 10))
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #
    #     pygame.display.flip()
    #     clock.tick(fps)

if __name__ == '__main__':
    main()
