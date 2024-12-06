from PIL import Image, ImageDraw


class Character:
    def __init__(self, x, y, image):
        self.position = [x, y]
        self.width = 8  # 캐릭터의 가로 크기
        self.height = 1  # 캐릭터의 세로 크기
        self.velocity = [0, 0]
        self.on_ground = False
        self.speed = 7
        self.animation_frames = self.load_animation_frames(image)
        self.current_frame = 0
        self.walk_frame_count = 4  # 걷기 애니메이션 프레임 수
        self.jump_frame = 6  # 점프 애니메이션 프레임
        self.frame_timer = 0
        self.frame_duration = 0.1  # 프레임 전환 시간
        self.is_jumping = False  # 점프 상태 추적
        
    def get_current_image(self):
        if self.velocity[0] < 0:  # 왼쪽으로 이동 중
            return self.animation_frames[self.current_frame].transpose(Image.FLIP_LEFT_RIGHT)
        else:  # 오른쪽으로 이동 중 또는 정지
            return self.animation_frames[self.current_frame]
        
    def load_animation_frames(self, image):
        image = image.convert("RGBA")  # RGBA 모드로 변환
        width, height = image.size
        frame_width = width // 8  # 가로 프레임 수
        frame_height = height // 8  # 세로 프레임 수
        frames = []

        for row in range(4):
            for col in range(4):
                frame = image.crop((col * frame_width, row * frame_height,
                                    (col + 1) * frame_width, (row + 1) * frame_height))
                frame = frame.resize((frame_width * 3, frame_height * 3), Image.LANCZOS)
                frames.append(frame)
        return frames

    def move(self, dx):
        self.position[0] += dx * self.speed
        if dx != 0:  # 이동할 때 애니메이션 프레임 전환
            self.current_frame = (self.current_frame + 1) % self.walk_frame_count

    def jump(self):
        if self.on_ground:
            self.velocity[1] = -18
            self.current_frame = self.jump_frame
            self.is_jumping = True

    def update(self, level_map, tile_size, offset_x):
        self.velocity[1] += 4
        self.position[1] += self.velocity[1]
        self.check_collision(level_map, tile_size, offset_x)
        self.update_animation()

    def update_animation(self):
        if self.on_ground:
            if self.velocity[1] == 0:
                self.frame_timer += 0.1
                if self.frame_timer >= self.frame_duration:
                    self.current_frame = (self.current_frame + 1) % self.walk_frame_count
                    self.frame_timer = 0
        else:
            self.current_frame = self.jump_frame

    def check_collision(self, level_map, tile_size, offset_x):
        # 캐릭터의 실제 경계를 계산
        character_rect = (
            self.position[0] - self.width // 2,
            self.position[1] - self.height,
            self.position[0] + self.width // 2,
            self.position[1]
        )

        if character_rect[1] >= 400:  # 바닥 충돌 감지
            self.position[1] = 400
            self.on_ground = True
            self.velocity[1] = 0
            self.is_jumping = False  # 점프 상태 초기화
        else:
            self.on_ground = False

        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                if tile == 'X':
                    tile_rect = (
                        col_index * tile_size - offset_x,  # 오프셋을 적용
                        row_index * tile_size,
                        (col_index + 1) * tile_size - offset_x,  # 오프셋을 적용
                        (row_index + 1) * tile_size
                    )
                    # 충돌 감지
                    if (character_rect[2] > tile_rect[0] and
                        character_rect[0] < tile_rect[2] and
                        character_rect[3] > tile_rect[1] and
                        character_rect[1] < tile_rect[3]):
                        if self.velocity[1] > 0:  # 아래로 떨어질 때
                            self.position[1] = tile_rect[1] - (character_rect[3] - character_rect[1])
                            self.on_ground = True
                            self.velocity[1] = 0
                            self.is_jumping = False  # 점프 상태 초기화
                        
                        
                        

    def draw(self, draw):
        frame = self.animation_frames[self.current_frame]
        draw.bitmap((self.position[0] - frame.width // 2, self.position[1] - frame.height),
                    frame, fill=None)