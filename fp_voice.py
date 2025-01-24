import pygame
import random
from vosk import Model, KaldiRecognizer
import pyaudio
import numpy as np
import threading

audio_volume = 0.0
audio_lock = threading.Lock()
user_name = ""

def update_and_draw_stars():
    for star in stars:
        star['y'] += star['speed']
        if star['y'] > HEIGHT:
            star['y'] = 0
            star['x'] = random.randint(0, WIDTH)
            star['speed'] = random.uniform(1, 3)
        pygame.draw.circle(screen, WHITE, (int(star['x']), int(star['y'])), 2)

def update_and_draw_particles():
    global particles
    for particle in particles:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['lifetime'] -= 1
        if particle['lifetime'] > 0:
            pygame.draw.circle(screen, (255, 215, 0), (int(particle['x']), int(particle['y'])), particle['size'])
    particles = [p for p in particles if p['lifetime'] > 0]

def process_audio():
    global audio_volume
    while True:
        try:
            data = stream.read(4000, exception_on_overflow=False)
            volume = get_volume(data)
            with audio_lock:
                audio_volume = volume
        except Exception as e:
            print(f"Audio Error: {e}")

def select_game_level():
    global obstacle_speed
    recognizer = KaldiRecognizer(model, 16000)
    font = pygame.font.SysFont("comicsans", 40)

    while True:
        screen.fill(background_color)
        level_text = font.render("Say Difficulty Level:", True, WHITE)
        option1 = font.render("1. Easy", True, WHITE)
        option2 = font.render("2. Medium", True, WHITE)
        option3 = font.render("3. Hard", True, WHITE)
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(option3, (WIDTH // 2 - option3.get_width() // 2, HEIGHT // 2 + 80))
        pygame.display.flip()

        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_text = eval(result)['text']
            print(f"Recognized level selection: {result_text}")

            if "easy" in result_text or "one" in result_text:
                obstacle_speed = 1
                return
            elif "medium" in result_text or "two" in result_text:
                obstacle_speed = 1.8
                return
            elif "hard" in result_text or "three" in result_text:
                obstacle_speed = 2.7
                return

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice-Pitch Controlled Flappy Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "speed": random.uniform(1, 3)} for _ in range(50)]
particles = []

character_image = pygame.image.load("santa.png").convert_alpha()
character_image = pygame.transform.scale(character_image, (50, 50))

collectible_image = pygame.image.load("snowflake.png").convert_alpha()
collectible_image = pygame.transform.scale(collectible_image, (40, 40))

background_color = (0, 100, 0)

character_x = 100
character_y = HEIGHT // 2
character_size = 20
gravity = 2
max_jump = 8
min_jump = 1

obstacle_width = 70
obstacle_gap = 300
obstacles = []

collectibles = []
collectible_size = 25
collectible_chance = 0.5

last_adjustment = 0
snowflakes_collected = 0
clock = pygame.time.Clock()
fps = 40

max_obstacle_speed = 5
min_obstacle_gap = 120

model = Model("C:\\Users\\Tara\\Documents\\Faks\\ioi\\vosk-model-small-en-us-0.15")

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Start the audio thread AFTER initializing stream
audio_thread = threading.Thread(target=process_audio, daemon=True)
audio_thread.start()

def get_volume(data):
    try:
        audio_data = np.frombuffer(data, np.int16)
        volume = np.abs(audio_data).mean()
        return volume / 500.0
    except ValueError:
        return 0.0

def create_obstacle():
    min_gap_center = obstacle_gap // 2 + 50
    max_gap_center = HEIGHT - obstacle_gap // 2 - 50
    gap_y = random.randint(min_gap_center, max_gap_center)
    obstacles.append({"x": WIDTH, "y_top": gap_y - obstacle_gap // 2, "y_bottom": gap_y + obstacle_gap // 2})
    if random.random() < collectible_chance:
        create_collectible(gap_y)

def create_collectible(gap_y):
    collectible_y = random.randint(gap_y - obstacle_gap // 2 + collectible_size, gap_y + obstacle_gap // 2 - collectible_size)
    collectibles.append({"x": WIDTH, "y": collectible_y})

for i in range(2):
    obstacle_x = WIDTH - i * (WIDTH // 3) + 100
    gap_y = random.randint(obstacle_gap // 2 + 50, HEIGHT - obstacle_gap // 2 - 50)
    obstacles.append({"x": obstacle_x, "y_top": gap_y - obstacle_gap // 2, "y_bottom": gap_y + obstacle_gap // 2})

distance_between_obstacles = 200

select_game_level()
#recognize_name_and_start()
obstacles_passed = 0
running = True
while running:
    screen.fill(background_color)
    update_and_draw_stars()
    update_and_draw_particles()

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False

    with audio_lock:
        volume = audio_volume

    if volume > 0.25:
        #print("jump " + str(volume))
        jump = max(min_jump, min(int(volume * 3), max_jump))
        character_y -= jump
        for _ in range(5):
            particles.append({
                "x": character_x + character_size // 2,
                "y": character_y + character_size,
                "dx": random.uniform(-2, 2),
                "dy": random.uniform(-2, 2),
                "size": random.randint(2, 4),
                "lifetime": random.randint(20, 40)
            })

    else:
        character_y += gravity

    character_y = max(0, min(character_y, HEIGHT - character_size))

    if len(obstacles) == 0 or obstacles[-1]["x"] < WIDTH - distance_between_obstacles:
        create_obstacle()

    if obstacles_passed % 2 == 0 and obstacles_passed > 0 and obstacles_passed != last_adjustment:
        last_adjustment = obstacles_passed
        if obstacle_speed < max_obstacle_speed:
            obstacle_speed += 0.5
        if obstacle_gap > min_obstacle_gap:
            obstacle_gap -= 20

    for obstacle in obstacles:
        obstacle["x"] -= obstacle_speed
        pygame.draw.rect(screen, RED, (obstacle["x"], 0, obstacle_width, obstacle["y_top"]))
        pygame.draw.rect(screen, RED, (obstacle["x"], obstacle["y_bottom"], obstacle_width, HEIGHT - obstacle["y_bottom"]))

        if (
            character_x + character_size > obstacle["x"]
            and character_x < obstacle["x"] + obstacle_width
            and (character_y < obstacle["y_top"] or character_y + character_size > obstacle["y_bottom"])
        ):
            for _ in range(5):
                screen.fill(RED)
                pygame.display.flip()
                pygame.time.wait(100)
                screen.fill(background_color)
                pygame.display.flip()
                pygame.time.wait(100)
            running = False
        if obstacle["x"] + obstacle_width < character_x and not obstacle.get("passed", False):
            obstacles_passed += 1
            obstacle["passed"] = True

    obstacles = [obstacle for obstacle in obstacles if obstacle["x"] > -obstacle_width]

    for collectible in collectibles:
        collectible["x"] -= obstacle_speed
        screen.blit(collectible_image, (collectible["x"], collectible["y"]))
        if (
            character_x + character_size > collectible["x"]
            and character_x < collectible["x"] + collectible_size
            and character_y + character_size > collectible["y"]
            and character_y < collectible["y"] + collectible_size
        ):
            collectibles.remove(collectible)
            snowflakes_collected += 1

    collectibles = [collectible for collectible in collectibles if collectible["x"] > -collectible_size]

    screen.blit(character_image, (character_x, character_y))

    font = pygame.font.SysFont("comicsans", 30)
    text = font.render(f"Snowflakes Collected: {snowflakes_collected}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

screen.fill(background_color)
font = pygame.font.SysFont("comicsans", 40)

game_over_text_line1 = font.render(f"Game Over!", True, WHITE)
game_over_text_line2 = font.render(f"You collected {snowflakes_collected} snowflakes!", True, WHITE)


line1_x = WIDTH // 2 - game_over_text_line1.get_width() // 2
line1_y = HEIGHT // 2 - 40  
line2_x = WIDTH // 2 - game_over_text_line2.get_width() // 2
line2_y = HEIGHT // 2 + 10  

screen.blit(game_over_text_line1, (line1_x, line1_y))
screen.blit(game_over_text_line2, (line2_x, line2_y))
pygame.display.flip()

pygame.time.wait(3000)
pygame.quit()