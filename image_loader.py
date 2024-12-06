# image_loader.py
from PIL import Image

def load_images(joystick):
    # 배경 이미지 로드
    bg_image = Image.open("asset/Cave.png")
    bg_image_resized = bg_image.resize((joystick.width, joystick.height))

    # player.png를 로드
    player_image = Image.open("asset/player.png")
    player_width, player_height = player_image.size  # 플레이어 이미지 사이즈 접근

    # tile.png를 로드
    tile_image = Image.open("asset/tile.png")
    tile_size = 30  # tile_size 정의
    tile_image = tile_image.resize((tile_size, tile_size))

    # item.png를 로드
    item_image = Image.open("asset/item.png")
    item_size = 20
    item_image = item_image.resize((item_size, item_size))

    # gameover 이미지 로드
    gameover_image = Image.open("asset/gameover_1.png").resize((joystick.width, joystick.height))
    gameover_image2 = Image.open("asset/gameover_2.png").resize((joystick.width, joystick.height))


    # nextstage.png를 로드
    next_image = Image.open("asset/nextstage.png")
    next_image = next_image.resize((30, 60))
    
    #gamestart.png를 로드
    gamestart_image = Image.open("asset/gamestart.png").resize((joystick.width, joystick.height))

    #Ending.png를 로드
    perfect_image = Image.open("asset/perfect.png").resize((joystick.width, joystick.height))
    great_image = Image.open("asset/great.png").resize((joystick.width, joystick.height))
    good_image = Image.open("asset/good.png").resize((joystick.width, joystick.height))


    # exit.png를 로드
    exit_image = Image.open("asset/exit.png")
    exit_image = next_image.resize((30, 30))
    
    return bg_image_resized, player_image, tile_image, item_image, gameover_image, gameover_image2, (player_width, player_height), tile_size, next_image, gamestart_image, exit_image, perfect_image, great_image, good_image
