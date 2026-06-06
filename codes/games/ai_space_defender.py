"""
╔══════════════════════════════════════════════╗
║       AI SPACE DEFENDER  —  OmniMind         ║
║   Defend the servers. Destroy cyber threats. ║
╚══════════════════════════════════════════════╝
Controls:
  A / ← / D / →   Move left / right
  SPACE            Shoot
  R                Restart (Game Over)
  ESC              Quit
"""

import pygame
import random
import math
import sys

# ── Constants ──────────────────────────────────────────────────────────────
W, H   = 900, 620
FPS    = 60

# Colour palette
BG          = (4,   6,  20)
C_GRID      = (12,  22,  60)
C_GLOW_BLUE = (60, 140, 255)
C_GLOW_CYAN = (0,  220, 200)
C_PLAYER    = (80, 180, 255)
C_BULLET    = (0,  240, 200)
C_ENEMY_A   = (255,  60,  90)   # Raider
C_ENEMY_B   = (255, 150,  30)   # Tank
C_ENEMY_C   = (200,  50, 255)   # Phantom
C_BOMB      = (255,  80,  30)
C_TEXT      = (210, 225, 255)
C_DIM       = (70,  90, 140)
C_GOLD      = (255, 210,  50)
C_GREEN     = (60,  230, 120)
C_WHITE     = (255, 255, 255)
C_SERVER    = (30,  60, 180)

PLAYER_Y    = H - 80
SERVER_Y    = H - 26
PLAYER_SPEED = 6
BULLET_SPEED = 14
BOMB_SPEED   = 4


# ── Helpers ────────────────────────────────────────────────────────────────

def lerp_color(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def draw_glow(surf, color, cx, cy, radius, alpha=60):
    s = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
    pygame.draw.circle(s, color + (alpha,), (radius+2, radius+2), radius)
    surf.blit(s, (cx - radius - 2, cy - radius - 2))

def draw_glow_rect(surf, color, rect, r=6, alpha=70):
    pad = 10
    s = pygame.Surface((rect[2]+pad*2, rect[3]+pad*2), pygame.SRCALPHA)
    pygame.draw.rect(s, color + (alpha,), (pad, pad, rect[2], rect[3]), border_radius=r+3)
    surf.blit(s, (rect[0]-pad, rect[1]-pad))

def draw_rounded(surf, color, rect, r=6):
    pygame.draw.rect(surf, color, rect, border_radius=r)


# ── Particle ───────────────────────────────────────────────────────────────

class Particle:
    def __init__(self, x, y, color, speed_range=(1, 5), gravity=0.08, life=None):
        self.x, self.y  = float(x), float(y)
        self.color      = color
        ang  = random.uniform(0, math.pi * 2)
        spd  = random.uniform(*speed_range)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd
        self.gravity     = gravity
        self.life        = life or random.randint(20, 45)
        self.max_life    = self.life
        self.size        = random.uniform(2, 5)

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += self.gravity
        self.life -= 1

    def draw(self, surf):
        t = self.life / self.max_life
        col = lerp_color((0, 0, 0), self.color, t) + (int(255 * t),)
        r   = max(1, int(self.size * t))
        s   = pygame.Surface((r*2+1, r*2+1), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (r, r), r)
        surf.blit(s, (int(self.x) - r, int(self.y) - r))


def explosion(x, y, color, count=22, **kw):
    return [Particle(x, y, color, **kw) for _ in range(count)]


# ── Stars ──────────────────────────────────────────────────────────────────

class Starfield:
    def __init__(self, n=120):
        self.stars = [
            [random.randint(0, W), random.randint(0, H),
             random.uniform(0.4, 2.5), random.uniform(0.2, 1.0)]
            for _ in range(n)
        ]

    def update(self, speed=0.4):
        for s in self.stars:
            s[1] += speed * (s[2] / 2)
            if s[1] > H:
                s[1] = 0
                s[0] = random.randint(0, W)

    def draw(self, surf):
        for sx, sy, sz, br in self.stars:
            col = tuple(int(c * br) for c in (180, 210, 255))
            r   = max(1, int(sz * 0.7))
            pygame.draw.circle(surf, col, (int(sx), int(sy)), r)


# ── Background grid ────────────────────────────────────────────────────────

class Grid:
    def __init__(self):
        self.offset = 0.0

    def update(self, speed):
        self.offset = (self.offset + speed) % 60

    def draw(self, surf):
        surf.fill(BG)
        o = int(self.offset)
        for x in range(0, W, 60):
            pygame.draw.line(surf, C_GRID, (x, 0), (x, H), 1)
        for y in range(-60 + o, H, 60):
            pygame.draw.line(surf, C_GRID, (0, y), (W, y), 1)


# ── Server bar ─────────────────────────────────────────────────────────────

class ServerBar:
    def __init__(self):
        self.hp    = 100
        self.max   = 100
        self.flash = 0

    def damage(self, amt):
        self.hp    = max(0, self.hp - amt)
        self.flash = 18

    def draw(self, surf, font):
        # Strip
        pygame.draw.rect(surf, (10, 20, 55), (0, SERVER_Y, W, H - SERVER_Y))
        pygame.draw.line(surf, C_GLOW_BLUE, (0, SERVER_Y), (W, SERVER_Y), 2)

        # Server blocks
        for i in range(9):
            bx = 30 + i * 96
            col = (20, 45, 120) if self.flash == 0 else (80, 20, 30)
            draw_rounded(surf, col, (bx, SERVER_Y + 5, 80, 16), r=4)
            pygame.draw.rect(surf, C_GLOW_BLUE, (bx, SERVER_Y + 5, 80, 16), 1, border_radius=4)
            # LED
            led = C_GREEN if self.hp > 30 else C_BOMB
            pygame.draw.circle(surf, led, (bx + 70, SERVER_Y + 13), 3)

        # HP bar
        bar_w   = 280
        bar_x   = W // 2 - bar_w // 2
        bar_y   = SERVER_Y + 6
        ratio   = self.hp / self.max
        bar_col = lerp_color(C_BOMB, C_GREEN, ratio)
        pygame.draw.rect(surf, (20, 30, 70), (bar_x, bar_y, bar_w, 14), border_radius=7)
        if ratio > 0:
            pygame.draw.rect(surf, bar_col, (bar_x, bar_y, int(bar_w * ratio), 14), border_radius=7)
        pygame.draw.rect(surf, C_DIM, (bar_x, bar_y, bar_w, 14), 1, border_radius=7)

        lbl = font.render(f"SERVER  {self.hp}%", True, C_TEXT)
        surf.blit(lbl, (W // 2 - lbl.get_width() // 2, bar_y + 16))

        if self.flash > 0:
            self.flash -= 1


# ── Player ship ────────────────────────────────────────────────────────────

class Player:
    W, H_SZ = 46, 36

    def __init__(self):
        self.x         = float(W // 2)
        self.y         = float(PLAYER_Y)
        self.speed     = PLAYER_SPEED
        self.shoot_cd  = 0
        self.shield    = 0      # invincibility
        self.thruster  = 0.0
        self.trail     = []

    def update(self, keys):
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        self.x = max(self.W//2, min(W - self.W//2, self.x))

        if self.shoot_cd > 0:
            self.shoot_cd -= 1
        if self.shield > 0:
            self.shield -= 1

        self.thruster  = (self.thruster + 0.2) % (math.pi * 2)
        self.trail.append((self.x, self.y + self.H_SZ // 2))
        if len(self.trail) > 8:
            self.trail.pop(0)

    def try_shoot(self):
        if self.shoot_cd == 0:
            self.shoot_cd = 14
            return [Bullet(self.x - 12, self.y - 8),
                    Bullet(self.x + 12, self.y - 8)]
        return []

    def rect(self):
        return pygame.Rect(self.x - 18, self.y - 14, 36, 28)

    def draw(self, surf):
        # Trail
        for i, (tx, ty) in enumerate(self.trail):
            a = int(60 * i / len(self.trail))
            s = pygame.Surface((5, 5), pygame.SRCALPHA)
            pygame.draw.circle(s, C_PLAYER + (a,), (2, 2), 2)
            surf.blit(s, (int(tx) - 2, int(ty) - 2))

        if self.shield > 0 and (self.shield // 5) % 2 == 0:
            return

        cx, cy = int(self.x), int(self.y)

        # Thruster flame
        flame_h = int(10 + math.sin(self.thruster) * 5)
        flame_pts = [
            (cx - 8,  cy + 16),
            (cx,      cy + 16 + flame_h),
            (cx + 8,  cy + 16),
        ]
        flame_col = lerp_color((255, 80, 0), (255, 220, 60), abs(math.sin(self.thruster)))
        pygame.draw.polygon(surf, flame_col, flame_pts)

        # Hull glow
        draw_glow_rect(surf, C_PLAYER, (cx - 22, cy - 18, 44, 36), r=8, alpha=50)

        # Main body
        body_pts = [
            (cx,      cy - 18),   # nose
            (cx + 22, cy + 16),   # right base
            (cx,      cy + 8),    # centre dip
            (cx - 22, cy + 16),   # left base
        ]
        pygame.draw.polygon(surf, (20, 50, 120), body_pts)
        pygame.draw.polygon(surf, C_PLAYER, body_pts, 2)

        # Wing highlights
        pygame.draw.line(surf, (150, 200, 255), (cx, cy - 14), (cx + 18, cy + 12), 2)
        pygame.draw.line(surf, (150, 200, 255), (cx, cy - 14), (cx - 18, cy + 12), 2)

        # Cockpit
        pygame.draw.circle(surf, (0, 200, 255), (cx, cy - 4), 7)
        pygame.draw.circle(surf, (180, 240, 255), (cx - 2, cy - 6), 3)

        # Cannons
        for sx in (-12, 12):
            pygame.draw.rect(surf, C_GLOW_CYAN, (cx + sx - 2, cy + 6, 4, 14), border_radius=2)


# ── Bullet ─────────────────────────────────────────────────────────────────

class Bullet:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.alive     = True

    def update(self):
        self.y -= BULLET_SPEED
        if self.y < -10:
            self.alive = False

    def rect(self):
        return pygame.Rect(self.x - 2, self.y - 8, 4, 16)

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        draw_glow(surf, C_BULLET, cx, cy, 8, alpha=60)
        pygame.draw.rect(surf, C_BULLET, (cx - 2, cy - 9, 4, 18), border_radius=2)
        pygame.draw.rect(surf, C_WHITE,  (cx - 1, cy - 9, 2, 6),  border_radius=1)


# ── Enemies ────────────────────────────────────────────────────────────────

class Enemy:
    """Base class."""
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.alive     = True
        self.phase     = random.uniform(0, math.pi * 2)
        self.bomb_cd   = random.randint(80, 200)
        self.score_val = 10
        self.hp        = 1
        self.color     = C_ENEMY_A

    def update(self, tick):
        self.phase  += 0.04
        self.bomb_cd -= 1

    def try_drop_bomb(self):
        if self.bomb_cd <= 0:
            self.bomb_cd = random.randint(140, 300)
            return Bomb(self.x, self.y + 16)
        return None

    def take_hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def rect(self):
        return pygame.Rect(self.x - 20, self.y - 16, 40, 32)

    def draw(self, surf):
        pass


class Raider(Enemy):
    """Fast, zigzag attacker."""
    def __init__(self, x, y, dx):
        super().__init__(x, y)
        self.dx        = dx
        self.dy        = 1.0
        self.hp        = 1
        self.color     = C_ENEMY_A
        self.score_val = 10

    def update(self, tick):
        super().update(tick)
        self.x += self.dx + math.sin(self.phase * 1.5) * 1.5
        self.y += self.dy
        if self.x < 20 or self.x > W - 20:
            self.dx *= -1

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        pulse  = abs(math.sin(self.phase)) * 0.4 + 0.6
        col    = tuple(int(c * pulse) for c in self.color)
        draw_glow_rect(surf, col, (cx-18, cy-14, 36, 28), r=5, alpha=70)
        pts = [(cx, cy+14), (cx-18, cy-12), (cx, cy-4), (cx+18, cy-12)]
        pygame.draw.polygon(surf, (50, 10, 20), pts)
        pygame.draw.polygon(surf, col, pts, 2)
        pygame.draw.circle(surf, col, (cx, cy - 2), 6)
        pygame.draw.circle(surf, (255, 180, 180), (cx, cy - 4), 2)


class Tank(Enemy):
    """Slow, absorbs 3 hits, drops more bombs."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dx        = random.choice([-0.8, 0.8])
        self.dy        = 0.35
        self.hp        = 3
        self.color     = C_ENEMY_B
        self.score_val = 30
        self.bomb_cd   = random.randint(60, 120)

    def update(self, tick):
        super().update(tick)
        self.x += self.dx + math.sin(self.phase) * 0.6
        self.y += self.dy
        if self.x < 32 or self.x > W - 32:
            self.dx *= -1

    def rect(self):
        return pygame.Rect(self.x - 28, self.y - 20, 56, 40)

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        t      = self.hp / 3
        col    = lerp_color(C_ENEMY_A, self.color, t)
        draw_glow_rect(surf, col, (cx-28, cy-20, 56, 40), r=7, alpha=80)
        draw_rounded(surf, (40, 20, 5), (cx-28, cy-20, 56, 40), r=7)
        draw_rounded(surf, col, (cx-24, cy-16, 48, 32), r=5)
        # HP pips
        for i in range(self.hp):
            pygame.draw.circle(surf, C_WHITE, (cx - 8 + i*8, cy), 4)


class Phantom(Enemy):
    """Stealthy: fades in/out."""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dx        = random.uniform(-1.5, 1.5)
        self.dy        = 0.6
        self.hp        = 2
        self.color     = C_ENEMY_C
        self.score_val = 20
        self.alpha_dir = 1
        self.vis       = 0.3

    def update(self, tick):
        super().update(tick)
        self.x   += self.dx
        self.y   += self.dy
        self.vis  = 0.35 + 0.65 * abs(math.sin(self.phase * 0.6))
        if self.x < 24 or self.x > W - 24:
            self.dx *= -1

    def draw(self, surf):
        cx, cy  = int(self.x), int(self.y)
        alpha   = int(220 * self.vis)
        col     = self.color + (alpha,)
        s       = pygame.Surface((52, 44), pygame.SRCALPHA)
        pts     = [(26, 0), (52, 38), (26, 28), (0, 38)]
        pygame.draw.polygon(s, (80, 10, 120, alpha), pts)
        pygame.draw.polygon(s, col, pts, 2)
        pygame.draw.circle(s, col, (26, 22), 8)
        pygame.draw.circle(s, (220, 180, 255, alpha), (23, 19), 3)
        surf.blit(s, (cx - 26, cy - 22))


# ── Enemy bomb ─────────────────────────────────────────────────────────────

class Bomb:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.alive     = True
        self.phase     = 0.0

    def update(self):
        self.y    += BOMB_SPEED
        self.phase += 0.1
        if self.y > SERVER_Y:
            self.alive = False

    def rect(self):
        return pygame.Rect(self.x - 6, self.y - 6, 12, 12)

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        pulse  = abs(math.sin(self.phase)) * 0.5 + 0.5
        col    = lerp_color((200, 40, 0), (255, 160, 30), pulse)
        draw_glow(surf, col, cx, cy, 12, alpha=70)
        pygame.draw.circle(surf, col, (cx, cy), 6)
        pygame.draw.circle(surf, C_WHITE, (cx - 2, cy - 2), 2)


# ── Wave builder ───────────────────────────────────────────────────────────

def build_wave(wave: int):
    enemies = []
    cols    = min(8 + wave, 14)
    rows    = min(2 + wave // 2, 5)
    spacing_x = max(52, (W - 80) // cols)
    spacing_y = 56

    for row in range(rows):
        for col in range(cols):
            x = 50 + col * spacing_x
            y = 70 + row * spacing_y
            r = random.random()
            if wave <= 1:
                enemies.append(Raider(x, y, random.choice([-0.8, 0.8])))
            elif r < 0.55:
                enemies.append(Raider(x, y, random.choice([-1.0, 1.0])))
            elif r < 0.80:
                enemies.append(Phantom(x, y))
            else:
                enemies.append(Tank(x, y))
    return enemies


# ── HUD ────────────────────────────────────────────────────────────────────

class HUD:
    def __init__(self):
        self.f_big  = pygame.font.SysFont("consolas", 34, bold=True)
        self.f_med  = pygame.font.SysFont("consolas", 18, bold=True)
        self.f_sm   = pygame.font.SysFont("consolas", 13)

    def draw(self, surf, score, high_score, lives, wave, wave_msg, wave_msg_timer):
        # Top bar
        bar = pygame.Surface((W, 50), pygame.SRCALPHA)
        bar.fill((4, 8, 28, 190))
        surf.blit(bar, (0, 0))
        pygame.draw.line(surf, C_GLOW_BLUE, (0, 50), (W, 50), 1)

        sc = self.f_big.render(f"{score:07d}", True, C_TEXT)
        surf.blit(sc, (18, 7))

        hs = self.f_med.render(f"BEST {high_score:07d}", True, C_DIM)
        surf.blit(hs, (W // 2 - hs.get_width() // 2, 14))

        wv = self.f_med.render(f"WAVE {wave}", True, C_GOLD)
        surf.blit(wv, (W - wv.get_width() - 100, 14))

        # Lives
        for i in range(lives):
            self._heart(surf, W - 22 - i * 24, 22, 9)

        # Wave announcement
        if wave_msg_timer > 0:
            alpha = min(255, wave_msg_timer * 8)
            s     = pygame.Surface((W, 50), pygame.SRCALPHA)
            txt   = self.f_big.render(wave_msg, True, C_GOLD + (alpha,))
            s.blit(txt, (W // 2 - txt.get_width() // 2, 10))
            surf.blit(s, (0, H // 2 - 40))

        # Controls hint
        if wave == 1:
            h = self.f_sm.render("A/D or ←/→ Move   SPACE Shoot", True, C_DIM)
            surf.blit(h, (W // 2 - h.get_width() // 2, H - 50))

    def _heart(self, surf, cx, cy, r):
        pygame.draw.circle(surf, C_BOMB, (cx - r//2, cy), r//2)
        pygame.draw.circle(surf, C_BOMB, (cx + r//2, cy), r//2)
        pygame.draw.polygon(surf, C_BOMB, [(cx-r, cy), (cx, cy+r+2), (cx+r, cy)])


# ── Screens ────────────────────────────────────────────────────────────────

def draw_title(surf, tick):
    surf.fill(BG)
    o = int(tick * 0.8) % 60
    for x in range(0, W, 60):
        pygame.draw.line(surf, C_GRID, (x, 0), (x, H), 1)
    for y in range(-60 + o, H, 60):
        pygame.draw.line(surf, C_GRID, (0, y), (W, y), 1)

    f_title = pygame.font.SysFont("consolas", 56, bold=True)
    f_sub   = pygame.font.SysFont("consolas", 22, bold=True)
    f_sm    = pygame.font.SysFont("consolas", 15)

    pulse = abs(math.sin(tick * 0.04))
    glow  = pygame.Surface((W, 130), pygame.SRCALPHA)
    glow.fill((40, 80, 255, int(35 * pulse)))
    surf.blit(glow, (0, H//2 - 90))

    t1 = f_title.render("AI SPACE DEFENDER", True, C_PLAYER)
    surf.blit(t1, (W//2 - t1.get_width()//2, H//2 - 100))

    t2 = f_sub.render("Defend OmniMind servers from cyber attacks.", True, C_DIM)
    surf.blit(t2, (W//2 - t2.get_width()//2, H//2 - 22))

    if (tick // 32) % 2 == 0:
        t3 = f_sm.render("▶   PRESS  SPACE  TO  LAUNCH   ◀", True, C_GOLD)
        surf.blit(t3, (W//2 - t3.get_width()//2, H//2 + 36))

    t4 = f_sm.render("A/D or ←/→ Move    SPACE Shoot    ESC Quit", True, C_DIM)
    surf.blit(t4, (W//2 - t4.get_width()//2, H - 34))


def draw_gameover(surf, score, high_score, new_best):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((4, 6, 20, 210))
    surf.blit(overlay, (0, 0))

    f_big = pygame.font.SysFont("consolas", 52, bold=True)
    f_med = pygame.font.SysFont("consolas", 24, bold=True)
    f_sm  = pygame.font.SysFont("consolas", 16)

    go = f_big.render("GAME  OVER", True, C_ENEMY_A)
    surf.blit(go, (W//2 - go.get_width()//2, H//2 - 110))

    sc = f_med.render(f"Score:  {score:07d}", True, C_TEXT)
    surf.blit(sc, (W//2 - sc.get_width()//2, H//2 - 20))

    if new_best:
        nb = f_med.render("✦  NEW  BEST  ✦", True, C_GOLD)
        surf.blit(nb, (W//2 - nb.get_width()//2, H//2 + 26))
    else:
        hs = f_sm.render(f"Best:  {high_score:07d}", True, C_DIM)
        surf.blit(hs, (W//2 - hs.get_width()//2, H//2 + 28))

    rs = f_sm.render("R = Restart       ESC = Quit", True, C_DIM)
    surf.blit(rs, (W//2 - rs.get_width()//2, H//2 + 74))


def draw_victory(surf, wave):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((4, 6, 20, 200))
    surf.blit(overlay, (0, 0))

    f_big = pygame.font.SysFont("consolas", 48, bold=True)
    f_sm  = pygame.font.SysFont("consolas", 18)

    vt = f_big.render(f"WAVE {wave} CLEARED!", True, C_GREEN)
    surf.blit(vt, (W//2 - vt.get_width()//2, H//2 - 40))

    ns = f_sm.render("SPACE = Next Wave", True, C_GOLD)
    surf.blit(ns, (W//2 - ns.get_width()//2, H//2 + 30))


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    surf  = pygame.display.set_mode((W, H))
    pygame.display.set_caption("AI Space Defender  —  OmniMind")
    clock = pygame.time.Clock()

    hud        = HUD()
    high_score = 0

    def new_game():
        return dict(
            player     = Player(),
            server     = ServerBar(),
            stars      = Starfield(),
            grid       = Grid(),
            bullets    = [],
            enemies    = [],
            bombs      = [],
            particles  = [],
            score      = 0,
            lives      = 3,
            wave       = 0,
            new_best   = False,
            wave_msg   = "",
            wave_msg_t = 0,
            between    = False,   # waiting for SPACE between waves
        )

    def next_wave(g):
        g["wave"]    += 1
        g["enemies"]  = build_wave(g["wave"])
        g["bombs"]    = []
        g["wave_msg"] = f"WAVE  {g['wave']}"
        g["wave_msg_t"] = 90
        g["between"]  = False

    state = "TITLE"
    tick  = 0
    g     = new_game()

    while True:
        clock.tick(FPS)
        tick += 1
        keys = pygame.key.get_pressed()

        # ── Events ──────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

                if state == "TITLE":
                    if event.key == pygame.K_SPACE:
                        g     = new_game()
                        next_wave(g)
                        state = "PLAYING"

                elif state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        if g["between"]:
                            next_wave(g)
                        else:
                            new_bullets = g["player"].try_shoot()
                            g["bullets"].extend(new_bullets)

                elif state == "GAMEOVER":
                    if event.key == pygame.K_r:
                        g     = new_game()
                        next_wave(g)
                        state = "PLAYING"

        # ── Update ──────────────────────────────────────────────────────
        if state == "PLAYING":
            p      = g["player"]
            server = g["server"]

            if not g["between"]:
                p.update(keys)

                # Hold SPACE = rapid fire
                if keys[pygame.K_SPACE]:
                    new_bullets = p.try_shoot()
                    g["bullets"].extend(new_bullets)

                # Bullets
                for b in g["bullets"]:
                    b.update()
                g["bullets"] = [b for b in g["bullets"] if b.alive]

                # Enemies
                for e in g["enemies"]:
                    e.update(tick)
                    bomb = e.try_drop_bomb()
                    if bomb:
                        g["bombs"].append(bomb)

                # Bullets vs Enemies
                for b in g["bullets"]:
                    if not b.alive:
                        continue
                    for e in g["enemies"]:
                        if e.alive and b.rect().colliderect(e.rect()):
                            b.alive = False
                            killed  = e.take_hit()
                            if killed:
                                g["score"] += e.score_val
                                g["particles"] += explosion(e.x, e.y, e.color, count=24)
                            else:
                                g["particles"] += explosion(e.x, e.y, e.color, count=6, speed_range=(1,3))
                            break

                g["enemies"] = [e for e in g["enemies"] if e.alive]

                # Bombs
                for bm in g["bombs"]:
                    bm.update()

                # Bomb hits server
                hits = [bm for bm in g["bombs"] if not bm.alive]
                for bm in hits:
                    server.damage(8)
                    g["particles"] += explosion(bm.x, SERVER_Y, C_BOMB, count=16)
                g["bombs"] = [bm for bm in g["bombs"] if bm.alive]

                # Bomb vs player
                for bm in list(g["bombs"]):
                    if p.shield == 0 and bm.rect().colliderect(p.rect()):
                        bm.alive  = False
                        g["lives"] -= 1
                        p.shield   = 90
                        g["particles"] += explosion(p.x, p.y, C_PLAYER, count=20)

                # Enemy reaches bottom
                for e in list(g["enemies"]):
                    if e.y > SERVER_Y:
                        e.alive = False
                        server.damage(20)
                        g["particles"] += explosion(e.x, SERVER_Y, e.color, count=18)

                g["enemies"] = [e for e in g["enemies"] if e.alive]

                # Particles
                for pt in g["particles"]:
                    pt.update()
                g["particles"] = [pt for pt in g["particles"] if pt.life > 0]

                if g["wave_msg_t"] > 0:
                    g["wave_msg_t"] -= 1

                # Check deaths
                if g["lives"] <= 0 or server.hp <= 0:
                    if g["score"] > high_score:
                        high_score   = g["score"]
                        g["new_best"] = True
                    state = "GAMEOVER"

                # Wave cleared
                if len(g["enemies"]) == 0 and not g["between"]:
                    g["between"] = True

            g["stars"].update()
            g["grid"].update(1.5)

        # ── Draw ────────────────────────────────────────────────────────
        if state == "TITLE":
            draw_title(surf, tick)
        else:
            g["grid"].draw(surf)
            g["stars"].draw(surf)

            for pt in g["particles"]:
                pt.draw(surf)
            for b in g["bullets"]:
                b.draw(surf)
            for e in g["enemies"]:
                e.draw(surf)
            for bm in g["bombs"]:
                bm.draw(surf)

            if state == "PLAYING":
                g["player"].draw(surf)

            g["server"].draw(surf, pygame.font.SysFont("consolas", 12))
            hud.draw(surf, g["score"], high_score, g["lives"],
                     g["wave"], g["wave_msg"], g["wave_msg_t"])

            if g.get("between"):
                draw_victory(surf, g["wave"])

            if state == "GAMEOVER":
                draw_gameover(surf, g["score"], high_score, g["new_best"])

        pygame.display.flip()


if __name__ == "__main__":
    main()