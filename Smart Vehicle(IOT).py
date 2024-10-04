import pygame
import time
import numpy as np
import picamera
import picamera.array
import grovepi
import threading  # Import threading

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set the display to full-screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Truck Project - Raspberry Pi")

# Font for messages
font = pygame.font.SysFont(None, 30)

# Camera setup (using Pi Camera)
camera = picamera.PiCamera()
camera.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
camera.framerate = 30
camera.rotation = 90  # Adjust the rotation based on your setup

# Buzzer setup (Grove Pi)
BUZZER_PORT = 5
grovepi.pinMode(BUZZER_PORT, "OUTPUT")

# Constants for screen layout
CAMERA_VIEW_HEIGHT = int(SCREEN_HEIGHT * 0.75)  # 75% for the camera view
MESSAGE_AREA_Y = CAMERA_VIEW_HEIGHT  # 25% for messages
TEXT_MARGIN = 10

# Helper function to play the buzzer for 5 seconds
def play_buzzer_for_5_seconds():
    grovepi.digitalWrite(BUZZER_PORT, 1)
    time.sleep(5)
    grovepi.digitalWrite(BUZZER_PORT, 0)

# Function to display a blinking message
def display_blinking_message(message, start_time, duration, y_position, blink_count=3):
    current_time = time.time()
    if (current_time - start_time) < (blink_count * 0.5):  # Blink for a total of blink_count times
        if (current_time % 1) < 0.5:  # Blink every half second
            text = font.render(message, True, RED)
            screen.blit(text, (TEXT_MARGIN, y_position))

# Main variables
clock = pygame.time.Clock()
running = True
alert_message = ""
turning_message_start_time = None

# Sample data for vehicle information
speed = 60  # in km/h
size = (100, 50)  # in units
weight = 1200  # in kg

# Show a black screen for a moment before starting the camera feed
screen.fill(BLACK)
pygame.display.flip()
time.sleep(1)  # Wait for 1 second

# Main loop
while running:
    screen.fill(WHITE)

    # Capture camera frame using picamera
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, 'rgb')
        frame = stream.array
        frame = np.rot90(frame)  # Rotate the frame for correct display orientation
        frame = pygame.surfarray.make_surface(frame)

        # Blit the camera frame within the top 75% of the screen
        camera_surf = pygame.transform.scale(frame, (SCREEN_WIDTH, CAMERA_VIEW_HEIGHT))
        screen.blit(camera_surf, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                running = False
            elif event.key == pygame.K_s:  # Driver sleeping alert
                alert_message = "Driver is sleeping! Be alert!"
                turning_message_start_time = time.time()
                # Start buzzer in a new thread
                threading.Thread(target=play_buzzer_for_5_seconds).start()
            elif event.key == pygame.K_1:  # Overtaking alert
                alert_message = "It's time to overtake!"
                turning_message_start_time = time.time()
            elif event.key == pygame.K_o:  # Object detected alert
                alert_message = "Object detected!"
                turning_message_start_time = time.time()
            elif event.key == pygame.K_e:  # Engine fault warning
                alert_message = "Warning: Engine going to fault!"
                turning_message_start_time = time.time()
            elif event.key == pygame.K_LEFT:  # Turning left
                alert_message = "Turning left!"
                turning_message_start_time = time.time()
            elif event.key == pygame.K_RIGHT:  # Turning right
                alert_message = "Turning right!"
                turning_message_start_time = time.time()
            elif event.key == pygame.K_SPACE:  # Slow
                alert_message = "Ready to Slow!"
                turning_message_start_time = time.time()

    # If an alert message is set and we are blinking, clear other messages
    if turning_message_start_time:
        # Blink the alert message three times
        display_blinking_message(alert_message, turning_message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)
        # Resetting the alert message after three blinks
        if time.time() - turning_message_start_time >= 1.5:  # 3 blinks, 0.5 seconds each
            alert_message = ""
            turning_message_start_time = None

    # Display speed, size, and weight at the top right corner
    speed_text = font.render(f"Speed: {speed} km/h", True, BLACK)
    size_text = font.render(f"Size: {size[0]} x {size[1]} units", True, BLACK)
    weight_text = font.render(f"Weight: {weight} kg", True, BLACK)

    text_x = SCREEN_WIDTH - TEXT_MARGIN - max(speed_text.get_width(), size_text.get_width(), weight_text.get_width())
    screen.blit(speed_text, (text_x, MESSAGE_AREA_Y + TEXT_MARGIN))
    screen.blit(size_text, (text_x, MESSAGE_AREA_Y + TEXT_MARGIN + speed_text.get_height() + 5))
    screen.blit(weight_text, (text_x, MESSAGE_AREA_Y + TEXT_MARGIN + speed_text.get_height() + size_text.get_height() + 10))

    pygame.display.flip()
    clock.tick(FPS)

# Cleanup
camera.close()
pygame.quit()
