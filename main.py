import time
from PIL import Image, ImageDraw, ImageFont
from Joystick import Joystick  # 조이스틱 클래스 추가
from character import *
from image_loader import load_images
from map import initial_level_map1, get_initial_level_map

# 전역 변수 선언
level_map = initial_level_map1  # 초기화
# 전체 코인 수를 위한 변수
total_items_collected = 0
# 현재 스테이지에서 모은 코인 수를 위한 변수
current_items_collected = 0

current_level = 1  # 현재 레벨 초기화
original_level_map = initial_level_map1

def main():
    joystick = Joystick()  # 조이스틱 클래스 인스턴스 생성
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    
     # 이미지 로드
    bg_image_resized, player_image, tile_image, item_image, gameover_image, gameover_image2,  player_size, tile_size, next_image, gamestart_image, exit_image, perfect_image, great_image, good_image = load_images(joystick)
    character = Character(joystick.width // 2, joystick.height - 50, player_image)  # player_image 전달

    global level_map, current_items_collected, total_items_collected, current_level, original_level_map  # 전역 변수 사용
    offset_x = 0
    scroll_speed = 5
    
    def reset_level_map(level):
        global level_map, original_level_map
        original_level_map = get_initial_level_map(level)
        level_map = [row[:] for row in original_level_map]
    
    # 시작 화면 표시
    game_start = False
    while not game_start:
        my_image.paste(gamestart_image, (0, 0))  #시작 화면
        joystick.disp.image(my_image)
        if not joystick.button_A.value:
            game_start = True
    
    reset_level_map(current_level)

    while True:
        
        command = None
        if not joystick.button_A.value:
            command = 'jump'
        if not joystick.button_L.value:
            command = 'left_pressed'
        if not joystick.button_R.value:
            command = 'right_pressed'
        if not joystick.button_B.value:
            command = 'pick_item'
        if not joystick.button_U.value:
            command = 'next_stage'    
        


        if command == 'jump':
            character.jump()
        
        character.velocity[0] = 0  # 매 루프 시작 시 속도를 0으로 초기화

        if command == 'left_pressed':
            character.velocity[0] = -(character.speed+5)

        if command == 'right_pressed':
            character.velocity[0] = character.speed
        
        # 아이템을 픽업하는 로직 추가
        if command == 'pick_item':
            # 현재 캐릭터의 위치에 'P'가 있는지 확인
            col_index = int(character.position[0] + offset_x) // tile_size
            row_index = int(character.position[1]) // tile_size
            
            if 0 <= row_index < len(level_map) and 0 <= col_index < len(level_map[0]):
                if level_map[row_index][col_index] == 'P':
                    level_map[row_index][col_index] = ' '  # 아이템을 제거
                    current_items_collected += 1
                    total_items_collected += 1  # 아이템 수 증가
        if command == 'next_stage':
            # 현재 캐릭터의 위치에 'N'가 있는지 확인
            col_index = int(character.position[0] + offset_x) // tile_size
            row_index = int(character.position[1]) // tile_size
            if 0 <= row_index < len(level_map) and 0 <= col_index < len(level_map[0]):
                if level_map[row_index][col_index] == 'N':
                    # 게임 재시작
                    character.position = [joystick.width // 2, joystick.height - 50]
                    character.velocity = [0, 0]
                    offset_x = 0
                    # 다음 레벨로 이동
                    current_level += 1
                    scroll_speed += 2
                    reset_level_map(current_level)
                    # 전체 코인 수 업데이트
                    current_items_collected = 0  # 현재 스테이지 아이템 수 초기화
                    continue  # 게임 루프를 다시 시작
                if level_map[row_index][col_index] == 'E':
                    if total_items_collected >= 14:
                        my_image.paste(perfect_image, (0, 0))  # 종료화면: 최고 성과
                    elif total_items_collected >= 10: 
                        my_image.paste(great_image, (0, 0))  # 좋은 성과
                    else:
                        my_image.paste(good_image, (0, 0))   # 기본 성과
                        
                    joystick.disp.image(my_image)
                    break
        character.position[0] += character.velocity[0]  # 속도에 따라 위치 업데이트
        #화면 이탈 방지
        
        if character.position[0] > joystick.width - character.width // 2:
            character.position[0] = joystick.width - character.width // 2
        
       # 플레이어가 화면을 이탈했는지 체크
        if character.position[1] > joystick.height or character.position[0] < 0 or character.position[0] > joystick.width:
            if character.position[0] < 0:
                my_image = gameover_image2.copy()
            else:
                # 게임 오버 화면 표시
                my_image = gameover_image.copy()
            joystick.disp.image(my_image)
            
            # A 버튼이 눌릴 때까지 대기
            while joystick.button_A.value:  # A 버튼이 눌리지 않았다면 대기
                time.sleep(0.1)  # A 버튼이 눌릴 때까지 대기
                
            level_map = [row[:] for row in original_level_map]
            
            # 게임 재시작
            character.position = [joystick.width // 2, joystick.height - 50]
            character.velocity = [0, 0]
            offset_x = 0
            total_items_collected -= current_items_collected
            current_items_collected = 0  # 현재 스테이지 아이템 수 초기화
            
            continue  # 게임 루프를 다시 시작
        

        character.update(level_map, tile_size, offset_x)

         # 오프셋 업데이트
        if offset_x < (len(level_map[0]) * tile_size) - joystick.width:
            offset_x += scroll_speed  # 스크롤 속도에 따라 오프셋 증가
        else:
            offset_x = (len(level_map[0]) * tile_size) - joystick.width  # 오프셋을 최대값으로 설정
        
        my_image = Image.new("RGB", (joystick.width, joystick.height))
        my_image.paste(bg_image_resized, (0, 0))  # 배경을 먼저 붙여넣기

        # 레벨 맵에서 타일 이미지를 직접 붙여넣기
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                if tile == 'X':
                    # 타일 이미지 붙여넣기 (오프셋 적용)
                    tile_position = (col_index * tile_size - offset_x, row_index * tile_size)
                    my_image.paste(tile_image, tile_position, tile_image)  # 알파 채널을 사용하여 투명도 유지
                elif tile == 'P':
                    # item 이미지 붙여넣기 (오프셋 적용)
                    item_position = (col_index * tile_size - offset_x, row_index * tile_size)
                    my_image.paste(item_image, item_position, item_image)  # 알파 채널을 사용하여 투명도 유지
                elif tile == 'N':
                    # item 이미지 붙여넣기 (오프셋 적용)
                    next_position = (col_index * tile_size - offset_x, row_index * tile_size -20)
                    my_image.paste(next_image, next_position, next_image)  # 알파 채널을 사용하여 투명도 유지   
                elif tile == 'E':
                    exit_position = (col_index * tile_size - offset_x, row_index * tile_size)
                    my_image.paste(exit_image, exit_position, exit_image)
        # 캐릭터 이미지 붙여넣기
        character_frame = character.get_current_image()  # 현재 방향에 따라 이미지 가져오기
        my_image.paste(character_frame, (int(character.position[0] - character_frame.width // 2), 
                                           int(character.position[1] - character_frame.height)), 
                        character_frame)  # 알파 채널을 사용하여 투명도 유지

         # 삭제한 아이템 수를 화면에 표시
        draw = ImageDraw.Draw(my_image)
        font = ImageFont.load_default()  # 기본 폰트 사용
        draw.text((10, 10), f"Items: {total_items_collected}", fill=(255, 255, 255), font=font)
        
        joystick.disp.image(my_image)

        time.sleep(0.1)

if __name__ == '__main__':
    main()
