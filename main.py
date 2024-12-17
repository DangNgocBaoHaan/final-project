import pygame, sys, time, random

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
# Thêm nhạc nền
win_sound = pygame.mixer.Sound("New folder\FileGame\sound\sfx_win.wav")
lose_sound = pygame.mixer.Sound("New folder\FileGame\sound\sfx_lose.wav")
bg_sound = pygame.mixer.Sound("New folder\FileGame\sound\sfx_bg.wav")
jump_sound = pygame.mixer.Sound("New folder\FileGame\sound\sfx_jump.wav")
squat_sound = pygame.mixer.Sound("New folder\FileGame\sound\sfx_squat.wav")
width, height = 600, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Helping robot go to school UEH")
yellow = (255, 255, 0)
background_image = pygame.image.load("New folder/Background.png")
background_image = pygame.transform.scale(background_image, (width, height))
player_image = {
    "Robot_blue": pygame.image.load("New folder/Robotblue.png"),
    "Robot_pink": pygame.image.load("New folder/Robotpink.png"),
    "Robot_gay": pygame.image.load("New folder/Robotgay.png")
}
current_character = "Robot_blue"
size_player_image = pygame.transform.scale(player_image[current_character], (300, 400))

levels = {
    "easy": {"time": 60},
    "medium": {"time": 45},

    "hard": {"time": 35}
}
current_level = "easy"
obstacle_image1 = pygame.image.load("New folder/Chướng ngại 1.png")
obstacle_image2 = pygame.image.load("New folder/Chướng ngại 2.png")
obstacle_width = 300
obstacle_height = 400
obstacle_image1 = pygame.transform.scale(obstacle_image1, (obstacle_width, obstacle_height))
obstacle_image2 = pygame.transform.scale(obstacle_image2, (obstacle_width, obstacle_height))
jump_image = {
    "Robot_blue_jump": pygame.image.load("New folder/robotblueup.png"),
    "Robot_pink_jump": pygame.image.load("New folder/robotpinkup.png"),
    "Robot_gay_jump": pygame.image.load("New folder/robotgayup.png")
}
current_jump = "Robot_blue_jump"
size_jump_image = pygame.transform.scale(jump_image[current_jump], (400, 600))
crouch_image = {
    "Robot_blue_crouch": pygame.image.load("New folder/robotbluesquat.png"),
    "Robot_pink_crouch": pygame.image.load("New folder/robotpinksquat.png"),
    "Robot_gay_crouch": pygame.image.load("New folder/robotgaysquat.png")
}
current_crouch = "Robot_blue_crouch"
size_crouch_image = pygame.transform.scale(crouch_image[current_crouch], (455, 600))
is_jumping = False
is_crouching = False
last_obstacle_time = 100
obstacle_interval = 4000
HE_image = {
    "blue_happy": pygame.image.load("New folder/Happyendingblue.png"),
    "pink_happy": pygame.image.load("New folder/HEpink.png"),
    "gay_happy": pygame.image.load("New folder/Happyendinggay.png")
}
current_HE_image = "blue_happy"
size_HE_image = pygame.transform.scale(HE_image[current_HE_image], (450, 350))
BE_image = {
    "blue_huhu": pygame.image.load("New folder/Badendingblue.png"),
    "pink_huhu": pygame.image.load("New folder/BEpink.png"),
    "gay_huhu": pygame.image.load("New folder/Badendinggay.png")
}
current_BE_image = "blue_huhu"
size_BE_image = pygame.transform.scale(BE_image[current_BE_image], (450, 350))
cloud1 = pygame.image.load('New folder/Cloud1.png')
cloud1 = pygame.transform.scale(cloud1, (500, 500))
cloud2 = pygame.image.load("New folder/Cloud2.png")
cloud2 = pygame.transform.scale(cloud2, (700, 700))
tree1 = pygame.image.load("New folder/Tree.png")
tree1 = pygame.transform.scale(tree1, (500, 700))
tree2 = pygame.image.load("New folder/Tree.png")
tree2 = pygame.transform.scale(tree1, (300, 500))
zoomin = 6
max_obstacles = 15
obstacles = []
obstacles_passed = 0
obstacle_type = random.choice([obstacle_image1, obstacle_image2])
rect_width = 20
rect_height = 100
gap = 50
num_rects = 5
rects = [{"x": 295, "y": 200 + i * (rect_height + gap)} for i in range(num_rects)]
speed_y = 1
play_time = levels[current_level]["time"]
player_x = 157
player_y = 470
cloud1_x = 500
cloud1_y = 50
cloud2_x = 500
cloud2_y = -80
speed_cloud1 = speed_cloud2 = 1
tree1_x = 300
tree1_y = 40
tree1_speed = 1
tree2_x = 70
tree2_y = 70
tree2_speed = 1
obstacle_y = 128
jump_x = 100
jump_y = 280
crouch_x = 86
crouch_y = 380
school = pygame.image.load("New folder/SchoolUEH.png")
school = pygame.transform.scale(school, (400, 500))
obstacle_speed = 5


def check_collision(obstacles):
    global player_x, player_y, play_time, obstacles_passed
    passed_obstacles = []
    for obstacle in obstacles[:]:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"])
        if is_jumping:
            jump_image_current = jump_image[current_jump]
            player_rect = pygame.Rect(jump_x, jump_y - jump_image_current.get_height() + 2895,
                                      jump_image_current.get_width(), jump_image_current.get_height())
        elif is_crouching:
            crouch_image_current = crouch_image[current_crouch]
            player_rect = pygame.Rect(crouch_x, crouch_y - crouch_image_current.get_height() + 2790,
                                      crouch_image_current.get_width(), crouch_image_current.get_height())
        else:
            player_rect = pygame.Rect(player_x, player_y + player_image[current_character].get_height() - 1800,
                                      player_image[current_character].get_width(),
                                      player_image[current_character].get_height())
        if player_rect.colliderect(obstacle_rect):
            if obstacle["type"] == obstacle_image1:
                if is_crouching:
                    continue
                else:
                    obstacle["y"] -= 100
                    obstacle["width"] -= 100
                    obstacle["height"] -= 100
            elif obstacle["type"] == obstacle_image2:
                if is_jumping:
                    continue
                else:
                    obstacle["y"] -= 100
                    obstacle["width"] -= 100
                    obstacle["height"] -= 100
            obstacle["collision_count"] += 1
            if obstacle["collision_count"] > 1:
                obstacles.remove(obstacle)
        if obstacle["y"] > 370 and obstacle not in passed_obstacles:
            obstacles_passed += 1
            passed_obstacles.append(obstacle)
    for passed_obstacle in passed_obstacles:
        if passed_obstacle in obstacles:
        obstacles.remove(passed_obstacle)


clock = pygame.time.Clock()
start_time = time.time()
target_time = start_time + play_time


def get_time_left():
    current_time = time.time()
    time_left = target_time - current_time
    return max(0, time_left)


def display_time_left(time_left):
    font = pygame.font.Font(None, 36)
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    time_text = f"{minutes:02}:{seconds:02}"
    time_surface = font.render(time_text, True, (255, 255, 0))
    screen.blit(time_surface, (width - 100, 10))


def show_game_over():
    if obstacles_passed >= 8:
        size_HE_image = pygame.transform.scale(HE_image[current_HE_image], (450, 350))
        screen.blit(size_HE_image, (75, 250))

    else:
        size_BE_image = pygame.transform.scale(BE_image[current_BE_image], (450, 350))
        screen.blit(size_BE_image, (75, 250))

    pygame.display.flip()
    pygame.time.delay(7000)
    pygame.quit()
    sys.exit()


def start_game():
    global player_image, current_level, play_time, target_time
    play_time = levels[current_level]["time"]
    target_time = time.time() + play_time
    bg_sound.play()
    game_loop()


def choose_character(direction):
    global current_character, size_player_image, current_HE_image, current_BE_image
    characters = list(player_image.keys())
    current_index = characters.index(current_character)
    if direction == "left":
        current_index = (current_index - 1) % len(characters)
    elif direction == "right":
        current_index = (current_index + 1) % len(characters)
    current_character = characters[current_index]
    size_player_image = pygame.transform.scale(player_image[current_character], (300, 400))
    if current_character == "Robot_blue":
        current_HE_image = "blue_happy"
        current_BE_image = "blue_huhu"
    elif current_character == "Robot_pink":
        current_HE_image = "pink_happy"
        current_BE_image = "pink_huhu"
    elif current_character == "Robot_gay":
        current_HE_image = "gay_happy"
        current_BE_image = "gay_huhu"


def choose_level(level):
    global current_level, play_time, target_time
    if level in levels:
        current_level = level
        print(f"Level changed to: {current_level}")
        play_time = levels[current_level]["time"]
        target_time = time.time() + play_time


def show_game_over():
    bg_sound.stop()  # Dừng nhạc nền
    if obstacles_passed > 7:
        size_HE_image = pygame.transform.scale(HE_image[current_HE_image], (450, 350))
        screen.blit(size_HE_image, (75, 250))
        win_sound.play()

    else:
        size_BE_image = pygame.transform.scale(BE_image[current_BE_image], (450, 350))
        screen.blit(size_BE_image, (75, 250))
        lose_sound.play()
    pygame.display.flip()
    pygame.time.delay(12000)
    pygame.quit()
    sys.exit()


def game_loop():
    global obstacles_passed, play_time, is_jumping, is_crouching, cloud1_x, cloud2_x, tree1_y, tree1_x, tree2_x, tree2_y, last_obstacle_time
    while True:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    choose_character("left")
                elif event.key == pygame.K_RIGHT:
                    choose_character("right")
                elif event.key == pygame.K_e:
                    choose_level("easy")
                    start_game()
                elif event.key == pygame.K_m:
                    choose_level("medium")
                    start_game()
                elif event.key == pygame.K_h:
                    choose_level("hard")
                    start_game()
                elif event.key == pygame.K_UP:
                    is_jumping = True
                    jump_sound.play()
                elif event.key == pygame.K_DOWN:
                    is_crouching = True
                    squat_sound.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    is_jumping = False
                elif event.key == pygame.K_DOWN:
                    is_crouching = False
        time_left = get_time_left()
        if time_left <= 0:
            show_game_over()
        screen.blit(background_image, (0, 0))
        display_time_left(time_left)
        for rect in rects:
            rect["y"] += speed_y
            if rect["y"] > height:
                rect["y"] = 200
            pygame.draw.rect(screen, yellow, (rect["x"], rect["y"], rect_width, rect_height))
        cloud1_x += speed_cloud1
        cloud2_x -= speed_cloud2
        tree1_y += tree1_speed
        tree1_x += tree1_speed
        tree2_y += tree2_speed
        tree2_x -= tree2_speed
        if cloud1_x > width:
            cloud1_x = -500
        if cloud2_x < -500:
            cloud2_x = width
        if tree1_y > 250:
            tree1_x = 300
            tree1_y = 10
        if tree2_y > 250:
            tree2_x = 60
            tree2_y = 50
        screen.blit(cloud1, (cloud1_x, cloud1_y))
        screen.blit(cloud2, (cloud2_x, cloud2_y))
        screen.blit(tree2, (tree2_x, tree2_y))
        screen.blit(tree1, (tree1_x, tree1_y))
        screen.blit(school, (103, 125))
        current_time = pygame.time.get_ticks()
        if len(obstacles) < max_obstacles and current_time - last_obstacle_time > obstacle_interval:
            obstacle_type = random.choice([obstacle_image1, obstacle_image2])
            obstacle_x = (width - obstacle_width) // 2
            obstacle_y = 125
            obstacles.append({"type": obstacle_type, "x": obstacle_x, "y": obstacle_y, "width": obstacle_width,
                              "height": obstacle_height, "collision_count": 0})

            last_obstacle_time = current_time
        if is_jumping:
            jump_image_current = jump_image[f"{current_character}_jump"]
            jump_image_current = pygame.transform.scale(jump_image_current, (400, 600))
            screen.blit(jump_image_current, (jump_x, jump_y))
        elif is_crouching:
            crouch_image_current = crouch_image[f"{current_character}_crouch"]
            crouch_image_current = pygame.transform.scale(crouch_image_current, (455, 600))
            screen.blit(crouch_image_current, (crouch_x, crouch_y))
        else:
            current_player_image = pygame.transform.scale(player_image[current_character], (300, 400))
            screen.blit(current_player_image, (player_x, player_y))
        for obstacle in obstacles[:]:
            obstacle["y"] += obstacle_speed * (obstacle["width"] / obstacle_width)
            obstacle["width"] += zoomin
            obstacle["height"] += zoomin
            obstacle["x"] = (width - obstacle["width"]) // 2
            screen.blit(pygame.transform.scale(obstacle["type"], (obstacle["width"], obstacle["height"])),
                        (obstacle["x"], obstacle["y"]))
        check_collision(obstacles)
        pygame.display.flip()
        clock.tick(60)


def main():
    choose_character("right")
    choose_level("hard")
    start_game()


if __name__ == "__main__":
    main()
