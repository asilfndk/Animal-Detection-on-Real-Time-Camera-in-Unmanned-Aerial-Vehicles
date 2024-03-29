import cv2
import numpy as np
import random

class VideoProcessor:
    def __init__(self, video_file, target_width, target_height):
        self.video_file = video_file
        self.target_width = target_width
        self.target_height = target_height
        self.cap = cv2.VideoCapture(video_file)
        self.animal = {
            'size': 20,
            'x': random.randint(0, target_width - 20),
            'y': random.randint(0, target_height - 20),
            'speed_x': 2,
            'speed_y': 2
        }
        self.corners = {
            'top_left': (320, 180),
            'top_right': (1600, 180),
            'bottom_left': (320, 900),
            'bottom_right': (1600, 900)
        }

    def process_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            original_height, original_width = frame.shape[:2]
            background = np.zeros((self.target_height, self.target_width, 3), dtype=np.uint8)
            x_offset = (self.target_width - original_width) // 2
            y_offset = (self.target_height - original_height) // 2
            background[y_offset:y_offset + original_height, x_offset:x_offset + original_width] = frame

            animal_center_x = self.animal['x'] + self.animal['size'] // 2
            animal_center_y = self.animal['y'] + self.animal['size'] // 2

            self.draw_corners(background)
            self.draw_animal(background, animal_center_x, animal_center_y)
            self.move_animal()
            self.draw_arrow_if_needed(background, x_offset, y_offset, original_width, original_height)

            cv2.imshow('Video', background)
            if cv2.waitKey(25) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def draw_corners(self, background):
        for corner_name, corner_pos in self.corners.items():
            cv2.putText(background, f"{corner_pos}", corner_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_animal(self, background, center_x, center_y):
        cv2.putText(background, f"Animal Position: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        background[self.animal['y']:self.animal['y'] + self.animal['size'], self.animal['x']:self.animal['x'] + self.animal['size']] = (0, 255, 0)

    def move_animal(self):
        self.animal['x'] += self.animal['speed_x']
        self.animal['y'] += self.animal['speed_y']

        for coord, speed, size, limit in zip(('x', 'y'), ('speed_x', 'speed_y'), ('size', 'size'), (self.target_width, self.target_height)):
            if self.animal[coord] <= 0 or self.animal[coord] + self.animal[size] >= limit:
                self.animal[speed] *= -1
                if self.animal[coord] <= 0:
                    self.animal[coord] = 0
                else:
                    self.animal[coord] = limit - self.animal[size]

    def draw_arrow_if_needed(self, background, x_offset, y_offset, original_width, original_height):
        if any((
            self.animal['x'] < x_offset,
            self.animal['x'] + self.animal['size'] > x_offset + original_width,
            self.animal['y'] < y_offset,
            self.animal['y'] + self.animal['size'] > y_offset + original_height
        )):
            arrow_start_x = max(min(self.animal['x'] + self.animal['size'] // 2, x_offset + original_width - 50), x_offset + 50)
            arrow_start_y = max(min(self.animal['y'] + self.animal['size'] // 2, y_offset + original_height - 50), y_offset + 50)

            if self.animal['x'] < x_offset:
                arrow_end_x = x_offset
            elif self.animal['x'] + self.animal['size'] > x_offset + original_width:
                arrow_end_x = x_offset + original_width - 1
            else:
                arrow_end_x = self.animal['x'] + self.animal['size'] // 2

            if self.animal['y'] < y_offset:
                arrow_end_y = y_offset
            elif self.animal['y'] + self.animal['size'] > y_offset + original_height:
                arrow_end_y = y_offset + original_height - 1
            else:
                arrow_end_y = self.animal['y'] + self.animal['size'] // 2

            arrow_end = (arrow_end_x, arrow_end_y)

            cv2.arrowedLine(background, (arrow_start_x, arrow_start_y), arrow_end, (0, 255, 0), 2)

            distance_x = abs(arrow_end_x - (self.animal['x'] + self.animal['size'] // 2))
            distance_y = abs(arrow_end_y - (self.animal['y'] + self.animal['size'] // 2))
            animal_distance = round(np.sqrt(distance_x ** 2 + distance_y ** 2), 2)

            cv2.putText(background, f"Animal Distance: {animal_distance}",
                        (arrow_end_x + 10, arrow_end_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

if __name__ == "__main__":
    video_file = "videos\ornek_video.mp4"
    target_width = 1920
    target_height = 1080

    video_processor = VideoProcessor(video_file, target_width, target_height)
    video_processor.process_video()
