import math
import random
import time
import pygame 
pygame.init()

# Set the dimensions for the game window
WIDTH, HEIGHT = 800, 600 

# Create the game window with specified dimensions
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")  # Set the title of the game window

TARGET_EVENT = pygame.USEREVENT  # Custom event for target generation

TARGET_PADDING = 30  # Padding to prevent targets from spawning too close to the edges

BG_COLOUR = (0, 25, 40)  # Background color of the game window (dark blue)
Lives = 3  # Number of lives the player has
TOP_BAR_HEIGHT = 50  # Height of the top bar where information will be displayed

LABEL_FONT = pygame.font.SysFont("comicsans", 24)  # Font used for displaying text on the top bar

class Target:
    MAX_SIZE = 30  # Maximum size of the target
    GROWTH_RATE = 0.2  # Rate at which the target grows or shrinks
    COLOUR = "red"  # Primary color of the target
    SECOND_COLOUR = "white"  # Secondary color of the target

    def __init__(self, x, y):
        # Initialize target position and size
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True  # Flag to determine whether the target is growing or shrinking

    def update(self):
        # Update the size of the target
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False  # Start shrinking when the max size is reached

        if self.grow:
            self.size += self.GROWTH_RATE  # Grow the target
        else:
            self.size -= self.GROWTH_RATE  # Shrink the target

    def draw(self, win):
        # Draw the target with multiple concentric circles
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOUR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOUR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        # Check if the target has been clicked (collision detection)
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size  # Return True if click is within the target radius

def draw(win, targets):
    # Fill the background with the specified color
    win.fill(BG_COLOUR)

    # Draw each target on the screen
    for target in targets:
        target.draw(win)

def format_time(secs):
    # Format the elapsed time as minutes:seconds:milliseconds
    milli = math.floor(int(secs*1000 % 1000)/ 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}:{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    # Draw the top bar with game information
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAR_HEIGHT))

    # Create labels for time, speed, hits, and lives
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1 , "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1 , "white")
    lives_label = LABEL_FONT.render(f"Lives: {Lives - misses}", 1 , "white")

    # Display labels on the top bar
    win.blit(time_label, (5,5))
    win.blit(speed_label, (200,5))
    win.blit(hits_label, (450,5))
    win.blit(lives_label, (650,5))

def end_screen(win, elapsed_time, targets_pressed, clicks):
    # Display the end screen with game summary
    win.fill(BG_COLOUR)

    # Create labels for time, speed, hits, and accuracy
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1 , "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1 , "white")
    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1 , "white")

    # Display the labels on the end screen, centered
    win.blit(time_label, (get_middle(time_label),100))
    win.blit(speed_label, (get_middle(speed_label),200))
    win.blit(hits_label, (get_middle(hits_label),300))
    win.blit(accuracy_label, (get_middle(accuracy_label),400))

    pygame.display.update()  # Update the display to show the end screen

    run = True

    while run:
        # Wait for the player to close the game window or press a key
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()  # Exit the game

def get_middle(surface):
    # Calculate the horizontal center position for a given surface
    return WIDTH / 2 - surface.get_width()/2

def is_overlapping(x, y, targets):
    # Check if the new target at (x, y) overlaps with any existing targets
    for target in targets:
        distance = math.sqrt((target.x - x)**2 + (target.y - y)**2)
        if distance < target.size + Target.MAX_SIZE + TARGET_PADDING:
            return True
    return False

def choose_difficulty():
    # Display the difficulty selection screen
    run = True
    while run:
        WIN.fill(BG_COLOUR)
        easy_label = LABEL_FONT.render("Press E for Easy", 1, "white")
        medium_label = LABEL_FONT.render("Press M for Medium", 1, "white")
        hard_label = LABEL_FONT.render("Press H for Hard", 1, "white")

        WIN.blit(easy_label, (get_middle(easy_label), 200))
        WIN.blit(medium_label, (get_middle(medium_label), 300))
        WIN.blit(hard_label, (get_middle(hard_label), 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 900  # Easy difficulty: targets appear every 1000 ms
                elif event.key == pygame.K_m:
                    return 600  # Medium difficulty: targets appear every 600 ms
                elif event.key == pygame.K_h:
                    return 300  # Hard difficulty: targets appear every 400 ms

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0

    TARGET_INCREMENT = choose_difficulty()  # Set the target increment based on chosen difficulty
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
    start_time = time.time()  # Start the timer only after difficulty is selected

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                # Generate a new target at a random position, ensuring it doesn't overlap
                while True:
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    if not is_overlapping(x, y, targets):
                        break
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= Lives:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
