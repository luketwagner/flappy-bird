import random
import sys

import pygame


# Window and gameplay constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60
GROUND_HEIGHT = 80

GRAVITY = 0.4
JUMP_VELOCITY = -8.5

PIPE_WIDTH = 70
PIPE_GAP = 170
PIPE_SPEED = 3
PIPE_SPAWN_MS = 1400

BACKGROUND_COLOR = (135, 206, 235)
GROUND_COLOR = (222, 184, 135)
BIRD_COLOR = (255, 215, 0)
PIPE_COLOR = (34, 139, 34)
TEXT_COLOR = (30, 30, 30)


class Bird:
    def __init__(self, x: int, y: int, radius: int = 16) -> None:
        self.x = x
        self.y = float(y)
        self.radius = radius
        self.velocity_y = 0.0

    def jump(self) -> None:
        # Instant upward impulse on player input
        self.velocity_y = JUMP_VELOCITY

    def update(self) -> None:
        # Gravity affects velocity every frame
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

    def draw(self, screen: pygame.Surface) -> None:
        center_x = int(self.x)
        center_y = int(self.y)

        # Body
        pygame.draw.circle(screen, BIRD_COLOR, (center_x, center_y), self.radius)

        # Eye
        eye_x = center_x + self.radius // 3
        eye_y = center_y - self.radius // 3
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 4)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x + 1, eye_y), 2)

        # Beak
        beak_points = [
            (center_x + self.radius, center_y - 2),
            (center_x + self.radius + 12, center_y + 2),
            (center_x + self.radius, center_y + 6),
        ]
        pygame.draw.polygon(screen, (255, 140, 0), beak_points)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )


class Pipe:
    def __init__(self, x: int) -> None:
        self.x = float(x)
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        self.passed = False

        min_center = 120
        max_center = WINDOW_HEIGHT - GROUND_HEIGHT - 120
        self.gap_center = random.randint(min_center, max_center)

    @property
    def top_height(self) -> int:
        return int(self.gap_center - self.gap // 2)

    @property
    def bottom_y(self) -> int:
        return int(self.gap_center + self.gap // 2)

    def update(self) -> None:
        self.x -= PIPE_SPEED

    def draw(self, screen: pygame.Surface) -> None:
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(
            int(self.x),
            self.bottom_y,
            self.width,
            WINDOW_HEIGHT - GROUND_HEIGHT - self.bottom_y,
        )
        pygame.draw.rect(screen, PIPE_COLOR, top_rect)
        pygame.draw.rect(screen, PIPE_COLOR, bottom_rect)

    def is_offscreen(self) -> bool:
        return self.x + self.width < 0

    def collides_with(self, bird_rect: pygame.Rect) -> bool:
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(
            int(self.x),
            self.bottom_y,
            self.width,
            WINDOW_HEIGHT - GROUND_HEIGHT - self.bottom_y,
        )
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)


class Game:
    START = "start"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Flappy Bird Clone")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 48)

        self.state = self.START
        self.spawn_timer = 0
        self.reset_game()

    def reset_game(self) -> None:
        self.bird = Bird(110, WINDOW_HEIGHT // 2)
        self.pipes: list[Pipe] = []
        self.score = 0
        self.spawn_timer = 0

    def spawn_pipe(self) -> None:
        self.pipes.append(Pipe(WINDOW_WIDTH))

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.state == self.START:
                    self.state = self.PLAYING
                    self.bird.jump()
                elif self.state == self.PLAYING:
                    self.bird.jump()
                elif self.state == self.GAME_OVER:
                    self.reset_game()
                    self.state = self.PLAYING
                    self.bird.jump()
        return True

    def update_playing(self, dt_ms: int) -> None:
        self.bird.update()

        self.spawn_timer += dt_ms
        if self.spawn_timer >= PIPE_SPAWN_MS:
            self.spawn_timer = 0
            self.spawn_pipe()

        bird_rect = self.bird.get_rect()

        for pipe in self.pipes:
            pipe.update()

            # Score once when bird passes a pipe's right edge
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1

            if pipe.collides_with(bird_rect):
                self.state = self.GAME_OVER

        self.pipes = [pipe for pipe in self.pipes if not pipe.is_offscreen()]

        ground_top = WINDOW_HEIGHT - GROUND_HEIGHT
        if self.bird.y + self.bird.radius >= ground_top:
            self.state = self.GAME_OVER
        if self.bird.y - self.bird.radius <= 0:
            self.state = self.GAME_OVER

    def draw_background(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(
            self.screen,
            GROUND_COLOR,
            pygame.Rect(0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT),
        )

    def draw_score(self) -> None:
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (12, 12))

    def draw_start_screen(self) -> None:
        title = self.big_font.render("Flappy Bird", True, TEXT_COLOR)
        prompt = self.font.render("Press SPACE to start", True, TEXT_COLOR)
        self.screen.blit(
            title,
            (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 2 - 80),
        )
        self.screen.blit(
            prompt,
            (WINDOW_WIDTH // 2 - prompt.get_width() // 2, WINDOW_HEIGHT // 2 - 30),
        )

    def draw_game_over_screen(self) -> None:
        game_over = self.big_font.render("Game Over", True, TEXT_COLOR)
        final_score = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
        prompt = self.font.render("Press SPACE to restart", True, TEXT_COLOR)
        self.screen.blit(
            game_over,
            (WINDOW_WIDTH // 2 - game_over.get_width() // 2, WINDOW_HEIGHT // 2 - 90),
        )
        self.screen.blit(
            final_score,
            (WINDOW_WIDTH // 2 - final_score.get_width() // 2, WINDOW_HEIGHT // 2 - 40),
        )
        self.screen.blit(
            prompt,
            (WINDOW_WIDTH // 2 - prompt.get_width() // 2, WINDOW_HEIGHT // 2 + 5),
        )

    def draw(self) -> None:
        self.draw_background()
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.bird.draw(self.screen)
        self.draw_score()

        if self.state == self.START:
            self.draw_start_screen()
        elif self.state == self.GAME_OVER:
            self.draw_game_over_screen()

        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt_ms = self.clock.tick(FPS)
            running = self.handle_events()

            if self.state == self.PLAYING:
                self.update_playing(dt_ms)

            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
