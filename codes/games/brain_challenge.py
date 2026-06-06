"""
╔══════════════════════════════════════════════╗
║       BRAIN CHALLENGE  —  OmniMind           ║
║  Quizzes · Logic · Coding · Math Puzzles     ║
╚══════════════════════════════════════════════╝
Controls:
  MOUSE CLICK   Select answer
  1 / 2 / 3 / 4  Keyboard shortcuts
  ESC           Quit
"""

import pygame
import random
import math
import sys
import textwrap

# ── Window ─────────────────────────────────────────────────────────────────
W, H = 960, 640
FPS  = 60

# ── Palette ────────────────────────────────────────────────────────────────
BG          = (6,   8,  22)
C_GRID      = (14,  24,  60)
C_PANEL     = (12,  18,  48)
C_PANEL2    = (18,  28,  70)
C_BORDER    = (30,  55, 140)
C_GLOW      = (80, 130, 255)
C_TEXT      = (215, 228, 255)
C_DIM       = (75,  95, 145)
C_GOLD      = (255, 210,  50)
C_GREEN     = (50,  220, 130)
C_RED       = (255,  65,  80)
C_CYAN      = (0,   220, 210)
C_PURPLE    = (170,  80, 255)
C_ORANGE    = (255, 150,  40)
C_WHITE     = (255, 255, 255)

# Category colours
CAT_COLORS = {
    "Quiz":   C_CYAN,
    "Logic":  C_PURPLE,
    "Coding": C_ORANGE,
    "Math":   C_GOLD,
}

# Answer button accent colours
BTN_COLS = [
    (80,  140, 255),   # A
    (170,  80, 255),   # B
    (0,   200, 180),   # C
    (255, 160,  40),   # D
]

# ── Question bank ──────────────────────────────────────────────────────────
QUESTIONS = [
    # ── Quiz ──
    {
        "cat": "Quiz", "diff": 1,
        "q": "What does CPU stand for?",
        "opts": ["Central Processing Unit", "Core Power Utility",
                 "Computer Personal Unit", "Central Program Uplink"],
        "ans": 0,
    },
    {
        "cat": "Quiz", "diff": 1,
        "q": "Which language runs natively in web browsers?",
        "opts": ["Python", "Java", "JavaScript", "Ruby"],
        "ans": 2,
    },
    {
        "cat": "Quiz", "diff": 1,
        "q": "What does HTML stand for?",
        "opts": ["HyperText Markup Language", "HighTech Modern Link",
                 "HyperTransfer Machine Language", "HyperText Media Link"],
        "ans": 0,
    },
    {
        "cat": "Quiz", "diff": 2,
        "q": "Which protocol secures web traffic with encryption?",
        "opts": ["FTP", "HTTPS", "SMTP", "UDP"],
        "ans": 1,
    },
    {
        "cat": "Quiz", "diff": 2,
        "q": "What is the base of the binary number system?",
        "opts": ["8", "10", "2", "16"],
        "ans": 2,
    },
    {
        "cat": "Quiz", "diff": 2,
        "q": "Which data structure operates on LIFO principle?",
        "opts": ["Queue", "Linked List", "Tree", "Stack"],
        "ans": 3,
    },
    {
        "cat": "Quiz", "diff": 3,
        "q": "What is the time complexity of binary search?",
        "opts": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
        "ans": 2,
    },
    {
        "cat": "Quiz", "diff": 3,
        "q": "Which sorting algorithm has worst-case O(n log n)?",
        "opts": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"],
        "ans": 2,
    },
    # ── Logic ──
    {
        "cat": "Logic", "diff": 1,
        "q": "If all Bloops are Razzles and all Razzles are Lazzles,\nare all Bloops definitely Lazzles?",
        "opts": ["Yes", "No", "Sometimes", "Cannot determine"],
        "ans": 0,
    },
    {
        "cat": "Logic", "diff": 1,
        "q": "A bat and ball cost $1.10 total.\nThe bat costs $1 more than the ball.\nHow much does the ball cost?",
        "opts": ["$0.10", "$0.05", "$0.15", "$0.20"],
        "ans": 1,
    },
    {
        "cat": "Logic", "diff": 2,
        "q": "You have 12 balls, one is heavier.\nMinimum weighings on a balance scale to find it?",
        "opts": ["2", "3", "4", "6"],
        "ans": 1,
    },
    {
        "cat": "Logic", "diff": 2,
        "q": "Which number continues the sequence?\n2, 6, 12, 20, 30, ?",
        "opts": ["40", "42", "44", "48"],
        "ans": 1,
    },
    {
        "cat": "Logic", "diff": 2,
        "q": "A clock shows 3:15. What is the angle\nbetween the hour and minute hands?",
        "opts": ["0°", "7.5°", "15°", "22.5°"],
        "ans": 1,
    },
    {
        "cat": "Logic", "diff": 3,
        "q": "Three boxes: one has gold, one silver, one empty.\nLabels are ALL wrong. Box A: 'Gold', Box B: 'Empty'.\nYou open Box B and it is Silver. Where is Gold?",
        "opts": ["Box A", "Box B", "Box C", "Cannot tell"],
        "ans": 2,
    },
    {
        "cat": "Logic", "diff": 3,
        "q": "Which next in sequence?\nO, T, T, F, F, S, S, E, ?",
        "opts": ["N", "T", "O", "S"],
        "ans": 0,
    },
    # ── Coding ──
    {
        "cat": "Coding", "diff": 1,
        "q": "What does this Python print?\n\nprint(type(3.14))",
        "opts": ["<class 'int'>", "<class 'float'>",
                 "<class 'str'>", "<class 'number'>"],
        "ans": 1,
    },
    {
        "cat": "Coding", "diff": 1,
        "q": "What is the output?\n\nx = [1, 2, 3]\nprint(x[-1])",
        "opts": ["1", "3", "-1", "Error"],
        "ans": 1,
    },
    {
        "cat": "Coding", "diff": 2,
        "q": "What does this return?\n\ndef f(n):\n    return n if n<=1 else f(n-1)+f(n-2)\nf(5)",
        "opts": ["3", "5", "8", "13"],
        "ans": 2,
    },
    {
        "cat": "Coding", "diff": 2,
        "q": "What is the output?\n\nx = {'a':1,'b':2}\nprint(list(x.keys()))",
        "opts": ["['a','b']", "['1','2']",
                 "dict_keys(['a','b'])", "['a':1,'b':2]"],
        "ans": 0,
    },
    {
        "cat": "Coding", "diff": 2,
        "q": "What does this print?\n\nprint([x**2 for x in range(4)])",
        "opts": ["[1,4,9,16]", "[0,1,4,9]",
                 "[0,2,4,6]", "[1,2,3,4]"],
        "ans": 1,
    },
    {
        "cat": "Coding", "diff": 3,
        "q": "Big-O of this algorithm?\n\nfor i in range(n):\n  for j in range(i, n):\n    print(i, j)",
        "opts": ["O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"],
        "ans": 2,
    },
    {
        "cat": "Coding", "diff": 3,
        "q": "What is printed?\n\na = [1,2,3]\nb = a\nb.append(4)\nprint(len(a))",
        "opts": ["3", "4", "Error", "None"],
        "ans": 1,
    },
    # ── Math ──
    {
        "cat": "Math", "diff": 1,
        "q": "What is 2⁸?",
        "opts": ["128", "256", "512", "64"],
        "ans": 1,
    },
    {
        "cat": "Math", "diff": 1,
        "q": "What is the sum of interior angles\nof a hexagon?",
        "opts": ["540°", "720°", "900°", "360°"],
        "ans": 1,
    },
    {
        "cat": "Math", "diff": 2,
        "q": "If log₂(x) = 5, what is x?",
        "opts": ["10", "25", "32", "64"],
        "ans": 2,
    },
    {
        "cat": "Math", "diff": 2,
        "q": "A train travels 120 km in 1.5 hours.\nWhat is its speed in m/s?",
        "opts": ["20 m/s", "22.2 m/s", "25 m/s", "80 m/s"],
        "ans": 1,
    },
    {
        "cat": "Math", "diff": 2,
        "q": "What is the derivative of x³ + 2x?",
        "opts": ["3x + 2", "3x² + 2", "x² + 2", "3x² + 2x"],
        "ans": 1,
    },
    {
        "cat": "Math", "diff": 3,
        "q": "How many ways to arrange 4 items\nout of 7 distinct items? (Permutation)",
        "opts": ["35", "210", "840", "5040"],
        "ans": 2,
    },
    {
        "cat": "Math", "diff": 3,
        "q": "What is the value of i² + i³ + i⁴?\n(where i = √-1)",
        "opts": ["-1+i", "1-i", "-i", "0"],
        "ans": 3,
    },
]

# ── Helpers ────────────────────────────────────────────────────────────────

def lerp_color(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def draw_rounded(surf, color, rect, r=8, border=None, border_w=2):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if border:
        pygame.draw.rect(surf, border, rect, border_w, border_radius=r)

def draw_glow_rect(surf, color, rect, r=8, alpha=60, pad=12):
    s = pygame.Surface((rect[2]+pad*2, rect[3]+pad*2), pygame.SRCALPHA)
    pygame.draw.rect(s, color+(alpha,), (pad, pad, rect[2], rect[3]), border_radius=r+3)
    surf.blit(s, (rect[0]-pad, rect[1]-pad))

def draw_text_wrapped(surf, text, font, color, rect, line_spacing=6):
    """Draw text wrapped inside rect, returns final y."""
    lines = text.split('\n')
    y = rect[1]
    for raw_line in lines:
        # wrap long lines
        words = raw_line.split(' ')
        cur = ""
        wrapped = []
        for w in words:
            test = cur + (" " if cur else "") + w
            if font.size(test)[0] <= rect[2]:
                cur = test
            else:
                if cur:
                    wrapped.append(cur)
                cur = w
        if cur:
            wrapped.append(cur)
        if not wrapped:
            wrapped = [""]
        for line in wrapped:
            s = font.render(line, True, color)
            surf.blit(s, (rect[0] + rect[2]//2 - s.get_width()//2, y))
            y += font.get_height() + line_spacing
    return y

# ── Particle ───────────────────────────────────────────────────────────────

class Particle:
    def __init__(self, x, y, color, up=True):
        self.x, self.y = float(x), float(y)
        self.color = color
        ang = random.uniform(-math.pi, 0) if up else random.uniform(0, math.pi*2)
        spd = random.uniform(2, 7)
        self.vx = math.cos(ang)*spd
        self.vy = math.sin(ang)*spd
        self.life = random.randint(25, 55)
        self.max_life = self.life
        self.size = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.12
        self.life -= 1

    def draw(self, surf):
        t = self.life / self.max_life
        col = lerp_color((0,0,0), self.color, t) + (int(220*t),)
        r = max(1, int(self.size * t))
        s = pygame.Surface((r*2+1, r*2+1), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (r,r), r)
        surf.blit(s, (int(self.x)-r, int(self.y)-r))

# ── Background ─────────────────────────────────────────────────────────────

class Background:
    def __init__(self):
        self.offset = 0.0
        self.neurons = [(random.randint(0,W), random.randint(0,H),
                         random.uniform(0,math.pi*2), random.uniform(0.003, 0.008))
                        for _ in range(18)]
        self.connections = []
        for i in range(len(self.neurons)):
            for j in range(i+1, len(self.neurons)):
                if random.random() < 0.25:
                    self.connections.append((i,j))

    def update(self):
        self.offset += 0.4
        self.neurons = [(x, y, ph + sp, sp)
                        for x,y,ph,sp in self.neurons]

    def draw(self, surf):
        surf.fill(BG)
        # Grid
        o = int(self.offset) % 60
        for x in range(0, W, 60):
            pygame.draw.line(surf, C_GRID, (x, 0), (x, H), 1)
        for y in range(-60+o, H, 60):
            pygame.draw.line(surf, C_GRID, (0, y), (W, y), 1)

        # Neural net decoration
        positions = [(int(x + math.sin(ph)*18), int(y + math.cos(ph)*12))
                     for x,y,ph,_ in self.neurons]
        for i, j in self.connections:
            ax,ay = positions[i]
            bx,by = positions[j]
            dist = math.hypot(bx-ax, by-ay)
            if dist < 260:
                alpha = int(25 * (1 - dist/260))
                s = pygame.Surface((W, H), pygame.SRCALPHA)
                pygame.draw.line(s, C_GLOW+(alpha,), (ax,ay), (bx,by), 1)
                surf.blit(s, (0,0))
        for nx, ny in positions:
            pygame.draw.circle(surf, C_PANEL2, (nx,ny), 4)
            pygame.draw.circle(surf, C_GLOW,   (nx,ny), 4, 1)

# ── Timer bar ──────────────────────────────────────────────────────────────

class TimerBar:
    def __init__(self, total):
        self.total   = total
        self.elapsed = 0.0
        self.done    = False

    def reset(self, total):
        self.total   = total
        self.elapsed = 0.0
        self.done    = False

    def update(self, dt):
        if not self.done:
            self.elapsed += dt
            if self.elapsed >= self.total:
                self.elapsed = self.total
                self.done    = True

    @property
    def ratio(self):
        return max(0.0, 1.0 - self.elapsed / self.total)

    def draw(self, surf, x, y, w, h=10):
        draw_rounded(surf, C_PANEL2, (x, y, w, h), r=5)
        r = self.ratio
        col = lerp_color(C_RED, C_GREEN, r)
        if r > 0:
            draw_rounded(surf, col, (x, y, int(w*r), h), r=5)
        # Glow on edge
        if r > 0.02:
            ex = x + int(w*r)
            pygame.draw.rect(surf, col, (ex-3, y, 3, h), border_radius=2)
        pygame.draw.rect(surf, C_BORDER, (x, y, w, h), 1, border_radius=5)
        return self.done

# ── Answer button ──────────────────────────────────────────────────────────

class AnswerButton:
    LABELS = ['A', 'B', 'C', 'D']
    H = 62

    def __init__(self, index, text, x, y, w):
        self.index  = index
        self.text   = text
        self.rect_r = pygame.Rect(x, y, w, self.H)
        self.color  = BTN_COLS[index]
        self.state  = "idle"   # idle | hover | correct | wrong | locked
        self.anim   = 0.0      # 0..1 for feedback flash
        self.font   = pygame.font.SysFont("consolas", 16, bold=True)
        self.lbl_f  = pygame.font.SysFont("consolas", 20, bold=True)

    def update(self, mx, my, locked):
        if self.state not in ("correct", "wrong", "locked"):
            if self.rect_r.collidepoint(mx, my) and not locked:
                self.state = "hover"
            else:
                self.state = "idle"
        if self.anim > 0:
            self.anim = max(0.0, self.anim - 0.04)

    def trigger(self, result):
        self.state = result
        self.anim  = 1.0

    def draw(self, surf):
        r  = self.rect_r
        st = self.state

        if st == "correct":
            bg  = lerp_color(C_PANEL, C_GREEN, 0.35)
            brd = C_GREEN
        elif st == "wrong":
            bg  = lerp_color(C_PANEL, C_RED, 0.35)
            brd = C_RED
        elif st == "locked":
            bg  = C_PANEL
            brd = C_BORDER
        elif st == "hover":
            bg  = lerp_color(C_PANEL, self.color, 0.25)
            brd = self.color
        else:
            bg  = C_PANEL
            brd = C_BORDER

        # Glow on hover/feedback
        if st == "hover":
            draw_glow_rect(surf, self.color, r, r=8, alpha=40)
        if self.anim > 0 and st in ("correct","wrong"):
            col = C_GREEN if st=="correct" else C_RED
            draw_glow_rect(surf, col, r, r=8, alpha=int(80*self.anim))

        draw_rounded(surf, bg, r, r=8, border=brd, border_w=2)

        # Letter badge
        badge_rect = pygame.Rect(r.x+10, r.y+r.h//2-16, 32, 32)
        badge_col  = self.color if st in ("idle","hover") else (brd if st=="correct" else C_RED if st=="wrong" else C_DIM)
        draw_rounded(surf, lerp_color(bg, badge_col, 0.3), badge_rect, r=6, border=badge_col)
        lbl = self.lbl_f.render(self.LABELS[self.index], True, badge_col)
        surf.blit(lbl, (badge_rect.x + badge_rect.w//2 - lbl.get_width()//2,
                        badge_rect.y + badge_rect.h//2 - lbl.get_height()//2))

        # Answer text (wrapped)
        text_x = r.x + 54
        text_w  = r.w - 64
        text_col = C_TEXT if st != "locked" else C_DIM
        lines = self.text.split('\n')
        # simple single line for answers
        ty = r.y + r.h//2 - self.font.get_height()//2
        for line in lines:
            s = self.font.render(line, True, text_col)
            surf.blit(s, (text_x, ty))
            ty += self.font.get_height() + 2

        # Tick / cross icon
        if st == "correct":
            pygame.draw.line(surf, C_GREEN, (r.right-36, r.centery),
                             (r.right-26, r.centery+9), 3)
            pygame.draw.line(surf, C_GREEN, (r.right-26, r.centery+9),
                             (r.right-12, r.centery-10), 3)
        elif st == "wrong":
            pygame.draw.line(surf, C_RED, (r.right-36, r.centery-10),
                             (r.right-12, r.centery+10), 3)
            pygame.draw.line(surf, C_RED, (r.right-12, r.centery-10),
                             (r.right-36, r.centery+10), 3)


# ── Score popup ────────────────────────────────────────────────────────────

class ScorePopup:
    def __init__(self, x, y, text, color):
        self.x, self.y = float(x), float(y)
        self.text  = text
        self.color = color
        self.life  = 60
        self.font  = pygame.font.SysFont("consolas", 28, bold=True)

    def update(self):
        self.y    -= 1.2
        self.life -= 1

    def draw(self, surf):
        t     = self.life / 60
        alpha = int(255 * t)
        s     = self.font.render(self.text, True, self.color + (alpha,))
        surf2 = pygame.Surface(s.get_size(), pygame.SRCALPHA)
        surf2.blit(s, (0,0))
        surf.blit(surf2, (int(self.x) - s.get_width()//2, int(self.y)))


# ── HUD ────────────────────────────────────────────────────────────────────

class HUD:
    def __init__(self):
        self.f_big  = pygame.font.SysFont("consolas", 30, bold=True)
        self.f_med  = pygame.font.SysFont("consolas", 17, bold=True)
        self.f_sm   = pygame.font.SysFont("consolas", 13)

    def draw(self, surf, score, high_score, lives, streak, q_num, total_q, cat_col, cat_name):
        # Top bar
        bar = pygame.Surface((W, 54), pygame.SRCALPHA)
        bar.fill((6, 9, 28, 200))
        surf.blit(bar, (0, 0))
        pygame.draw.line(surf, C_GLOW, (0, 54), (W, 54), 1)

        sc = self.f_big.render(f"{score:06d}", True, C_TEXT)
        surf.blit(sc, (18, 10))

        hs = self.f_sm.render(f"BEST {high_score:06d}", True, C_DIM)
        surf.blit(hs, (18, 42))

        # Category badge
        badge_w = 130
        draw_rounded(surf, lerp_color(BG, cat_col, 0.15),
                     (W//2 - badge_w//2, 8, badge_w, 30), r=15,
                     border=cat_col, border_w=1)
        cat_t = self.f_sm.render(cat_name, True, cat_col)
        surf.blit(cat_t, (W//2 - cat_t.get_width()//2, 18))

        # Q progress
        prog = self.f_sm.render(f"Q {q_num} / {total_q}", True, C_DIM)
        surf.blit(prog, (W//2 - prog.get_width()//2, 40))

        # Streak
        if streak > 1:
            st_col = C_GOLD if streak < 5 else C_CYAN
            st = self.f_med.render(f"🔥 x{streak} STREAK", True, st_col)
            surf.blit(st, (W - st.get_width() - 18, 10))

        # Lives (stars)
        for i in range(5):
            col = C_GOLD if i < lives else C_PANEL2
            self._star(surf, W - 18 - (4-i)*26, 42, 8, col)

    def _star(self, surf, cx, cy, r, color):
        pts = []
        for i in range(10):
            angle = math.pi/2 + i * math.pi/5
            radius = r if i%2==0 else r*0.45
            pts.append((cx + math.cos(angle)*radius,
                        cy - math.sin(angle)*radius))
        pygame.draw.polygon(surf, color, pts)


# ── Screens ────────────────────────────────────────────────────────────────

def draw_title(surf, tick):
    f_huge = pygame.font.SysFont("consolas", 58, bold=True)
    f_sub  = pygame.font.SysFont("consolas", 20, bold=True)
    f_sm   = pygame.font.SysFont("consolas", 15)

    pulse = abs(math.sin(tick * 0.04))
    glow  = pygame.Surface((W, 140), pygame.SRCALPHA)
    glow.fill((60, 80, 255, int(30*pulse)))
    surf.blit(glow, (0, H//2 - 100))

    t1 = f_huge.render("BRAIN CHALLENGE", True, C_CYAN)
    surf.blit(t1, (W//2 - t1.get_width()//2, H//2 - 110))

    t2 = f_sub.render("Quizzes  ·  Logic  ·  Coding  ·  Math", True, C_DIM)
    surf.blit(t2, (W//2 - t2.get_width()//2, H//2 - 25))

    # Category icons
    cats = [("Quiz", C_CYAN), ("Logic", C_PURPLE), ("Coding", C_ORANGE), ("Math", C_GOLD)]
    total_w = len(cats)*140
    start_x = W//2 - total_w//2
    for i, (cat, col) in enumerate(cats):
        bx = start_x + i*140
        draw_rounded(surf, lerp_color(BG, col, 0.12),
                     (bx, H//2+20, 128, 42), r=10, border=col)
        ct = f_sm.render(cat, True, col)
        surf.blit(ct, (bx+64-ct.get_width()//2, H//2+33))

    if (tick//32)%2==0:
        pr = f_sm.render("▶   PRESS  SPACE  TO  START   ◀", True, C_GOLD)
        surf.blit(pr, (W//2 - pr.get_width()//2, H//2 + 90))

    hint = f_sm.render("Click answer or press  1  2  3  4      ESC = Quit", True, C_DIM)
    surf.blit(hint, (W//2 - hint.get_width()//2, H - 32))


def draw_result_screen(surf, score, high_score, correct, total, new_best):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((4, 6, 22, 215))
    surf.blit(overlay, (0, 0))

    f_big = pygame.font.SysFont("consolas", 50, bold=True)
    f_med = pygame.font.SysFont("consolas", 24, bold=True)
    f_sm  = pygame.font.SysFont("consolas", 16)

    pct = correct / total
    if pct >= 0.8:
        grade, col = "GENIUS! 🧠", C_GOLD
    elif pct >= 0.6:
        grade, col = "SMART!", C_GREEN
    elif pct >= 0.4:
        grade, col = "KEEP PRACTICING", C_CYAN
    else:
        grade, col = "NEEDS WORK", C_RED

    t1 = f_big.render(grade, True, col)
    surf.blit(t1, (W//2 - t1.get_width()//2, H//2 - 120))

    t2 = f_med.render(f"{correct} / {total} correct", True, C_TEXT)
    surf.blit(t2, (W//2 - t2.get_width()//2, H//2 - 40))

    t3 = f_med.render(f"Score:  {score:06d}", True, C_TEXT)
    surf.blit(t3, (W//2 - t3.get_width()//2, H//2 + 10))

    if new_best:
        nb = f_med.render("✦  NEW  BEST  ✦", True, C_GOLD)
        surf.blit(nb, (W//2 - nb.get_width()//2, H//2 + 55))
    else:
        hs = f_sm.render(f"Best: {high_score:06d}", True, C_DIM)
        surf.blit(hs, (W//2 - hs.get_width()//2, H//2 + 58))

    rs = f_sm.render("SPACE = Play Again       ESC = Quit", True, C_DIM)
    surf.blit(rs, (W//2 - rs.get_width()//2, H//2 + 105))


# ── Game state ─────────────────────────────────────────────────────────────

TOTAL_QUESTIONS = 15
TIME_PER_Q      = {1: 15, 2: 20, 3: 28}   # seconds by difficulty


def pick_questions():
    pool = QUESTIONS[:]
    random.shuffle(pool)
    # Ensure variety: 4 quiz, 4 logic, 4 coding, 3 math (or best effort)
    selected = []
    by_cat = {}
    for q in pool:
        by_cat.setdefault(q["cat"], []).append(q)
    targets = {"Quiz":4, "Logic":4, "Coding":4, "Math":3}
    for cat, cnt in targets.items():
        selected.extend(by_cat.get(cat, [])[:cnt])
    random.shuffle(selected)
    return selected[:TOTAL_QUESTIONS]


def new_game():
    qs = pick_questions()
    return {
        "questions":  qs,
        "q_index":    0,
        "score":      0,
        "lives":      5,
        "streak":     0,
        "correct":    0,
        "particles":  [],
        "popups":     [],
        "buttons":    [],
        "timer":      None,
        "locked":     False,
        "feedback_t": 0,
        "next_delay": 0,
    }


def load_question(g):
    q     = g["questions"][g["q_index"]]
    opts  = q["opts"][:]
    # shuffle options but track correct
    paired = list(enumerate(opts))
    random.shuffle(paired)
    correct_shuffled = next(i for i,(orig_i,_) in enumerate(paired) if orig_i == q["ans"])

    margin = 40
    bw     = (W - margin*2 - 10) // 2
    bh     = AnswerButton.H

    button_positions = [
        (margin,          310),
        (margin + bw+10,  310),
        (margin,          310 + bh + 12),
        (margin + bw+10,  310 + bh + 12),
    ]

    g["buttons"] = [
        AnswerButton(i, text, bx, by, bw)
        for i, ((orig_i, text), (bx, by)) in enumerate(zip(paired, button_positions))
    ]
    g["correct_btn"] = correct_shuffled
    g["locked"]      = False
    g["feedback_t"]  = 0
    g["next_delay"]  = 0
    g["timer"]       = TimerBar(TIME_PER_Q[q["diff"]])


def answer_selected(g, btn_index, high_score):
    if g["locked"]:
        return high_score
    g["locked"] = True
    correct = g["correct_btn"]

    if btn_index == correct:
        # Correct
        g["buttons"][btn_index].trigger("correct")
        g["streak"] += 1
        q    = g["questions"][g["q_index"]]
        diff = q["diff"]
        time_bonus = int(g["timer"].ratio * 50)
        streak_bonus = min(g["streak"]-1, 4) * 10
        pts  = diff * 100 + time_bonus + streak_bonus
        g["score"]   += pts
        g["correct"] += 1
        bx = g["buttons"][btn_index].rect_r.centerx
        by = g["buttons"][btn_index].rect_r.centery
        g["popups"].append(ScorePopup(bx, by-20, f"+{pts}", C_GREEN))
        for _ in range(20):
            g["particles"].append(Particle(bx, by, C_GREEN))
        if g["streak"] >= 3:
            g["popups"].append(ScorePopup(W//2, 200, f"🔥 x{g['streak']} STREAK!", C_GOLD))
    else:
        # Wrong
        g["buttons"][btn_index].trigger("wrong")
        g["buttons"][correct].trigger("correct")   # reveal answer
        g["lives"]  = max(0, g["lives"] - 1)
        g["streak"] = 0
        bx = g["buttons"][btn_index].rect_r.centerx
        by = g["buttons"][btn_index].rect_r.centery
        g["popups"].append(ScorePopup(bx, by-20, "WRONG", C_RED))
        for _ in range(12):
            g["particles"].append(Particle(bx, by, C_RED))

    # Lock others
    for i, b in enumerate(g["buttons"]):
        if b.state == "idle":
            b.state = "locked"

    g["feedback_t"] = 90
    return max(high_score, g["score"])


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    surf  = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Brain Challenge  —  OmniMind")
    clock = pygame.time.Clock()

    f_q   = pygame.font.SysFont("consolas", 19, bold=True)
    f_diff= pygame.font.SysFont("consolas", 13)
    f_cat = pygame.font.SysFont("consolas", 13)

    bg         = Background()
    high_score = 0
    state      = "TITLE"
    tick       = 0
    g          = new_game()

    while True:
        dt = clock.tick(FPS) / 1000.0
        tick += 1
        mx, my = pygame.mouse.get_pos()

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
                        load_question(g)
                        state = "PLAYING"

                elif state == "PLAYING":
                    key_map = {pygame.K_1:0, pygame.K_2:1,
                               pygame.K_3:2, pygame.K_4:3}
                    if event.key in key_map and not g["locked"]:
                        high_score = answer_selected(g, key_map[event.key], high_score)

                elif state == "RESULT":
                    if event.key == pygame.K_SPACE:
                        g     = new_game()
                        load_question(g)
                        state = "PLAYING"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "TITLE":
                    g     = new_game()
                    load_question(g)
                    state = "PLAYING"
                elif state == "PLAYING" and not g["locked"]:
                    for i, b in enumerate(g["buttons"]):
                        if b.rect_r.collidepoint(mx, my):
                            high_score = answer_selected(g, i, high_score)
                elif state == "RESULT":
                    g     = new_game()
                    load_question(g)
                    state = "PLAYING"

        # ── Update ──────────────────────────────────────────────────────
        bg.update()

        if state == "PLAYING":
            q = g["questions"][g["q_index"]]

            # Timer
            if not g["locked"]:
                timed_out = g["timer"].update(dt)
                if timed_out:
                    # Time's up → treat as wrong
                    g["locked"] = True
                    g["lives"]  = max(0, g["lives"] - 1)
                    g["streak"] = 0
                    correct = g["correct_btn"]
                    g["buttons"][correct].trigger("correct")
                    for b in g["buttons"]:
                        if b.state == "idle":
                            b.state = "locked"
                    g["popups"].append(ScorePopup(W//2, 240, "TIME'S UP!", C_RED))
                    g["feedback_t"] = 90

            # Buttons hover
            for b in g["buttons"]:
                b.update(mx, my, g["locked"])

            # Feedback countdown → advance
            if g["locked"]:
                g["feedback_t"] -= 1
                if g["feedback_t"] <= 0:
                    g["q_index"] += 1
                    if g["q_index"] >= len(g["questions"]) or g["lives"] <= 0:
                        new_best = g["score"] > high_score
                        if new_best:
                            high_score = g["score"]
                        g["new_best"] = new_best
                        state = "RESULT"
                    else:
                        load_question(g)

            # Particles & popups
            for p in g["particles"]:
                p.update()
            g["particles"] = [p for p in g["particles"] if p.life > 0]
            for p in g["popups"]:
                p.update()
            g["popups"] = [p for p in g["popups"] if p.life > 0]

        # ── Draw ────────────────────────────────────────────────────────
        bg.draw(surf)

        if state == "TITLE":
            draw_title(surf, tick)

        elif state == "PLAYING":
            q      = g["questions"][g["q_index"]]
            cat_c  = CAT_COLORS[q["cat"]]
            diff_s = "★" * q["diff"] + "☆" * (3 - q["diff"])

            # ── Question card ──
            card_rect = pygame.Rect(30, 62, W-60, 230)
            draw_glow_rect(surf, cat_c, card_rect, r=12, alpha=30)
            draw_rounded(surf, C_PANEL, card_rect, r=12, border=cat_c, border_w=2)

            # Category + difficulty row
            cat_lbl = f_cat.render(f"  {q['cat'].upper()}  ", True, cat_c)
            draw_rounded(surf, lerp_color(BG, cat_c, 0.15),
                         (card_rect.x+14, card_rect.y+12,
                          cat_lbl.get_width()+4, cat_lbl.get_height()+4),
                         r=8, border=cat_c)
            surf.blit(cat_lbl, (card_rect.x+16, card_rect.y+14))

            diff_lbl = f_diff.render(diff_s, True, C_GOLD)
            surf.blit(diff_lbl, (card_rect.right - diff_lbl.get_width() - 16, card_rect.y+14))

            # Question text
            draw_text_wrapped(surf, q["q"], f_q, C_TEXT,
                              (card_rect.x+20, card_rect.y+44, card_rect.w-40, 170),
                              line_spacing=4)

            # Timer bar
            g["timer"].draw(surf, card_rect.x, card_rect.bottom - 16, card_rect.w, 8)

            # Buttons
            for b in g["buttons"]:
                b.draw(surf)

            # Particles & popups
            for p in g["particles"]:
                p.draw(surf)
            for p in g["popups"]:
                p.draw(surf)

            # HUD
            hud_obj = HUD()
            hud_obj.draw(surf, g["score"], high_score, g["lives"],
                         g["streak"], g["q_index"]+1,
                         len(g["questions"]), cat_c, q["cat"])

        elif state == "RESULT":
            draw_result_screen(surf, g["score"], high_score,
                               g["correct"], len(g["questions"]),
                               g.get("new_best", False))
            for p in g["particles"]:
                p.update(); p.draw(surf)
            g["particles"] = [p for p in g["particles"] if p.life > 0]

        pygame.display.flip()


if __name__ == "__main__":
    main()