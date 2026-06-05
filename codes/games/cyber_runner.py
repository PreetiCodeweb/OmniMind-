"""
╔══════════════════════════════════════════╗
║         CYBER RUNNER  by OmniMind        ║
║  Collect data packets. Dodge malware.    ║
╚══════════════════════════════════════════╝
Controls:  SPACE / UP  →  Jump
           R           →  Restart (after game over)
           ESC         →  Quit
"""

import pygame
import random
import math
import sys

# ── Constants ──────────────────────────────────────────────────────────────
W, H = 900, 500
FPS  = 60

# Palette
BG_TOP    = (5,   8,  20)
BG_BOT    = (10, 18,  45)
C_GRID    = (20,  35,  80)
C_GROUND  = (30,  50, 140)
C_GLOW    = (80, 120, 255)
C_PLAYER  = (100, 180, 255)
C_PACKET  = (0,   230, 180)
C_MALWARE = (255,  60,  80)
C_TEXT    = (220, 230, 255)
C_DIM     = (80,  95, 140)
C_GOLD    = (255, 210,  60)
C_WHITE   = (255, 255, 255)

GROUND_Y  = 390          # top of ground strip
PLAYER_X  = 110
JUMP_VEL  = -16
GRAVITY   = 0.7
TILE_W    = 60

# ── Helpers ────────────────────────────────────────────────────────────────

def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def draw_glow_rect(surf, color, rect, radius=8, alpha=80):
    s = pygame.Surface((rect[2]+20, rect[3]+20), pygame.SRCALPHA)
    glow_col = color + (alpha,)
    pygame.draw.rect(s, glow_col, (10, 10, rect[2], rect[3]), border_radius=radius+4)
    surf.blit(s, (rect[0]-10, rect[1]-10))

def draw_rounded(surf, color, rect, r=6):
    pygame.draw.rect(surf, color, rect, border_radius=r)

# ── Particle ───────────────────────────────────────────────────────────────

class Particle:
    def __init__(self, x, y, color, vel=None):
        self.x, self.y = float(x), float(y)
        self.color = color
        angle = random.uniform(0, math.pi*2)
        spd   = random.uniform(1.5, 5)
        self.vx = math.cos(angle)*spd if vel is None else vel[0]+random.uniform(-1,1)
        self.vy = math.sin(angle)*spd if vel is None else vel[1]+random.uniform(-1,1)
        self.life = random.randint(18, 35)
        self.max_life = self.life
        self.size = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.life -= 1

    def draw(self, surf):
        t = self.life / self.max_life
        alpha = int(255 * t)
        col = lerp_color((0,0,0), self.color, t) + (alpha,)
        r = max(1, int(self.size * t))
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (r, r), r)
        surf.blit(s, (int(self.x)-r, int(self.y)-r))

# ── Player ─────────────────────────────────────────────────────────────────

class Player:
    W, H = 34, 42

    def __init__(self):
        self.reset()

    def reset(self):
        self.x  = float(PLAYER_X)
        self.y  = float(GROUND_Y - self.H)
        self.vy = 0.0
        self.on_ground = True
        self.jump_count = 0        # allow double-jump
        self.trail = []
        self.shield_time = 0       # invincibility frames after hit

    def jump(self):
        if self.jump_count < 2:
            self.vy = JUMP_VEL
            self.jump_count += 1
            self.on_ground = False
            return True
        return False

    def update(self):
        self.vy += GRAVITY
        self.y  += self.vy
        if self.y >= GROUND_Y - self.H:
            self.y  = GROUND_Y - self.H
            self.vy = 0
            self.on_ground = True
            self.jump_count = 0

        # Trail
        self.trail.append((self.x + self.W//2, self.y + self.H//2))
        if len(self.trail) > 10:
            self.trail.pop(0)

        if self.shield_time > 0:
            self.shield_time -= 1

    def rect(self):
        # slightly smaller hitbox than visual
        return pygame.Rect(self.x+5, self.y+4, self.W-10, self.H-6)

    def draw(self, surf):
        # Trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(80 * i / len(self.trail))
            s = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(s, C_PLAYER+(alpha,), (3,3), 3)
            surf.blit(s, (tx-3, ty-3))

        x, y = int(self.x), int(self.y)
        W, H = self.W, self.H

        # Shield flicker
        if self.shield_time > 0 and (self.shield_time // 4) % 2 == 0:
            return

        # Body (rounded rect + gradient feel)
        body_col = C_PLAYER
        draw_glow_rect(surf, body_col, (x, y, W, H), radius=7, alpha=60)
        draw_rounded(surf, (15, 30, 70), (x, y, W, H), r=7)
        draw_rounded(surf, body_col, (x+2, y+2, W-4, H//2), r=5)  # highlight top

        # Visor
        visor = pygame.Rect(x+6, y+8, W-12, 12)
        pygame.draw.rect(surf, (0, 200, 255), visor, border_radius=3)
        pygame.draw.rect(surf, (150, 240, 255), (x+8, y+10, 6, 4), border_radius=2)

        # Legs animation
        tick = pygame.time.get_ticks()
        leg_offset = int(math.sin(tick * 0.015) * 5) if self.on_ground else 0
        leg_col = (60, 110, 200)
        pygame.draw.rect(surf, leg_col, (x+5,  y+H-12, 10, 12+leg_offset), border_radius=3)
        pygame.draw.rect(surf, leg_col, (x+W-15, y+H-12, 10, 12-leg_offset), border_radius=3)

# ── Data Packet ────────────────────────────────────────────────────────────

class DataPacket:
    SIZE = 22

    def __init__(self, x):
        self.x = float(x)
        self.y = float(GROUND_Y - self.SIZE - random.randint(0, 60))
        self.collected = False
        self.phase = random.uniform(0, math.pi*2)

    def update(self, speed):
        self.x -= speed
        self.phase += 0.07

    def rect(self):
        s = self.SIZE
        return pygame.Rect(self.x - s//2, self.y - s//2, s, s)

    def draw(self, surf):
        bob = math.sin(self.phase) * 5
        cx, cy = int(self.x), int(self.y + bob)
        s = self.SIZE
        # Glow
        draw_glow_rect(surf, C_PACKET, (cx-s//2, cy-s//2, s, s), radius=5, alpha=100)
        # Diamond shape
        pts = [(cx, cy-s//2), (cx+s//2, cy), (cx, cy+s//2), (cx-s//2, cy)]
        pygame.draw.polygon(surf, C_PACKET, pts)
        pygame.draw.polygon(surf, C_WHITE, pts, 2)
        # Inner shine
        pts2 = [(cx, cy-s//4), (cx+s//4, cy), (cx, cy+s//4), (cx-s//4, cy)]
        pygame.draw.polygon(surf, (180, 255, 240), pts2)

# ── Malware Obstacle ───────────────────────────────────────────────────────

class Malware:
    TYPES = [
        {"w": 24, "h": 48, "label": "VIRUS"},
        {"w": 48, "h": 28, "label": "BUG"},
        {"w": 22, "h": 64, "label": "WORM"},
    ]

    def __init__(self, x):
        t = random.choice(self.TYPES)
        self.w = t["w"]
        self.h = t["h"]
        self.label = t["label"]
        self.x = float(x)
        self.y = float(GROUND_Y - self.h)
        self.phase = random.uniform(0, math.pi*2)

    def update(self, speed):
        self.x -= speed
        self.phase += 0.05

    def rect(self):
        return pygame.Rect(self.x+3, self.y+3, self.w-6, self.h-6)

    def draw(self, surf):
        pulse = abs(math.sin(self.phase)) * 0.4 + 0.6
        col = tuple(int(c * pulse) for c in C_MALWARE)
        rx, ry = int(self.x), int(self.y)
        draw_glow_rect(surf, C_MALWARE, (rx, ry, self.w, self.h), radius=5, alpha=90)
        draw_rounded(surf, (60, 10, 20), (rx, ry, self.w, self.h), r=5)
        draw_rounded(surf, col, (rx+2, ry+2, self.w-4, self.h-4), r=4)
        # X mark
        mid_x = rx + self.w//2
        mid_y = ry + self.h//2
        pygame.draw.line(surf, C_WHITE, (mid_x-7, mid_y-7), (mid_x+7, mid_y+7), 2)
        pygame.draw.line(surf, C_WHITE, (mid_x+7, mid_y-7), (mid_x-7, mid_y+7), 2)
        # Label
        font_s = pygame.font.SysFont("consolas", 8, bold=True)
        lbl = font_s.render(self.label, True, (255, 180, 180))
        surf.blit(lbl, (mid_x - lbl.get_width()//2, ry - 13))

# ── Background ─────────────────────────────────────────────────────────────

class Background:
    def __init__(self):
        self.scroll = 0.0
        # Stars
        self.stars = [(random.randint(0, W), random.randint(0, GROUND_Y-60),
                       random.uniform(0.5, 2.5), random.uniform(0.3, 1.0))
                      for _ in range(80)]
        # City silhouette columns
        self.buildings = []
        for bx in range(0, W+80, 40):
            bh = random.randint(40, 140)
            self.buildings.append([float(bx), bh])

    def update(self, speed):
        self.scroll = (self.scroll + speed * 0.3) % W
        for b in self.buildings:
            b[0] -= speed * 0.25
            if b[0] < -40:
                b[0] += W + 80
                b[1] = random.randint(40, 140)

    def draw(self, surf):
        # Sky gradient
        for row in range(GROUND_Y):
            t = row / GROUND_Y
            c = lerp_color(BG_TOP, BG_BOT, t)
            pygame.draw.line(surf, c, (0, row), (W, row))

        # City
        for bx, bh in self.buildings:
            col = (18, 28, 65)
            rect = (int(bx), GROUND_Y - bh, 35, bh)
            pygame.draw.rect(surf, col, rect)
            # Windows
            for wy in range(GROUND_Y - bh + 5, GROUND_Y - 5, 12):
                for wxi in range(int(bx)+4, int(bx)+30, 8):
                    if random.random() < 0.0005:   # rare flicker
                        wc = (200, 220, 255)
                    else:
                        wc = (30, 55, 110) if (int(bx//8 + wy//12)) % 3 != 0 else (60, 100, 180)
                    pygame.draw.rect(surf, wc, (wxi, wy, 5, 7))

        # Grid floor lines
        ox = int(self.scroll) % TILE_W
        for gx in range(-ox, W + TILE_W, TILE_W):
            pygame.draw.line(surf, C_GRID, (gx, GROUND_Y), (gx, H), 1)
        for gy in range(GROUND_Y, H+1, 20):
            alpha = int(180 * (gy - GROUND_Y) / (H - GROUND_Y))
            col = C_GRID + (alpha,)
            s = pygame.Surface((W, 1), pygame.SRCALPHA)
            s.fill(col)
            surf.blit(s, (0, gy))

        # Ground strip
        pygame.draw.rect(surf, C_GROUND, (0, GROUND_Y, W, 4))
        pygame.draw.rect(surf, C_GLOW,   (0, GROUND_Y, W, 2))

        # Stars
        for sx, sy, sz, bright in self.stars:
            col = tuple(int(c * bright) for c in (200, 220, 255))
            r = max(1, int(sz))
            pygame.draw.circle(surf, col, (int(sx), int(sy)), r)

# ── HUD ────────────────────────────────────────────────────────────────────

class HUD:
    def __init__(self):
        self.font_big  = pygame.font.SysFont("consolas", 36, bold=True)
        self.font_med  = pygame.font.SysFont("consolas", 20, bold=True)
        self.font_sm   = pygame.font.SysFont("consolas", 14)
        self.font_tiny = pygame.font.SysFont("consolas", 11)

    def draw(self, surf, score, high_score, lives, level, distance):
        # Top bar background
        bar = pygame.Surface((W, 52), pygame.SRCALPHA)
        bar.fill((5, 10, 30, 180))
        surf.blit(bar, (0, 0))
        pygame.draw.line(surf, C_GLOW, (0, 52), (W, 52), 1)

        # Score
        sc = self.font_big.render(f"{score:06d}", True, C_TEXT)
        surf.blit(sc, (20, 8))
        lb = self.font_tiny.render("SCORE", True, C_DIM)
        surf.blit(lb, (22, 52))

        # High score
        hs = self.font_med.render(f"BEST {high_score:06d}", True, C_DIM)
        surf.blit(hs, (W//2 - hs.get_width()//2, 15))

        # Level
        lv = self.font_med.render(f"LVL {level}", True, C_GOLD)
        surf.blit(lv, (W - 160, 15))

        # Distance
        dist_s = self.font_sm.render(f"{distance}m", True, C_DIM)
        surf.blit(dist_s, (W - dist_s.get_width() - 20, 38))

        # Lives (hearts)
        for i in range(lives):
            hx = W - 20 - i*28
            hy = 14
            self._draw_heart(surf, hx, hy, 10, C_MALWARE)

        # Double-jump hint (shown early)
        if distance < 200:
            hint = self.font_tiny.render("SPACE / ↑ = Jump  (double-jump allowed)", True, C_DIM)
            surf.blit(hint, (W//2 - hint.get_width()//2, H - 22))

    def _draw_heart(self, surf, cx, cy, r, col):
        pygame.draw.circle(surf, col, (cx - r//2, cy), r//2)
        pygame.draw.circle(surf, col, (cx + r//2, cy), r//2)
        pts = [(cx - r, cy), (cx, cy + r + 2), (cx + r, cy)]
        pygame.draw.polygon(surf, col, pts)

# ── Screens ────────────────────────────────────────────────────────────────

def draw_title_screen(surf, fonts, tick):
    surf.fill(BG_TOP)
    # Animated grid
    ox = tick % TILE_W
    for gx in range(-ox, W+TILE_W, TILE_W):
        pygame.draw.line(surf, C_GRID, (gx, 0), (gx, H), 1)
    for gy in range(0, H, TILE_W):
        pygame.draw.line(surf, C_GRID, (0, gy), (W, gy), 1)

    font_title = fonts["title"]
    font_sub   = fonts["sub"]
    font_sm    = fonts["sm"]

    # Pulsing glow behind title
    pulse = abs(math.sin(tick * 0.04))
    glow_s = pygame.Surface((W, 120), pygame.SRCALPHA)
    glow_s.fill((60, 100, 255, int(40 * pulse)))
    surf.blit(glow_s, (0, H//2 - 80))

    title = font_title.render("CYBER RUNNER", True, C_PLAYER)
    surf.blit(title, (W//2 - title.get_width()//2, H//2 - 90))

    sub = font_sub.render("Collect data packets. Dodge malware.", True, C_DIM)
    surf.blit(sub, (W//2 - sub.get_width()//2, H//2 - 20))

    # Blinking prompt
    if (tick // 35) % 2 == 0:
        prompt = font_sm.render("▶  PRESS  SPACE  TO  START  ◀", True, C_GOLD)
        surf.blit(prompt, (W//2 - prompt.get_width()//2, H//2 + 40))

    controls = font_sm.render("SPACE / ↑ = Jump   (double-jump)    ESC = Quit", True, C_DIM)
    surf.blit(controls, (W//2 - controls.get_width()//2, H - 36))

def draw_gameover_screen(surf, fonts, score, high_score, new_best):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((5, 5, 20, 200))
    surf.blit(overlay, (0, 0))

    font_title = fonts["title"]
    font_sub   = fonts["sub"]
    font_sm    = fonts["sm"]

    go = font_title.render("GAME  OVER", True, C_MALWARE)
    surf.blit(go, (W//2 - go.get_width()//2, H//2 - 100))

    sc = font_sub.render(f"Score: {score:06d}", True, C_TEXT)
    surf.blit(sc, (W//2 - sc.get_width()//2, H//2 - 20))

    if new_best:
        nb = font_sub.render("✦  NEW BEST!  ✦", True, C_GOLD)
        surf.blit(nb, (W//2 - nb.get_width()//2, H//2 + 20))
    else:
        hs = font_sm.render(f"Best: {high_score:06d}", True, C_DIM)
        surf.blit(hs, (W//2 - hs.get_width()//2, H//2 + 22))

    restart = font_sm.render("R = Restart     ESC = Quit", True, C_DIM)
    surf.blit(restart, (W//2 - restart.get_width()//2, H//2 + 68))

# ── Main Game ───────────────────────────────────────────────────────────────

def main():
    pygame.init()
    surf = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Cyber Runner  —  OmniMind")
    clock = pygame.time.Clock()

    fonts = {
        "title": pygame.font.SysFont("consolas", 52, bold=True),
        "sub":   pygame.font.SysFont("consolas", 24, bold=True),
        "sm":    pygame.font.SysFont("consolas", 16),
    }

    high_score = 0

    # ── States: TITLE | PLAYING | GAMEOVER ──
    state = "TITLE"
    tick  = 0

    # Game objects (initialised on start)
    bg      = Background()
    player  = Player()
    hud     = HUD()
    packets : list[DataPacket] = []
    malwares: list[Malware]    = []
    particles: list[Particle]  = []

    score    = 0
    lives    = 3
    distance = 0
    level    = 1
    speed    = 5.0
    new_best = False

    spawn_timer   = 0
    packet_timer  = 0
    score_timer   = 0

    def start_game():
        nonlocal bg, player, packets, malwares, particles
        nonlocal score, lives, distance, level, speed, new_best
        nonlocal spawn_timer, packet_timer, score_timer
        bg        = Background()
        player    = Player()
        packets   = []
        malwares  = []
        particles = []
        score     = 0
        lives     = 3
        distance  = 0
        level     = 1
        speed     = 5.0
        new_best  = False
        spawn_timer  = 60
        packet_timer = 30
        score_timer  = 0

    while True:
        dt = clock.tick(FPS)
        tick += 1

        # ── Events ──────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

                if state == "TITLE":
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        start_game()
                        state = "PLAYING"

                elif state == "PLAYING":
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        if player.jump():
                            for _ in range(8):
                                particles.append(Particle(
                                    player.x + player.W//2,
                                    player.y + player.H,
                                    C_PLAYER,
                                    vel=(0, 2)
                                ))

                elif state == "GAMEOVER":
                    if event.key == pygame.K_r:
                        start_game()
                        state = "PLAYING"

        # ── Update ──────────────────────────────────────────────────────
        if state == "TITLE":
            bg.update(2)

        elif state == "PLAYING":
            # Level scaling
            level    = 1 + distance // 300
            speed    = 5.0 + level * 0.6 + score * 0.0003

            bg.update(speed)
            player.update()

            distance += speed / 60   # approximate metres
            distance  = int(distance)

            # Score ticks
            score_timer += 1
            if score_timer >= 6:
                score       += 1
                score_timer  = 0

            # Spawn malware
            spawn_timer -= 1
            if spawn_timer <= 0:
                malwares.append(Malware(W + 20))
                gap = max(45, 90 - level * 4)
                spawn_timer = random.randint(gap, gap + 35)

            # Spawn packets (clusters)
            packet_timer -= 1
            if packet_timer <= 0:
                base_x = W + 20
                count  = random.randint(2, 5)
                for i in range(count):
                    packets.append(DataPacket(base_x + i * 38))
                packet_timer = random.randint(40, 80)

            # Move malware
            for m in malwares:
                m.update(speed)
            malwares = [m for m in malwares if m.x > -80]

            # Move packets
            for p in packets:
                p.update(speed)
            packets = [p for p in packets if p.x > -40 and not p.collected]

            # Particle update
            for pt in particles:
                pt.update()
            particles = [pt for pt in particles if pt.life > 0]

            # Collision: packets
            pr = player.rect()
            for p in packets:
                if not p.collected and pr.colliderect(p.rect()):
                    p.collected = True
                    score += 10
                    for _ in range(12):
                        particles.append(Particle(p.x, p.y, C_PACKET))

            # Collision: malware
            for m in malwares:
                if player.shield_time == 0 and pr.colliderect(m.rect()):
                    lives -= 1
                    player.shield_time = 90   # ~1.5s invincibility
                    for _ in range(20):
                        particles.append(Particle(
                            player.x + player.W//2,
                            player.y + player.H//2,
                            C_MALWARE
                        ))
                    malwares.remove(m)
                    if lives <= 0:
                        if score > high_score:
                            high_score = score
                            new_best   = True
                        state = "GAMEOVER"
                    break

        # ── Draw ────────────────────────────────────────────────────────
        bg.draw(surf)

        if state in ("PLAYING", "GAMEOVER"):
            for p in packets:
                p.draw(surf)
            for m in malwares:
                m.draw(surf)
            for pt in particles:
                pt.draw(surf)
            player.draw(surf)
            hud.draw(surf, score, high_score, lives, level, distance)

        if state == "TITLE":
            draw_title_screen(surf, fonts, tick)

        if state == "GAMEOVER":
            draw_gameover_screen(surf, fonts, score, high_score, new_best)

        pygame.display.flip()

if __name__ == "__main__":
    main()