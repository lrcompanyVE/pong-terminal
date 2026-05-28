import curses
from curses import wrapper
import time

def main(stdscr):
    stdscr.clearok(False)
    curses.curs_set(0) 
    stdscr.nodelay(True)
    sh, sw = stdscr.getmaxyx()

    # Jugadores
    player_y = sh // 2





    player_x = 5
    player2_y = sh // 2
    player2_x = sw - 5

    # Puntos
    score1 = 0
    score2 = 0

    # Pelota
    ball_y, ball_x = sh // 2, sw // 2
    ball_vy = 1
    ball_vx = 1

    while True:
        stdscr.erase()
        sh, sw = stdscr.getmaxyx() 
        player2_x = sw - 5 # Mantener al P2 pegado a la derecha

        key = stdscr.getch()
        if key == ord('q'): break

        # Controles P1 (Flechas)
        if key == curses.KEY_UP and player_y > 0:
            player_y -= 1
        if key == curses.KEY_DOWN and player_y < sh - 4:
            player_y += 1

        # Controles P2 (W/S)
        if key == ord('w') and player2_y > 0:
            player2_y -= 1 
        if key == ord('s') and player2_y < sh - 4:
            player2_y += 1

        # Física Pelota
        ball_y += ball_vy
        ball_x += ball_vx

        # Rebotes Techo/Suelo
        if ball_y <= 0 or ball_y >= sh - 1:
            ball_vy *= -1

        # Colisiones (Lógica que ya dominas)
        if ball_x <= player_x + 1 and player_y <= ball_y <= player_y + 3:
            if ball_x >= player_x:
                ball_vx *= -1
                ball_x = player_x + 1

        if ball_x >= player2_x - 1 and player2_y <= ball_y <= player2_y + 3:
            if ball_x <= player2_x:
                ball_vx *= -1
                ball_x = player2_x - 1

        # Puntuación
        if ball_x <= 0:
            score2 += 1
            ball_y, ball_x = sh // 2, sw // 2
            ball_vx = 1
        elif ball_x >= sw - 1:
            score1 += 1
            ball_y, ball_x = sh // 2, sw // 2
            ball_vx = -1

        # --- DIBUJO SEGURO ---
        try:
            # Paletas
            for i in range(4):
                stdscr.addstr(player_y + i, player_x, "█")
                stdscr.addstr(player2_y + i, player2_x, "█")
            
            # Pelota
            stdscr.addstr(int(ball_y), int(ball_x), "●")
            
            # Línea central dinámica
            for i in range(sh):
                stdscr.addstr(i, sw // 2, "|")
            
            # Marcador
            stdscr.addstr(0, sw // 2 - 6, f"P1: {score1} | P2: {score2}")
        except:
            pass # Si la ventana es muy chica, no rompas el juego

        stdscr.refresh()
        time.sleep(0.04)

wrapper(main)
