import cv2
import pygame
import sys
import time
import numpy as np

pygame.init()

# Set the screen to full desktop screen
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set the display to full-screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Camera Display")

font = pygame.font.SysFont(None, 30)

cap = cv2.VideoCapture(0)
cap.set(3, SCREEN_WIDTH)
cap.set(4, SCREEN_HEIGHT)

# Load sound for alarm
alarm_sound = pygame.mixer.Sound('mixkit-facility-alarm-sound-999.wav')
def play_alarm_for_8_seconds():
    alarm_sound.play()
    start_time = time.time()
    
    # Keep checking the time and stop the sound after 8 seconds
    while time.time() - start_time < 8:
        pygame.time.wait(100)  # Wait for a short duration to reduce CPU usage
    
    alarm_sound.stop()

# Main loop (simplified for demonstration purposes)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                play_alarm_for_8_seconds()  # Play the alarm for 8 seconds when 'S' is pressed

clock = pygame.time.Clock()
running = True
overtake_time = None
alert_message = ""
brake_message = ""
lane_change_message = ""  # Message for lane change
sleeping_message = ""  # Message to indicate that the driver is sleeping
object_detected_message = ""  # Message to indicate object detected
engine_repair_message = ""  # Message to indicate engine repair needed
message_start_time = None  # Time when any message starts
turning_message_start_time = None  # Time when turning message starts
show_overtake_message = False  # Flag to show overtake message
overtake_message_start_time = None  # Time when the overtake message starts
sleeping_message_start_time = None  # Time when the sleeping message starts
object_detected_message_start_time = None  # Time when the object detected message starts
engine_repair_message_start_time = None  # Time when the engine repair message starts

# Sample data for speed, size, and weight (can be replaced with real data if available)
speed = 60  # in km/hr
size = (100, 50)  # in units
weight = 1200  # in kg (vehicle weight)

# Constants for screen sections
CAMERA_VIEW_HEIGHT = int(SCREEN_HEIGHT * 0.75)  # 75% of the screen height for the camera view
MESSAGE_AREA_HEIGHT = SCREEN_HEIGHT - CAMERA_VIEW_HEIGHT  # 25% of the screen height for messages
MESSAGE_AREA_Y = CAMERA_VIEW_HEIGHT  # Start the message area just below the camera view
TEXT_MARGIN = 10  # Margin from the right edge for text positioning

def display_blinking_message(message, start_time, duration, y_position):
    """Display a blinking message for a given duration"""
    current_time = time.time()
    if current_time - start_time < duration:
        if current_time % 1 < 0.5:  # Blink every half second
            text = font.render(message, True, RED)
            screen.blit(text, (TEXT_MARGIN, y_position))  # Position in the 25% message display area

while running:
    screen.fill(WHITE)

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        
        # Blit the camera frame within the top 75% of the screen
        camera_surf = pygame.transform.scale(frame, (SCREEN_WIDTH, CAMERA_VIEW_HEIGHT))
        screen.blit(camera_surf, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                alert_message = "Turning left!"
                turning_message_start_time = time.time()
                brake_message = ""  # Clear any brake message
                show_overtake_message = False  # Stop overtake message
                sleeping_message = ""  # Clear any sleeping message
                object_detected_message = ""  # Clear object detected message
                engine_repair_message = ""  # Clear engine repair message
                lane_change_message = ""  # Clear any lane change message
            elif event.key == pygame.K_RIGHT:
                alert_message = "Turning right!"
                turning_message_start_time = time.time()
                brake_message = ""  # Clear any brake message
                show_overtake_message = False  # Stop overtake message
                sleeping_message = ""  # Clear any sleeping message
                object_detected_message = ""  # Clear object detected message
                engine_repair_message = ""  # Clear engine repair message
                lane_change_message = ""  # Clear any lane change message
            elif event.key == pygame.K_SPACE:
                brake_message = "Come slow"  # Set the brake message
                message_start_time = time.time()  # Start the timer for the message
                alert_message = ""  # Clear any alert message
                turning_message_start_time = None  # Stop any active turning message
                show_overtake_message = False  # Stop overtake message
                sleeping_message = ""  # Clear any sleeping message
                object_detected_message = ""  # Clear object detected message
                engine_repair_message = ""  # Clear engine repair message
                lane_change_message = ""  # Clear any lane change message
            elif event.key == pygame.K_1:
                show_overtake_message = True
                overtake_message_start_time = time.time()  # Start the timer for the overtake message
                alert_message = ""  # Clear any other alert message
                brake_message = ""  # Clear any brake message
                turning_message_start_time = None  # Stop any active turning message
                sleeping_message = ""  # Clear any sleeping message
                object_detected_message = ""  # Clear object detected message
                engine_repair_message = ""  # Clear engine repair message
                lane_change_message = ""  # Clear any lane change message
            elif event.key == pygame.K_s:
                sleeping_message = "Driver is sleeping! Be alert!"  # Set the sleeping message
                sleeping_message_start_time = time.time()  # Start the timer for the sleeping message
                alert_message = ""  # Clear any other alert message
                brake_message = ""  # Clear any brake message
                turning_message_start_time = None  # Stop any active turning message
                show_overtake_message = False  # Stop overtake message
                object_detected_message = ""  # Clear object detected message
                engine_repair_message = ""  # Clear engine repair message
                lane_change_message = ""  # Clear any lane change message
                # Play alarm sound
                alarm_sound.play()
            elif event.key == pygame.K_o:
                object_detected_message = "Object detected in front, Come slow!"  # Set the object detected message
                object_detected_message_start_time = time.time()  # Start the timer for the object detected message
                alert_message = ""  # Clear any other alert message
                brake_message = ""  # Clear any brake message
                turning_message_start_time = None  # Stop any active turning message
                show_overtake_message = False  # Stop overtake message
                sleeping_message = ""  # Clear any sleeping message
                engine_repair_message = ""  # Clear engine repair message
                lane_change_message = ""  # Clear any lane change message
            elif event.key == pygame.K_e:
                engine_repair_message = "It's time to repair the engine parts!, Be alert"  # Set the engine repair message
                engine_repair_message_start_time = time.time()  # Start the timer for the engine repair message
                alert_message = ""  # Clear any other alert message
                brake_message = ""  # Clear any brake message
                turning_message_start_time = None  # Stop any active turning message
                show_overtake_message = False  # Stop overtake message
                sleeping_message = ""  # Clear any sleeping message
                object_detected_message = ""  # Clear object detected message
                lane_change_message = ""  # Clear any lane change message
            elif event.key == pygame.K_l:
                lane_change_message = "It's time to change lanes!"  # Set the lane change message
                message_start_time = time.time()  # Start the timer for the message
                alert_message = ""  # Clear any alert message
                brake_message = ""  # Clear any brake message
                turning_message_start_time = None  # Stop any active turning message
                show_overtake_message = False  # Stop overtake message
                sleeping_message = ""  # Clear any sleeping message
                object_detected_message = ""  # Clear object detected message
                engine_repair_message = ""  # Clear engine repair message

    # Handle the overtake message
    if overtake_time:
        current_time = time.time()
        time_difference = current_time - overtake_time
        if time_difference >= 10:
            overtake_time = None
            alert_message = "It's time to overtake!"
            message_start_time = time.time()  # Start the timer for the message
        else:
            alert_message = f"Wait for {int(10 - time_difference)} seconds to overtake"
            message_start_time = time.time()  # Start the timer for the message

    # Display the alert and brake messages if within 3 seconds
    if message_start_time:
        display_blinking_message(alert_message, message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)
        display_blinking_message(brake_message, message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)

    # Handle the turning message blinking for 3 seconds
    if turning_message_start_time:
        display_blinking_message(alert_message, turning_message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)

    # Handle the overtake message blinking for 3 seconds
    if show_overtake_message:
        display_blinking_message("It's time to overtake!", overtake_message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)

    # Handle the sleeping message blinking for 3 seconds
    if sleeping_message_start_time:
        display_blinking_message(sleeping_message, sleeping_message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)

    # Handle the object detected message blinking for 3 seconds
    if object_detected_message_start_time:
        display_blinking_message(object_detected_message, object_detected_message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)

    # Handle the engine repair message blinking for 3 seconds
    if engine_repair_message_start_time:
        display_blinking_message(engine_repair_message, engine_repair_message_start_time, 3, MESSAGE_AREA_Y + TEXT_MARGIN)

    # Displaying the speed, size, and weight at the top right corner of the white space
    speed_text = font.render(f"Speed: {speed} km/hr", True, BLACK)
    size_text = font.render(f"Size: {size[0]} x {size[1]} units", True, BLACK)
    weight_text = font.render(f"Weight: {weight} kg", True, BLACK)
    
    # Positioning text in the top-right corner
    text_x = SCREEN_WIDTH - TEXT_MARGIN - max(speed_text.get_width(), size_text.get_width(), weight_text.get_width())
    screen.blit(speed_text, (text_x, MESSAGE_AREA_Y + TEXT_MARGIN))  # Position at the top right
    screen.blit(size_text, (text_x, MESSAGE_AREA_Y + TEXT_MARGIN + speed_text.get_height() + 5))  # Position below speed
    screen.blit(weight_text, (text_x, MESSAGE_AREA_Y + TEXT_MARGIN + speed_text.get_height() + size_text.get_height() + 10))  # Position below size

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
