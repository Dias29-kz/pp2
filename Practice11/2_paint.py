import pygame, math

pygame.init()

screen = pygame.display.set_mode((800,600))
screen.fill((255,255,255))

drawing = False
start = None

# Current shape
shape = "square"

def draw_shape(surf, start, end):
    """Draw selected shape"""
    x1,y1 = start
    x2,y2 = end

    # Square
    if shape=="square":
        pygame.draw.rect(surf,(0,0,0),(x1,y1,x2-x1,x2-x1),2)

    # Right triangle
    elif shape=="right":
        pygame.draw.polygon(surf,(0,0,0),[(x1,y1),(x1,y2),(x2,y2)],2)

    # Equilateral triangle
    elif shape=="equilateral":
        side=abs(x2-x1)
        h=side*math.sqrt(3)/2
        pygame.draw.polygon(surf,(0,0,0),
                            [(x1,y1),(x1+side,y1),(x1+side/2,y1-h)],2)

    # Rhombus
    elif shape=="rhombus":
        pygame.draw.polygon(surf,(0,0,0),
                            [(x1,y1),(x2,(y1+y2)//2),(x1,y2),((x1+x2)//2,y1)],2)


running=True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

        # Change shape with keys
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_1: shape="square"
            if e.key==pygame.K_2: shape="right"
            if e.key==pygame.K_3: shape="equilateral"
            if e.key==pygame.K_4: shape="rhombus"

        # Start drawing
        if e.type==pygame.MOUSEBUTTONDOWN:
            start=pygame.mouse.get_pos()
            drawing=True

        # Finish drawing
        if e.type==pygame.MOUSEBUTTONUP:
            end=pygame.mouse.get_pos()
            draw_shape(screen,start,end)
            drawing=False

    pygame.display.update()

pygame.quit()