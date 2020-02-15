from part2 import *

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for p in VC.visualObjects:
                p.check_click(event.pos)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                message.rendUpdate()
            if event.key in VC.keyBindings:
                VC.keyBindings[event.key][0](VC.keyBindings[event.key][1])
        if event.type == pygame.MOUSEMOTION:
            for p in VC.visualObjects:
                p.check_motion(event.pos)

    VC.Screen.fill(VC.Black)

    for p in VC.visualObjects:
        p.render()

    pygame.display.flip()
pygame.quit()
