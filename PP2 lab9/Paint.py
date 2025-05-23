import pygame 

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    color = (0, 0, 255)  # Default to blue
    mode = 'free'  # Modes: free, rect, circle, erase, square, right_triangle, equilateral_triangle, rhombus
    drawing = False
    start_pos = None
    shapes = []  # Store drawn shapes

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_w and ctrl_held) or (event.key == pygame.K_F4 and alt_held):
                    return
                # Color selection
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_t:
                    mode = 'rect'
                elif event.key == pygame.K_f:
                    mode = 'free'
                elif event.key == pygame.K_e:
                    mode = 'erase'
                elif event.key == pygame.K_s:
                    mode = 'square'
                elif event.key == pygame.K_q:
                    mode = 'right_triangle'
                elif event.key == pygame.K_w:
                    mode = 'equilateral_triangle'
                elif event.key == pygame.K_x:
                    mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    end_pos = event.pos
                    drawing = False
                    if mode in ['circle', 'rect', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                        shapes.append((mode, color, start_pos, end_pos))
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing and mode == 'free':
                    pygame.draw.circle(screen, color, event.pos, radius)
                elif drawing and mode == 'erase':
                    pygame.draw.circle(screen, (0, 0, 0), event.pos, radius)

        screen_copy = screen.copy()

        # Preview shape if currently dragging
        if drawing and start_pos and mode in ['circle', 'rect', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
            current_pos = pygame.mouse.get_pos()
            rect = pygame.Rect(start_pos, (current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]))
            if mode == 'circle':
                pygame.draw.ellipse(screen_copy, color, rect, 2)
            elif mode == 'rect':
                pygame.draw.rect(screen_copy, color, rect, 2)
            elif mode == 'square':
                side = min(rect.width, rect.height)
                pygame.draw.rect(screen_copy, color, (rect.x, rect.y, side, side), 2)
            elif mode == 'right_triangle':
                pygame.draw.polygon(screen_copy, color, [(rect.x, rect.y), (rect.x, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height)], 2)
            elif mode == 'equilateral_triangle':
                pygame.draw.polygon(screen_copy, color, [(rect.x, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height), (rect.x + rect.width // 2, rect.y)], 2)
            elif mode == 'rhombus':
                pygame.draw.polygon(screen_copy, color, [(rect.x + rect.width // 2, rect.y), (rect.x, rect.y + rect.height // 2), (rect.x + rect.width // 2, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height // 2)], 2)

        # Redraw stored shapes
        for shape in shapes:
            kind, c, p1, p2 = shape
            rect = pygame.Rect(p1, (p2[0] - p1[0], p2[1] - p1[1]))
            if kind == 'circle':
                pygame.draw.ellipse(screen_copy, c, rect)
            elif kind == 'rect':
                pygame.draw.rect(screen_copy, c, rect)
            elif kind == 'square':
                side = min(rect.width, rect.height)
                pygame.draw.rect(screen_copy, c, (rect.x, rect.y, side, side))
            elif kind == 'right_triangle':
                pygame.draw.polygon(screen_copy, c, [(rect.x, rect.y), (rect.x, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height)])
            elif kind == 'equilateral_triangle':
                pygame.draw.polygon(screen_copy, c, [(rect.x, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height), (rect.x + rect.width // 2, rect.y)])
            elif kind == 'rhombus':
                pygame.draw.polygon(screen_copy, c, [(rect.x + rect.width // 2, rect.y), (rect.x, rect.y + rect.height // 2), (rect.x + rect.width // 2, rect.y + rect.height), (rect.x + rect.width, rect.y + rect.height // 2)])

        screen.blit(screen_copy, (0, 0))
        pygame.display.flip()
        clock.tick(60)

main()
