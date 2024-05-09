import cv2
import json
from shapely.geometry import Point, Polygon

# Video dosyasını aç
video_path = "videos/ornek_video.mp4"  # Video dosyasının yolunu belirtin
cap = cv2.VideoCapture(video_path)

# JSON dosyasını aç
json_file = "output.json"
with open(json_file, 'r') as f:
    data = json.load(f)

# Video boyutlarını al
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Köşe noktalarını belirle
corner_points = {
    "Sag Alt": (width - 260, height - 10),
    "Sag Ust": (width - 260, 20),
    "Sol Ust": (0, 20),
    "Sol Alt": (0, height - 7)
}
edge_names = ["Sag Taraf","Ust Taraf","Sol Taraf","Alt Taraf"]

# Videoyu açık tut
while(cap.isOpened()):
    # Video çerçevesini oku
    ret, frame = cap.read()
    if not ret:
        break

    # Köşelere metinleri yazdır
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2
    text_color = (255, 255, 255) 
    for corner, coord in corner_points.items():
        index = list(corner_points.keys()).index(corner)
        x, y = data['camera_coords'][index]
        text = f"{x:.6f}, {y:.6f}"
        cv2.putText(frame, text, coord, font, font_scale, text_color, font_thickness, cv2.LINE_AA)

    # Dikdörtgenin köşe noktalarını belirle
    rect_coords = [data["camera_coords"][0], data["camera_coords"][1], data["camera_coords"][2], data["camera_coords"][3]]
    rect_polygon = Polygon(rect_coords)

    # Başlangıç yüksekliği
    y_offset = 50

    # Her hayvan için kontrol et
    for animal_key, animal_data in data['animal_coords'].items():
        animal_x = animal_data['x']
        animal_y = animal_data['y']
        animal_point = Point(animal_x, animal_y)
        
        # Hayvanın konumunu dikdörtgenin içinde mi dışında mı kontrol et
        if rect_polygon.contains(animal_point):
            cv2.putText(frame, f"{animal_data['name']} icinde", (0, y_offset), font, 0.5, text_color, 1, cv2.LINE_AA)
        else:
            # Hayvanın dikdörtgenin hangi kenarına daha yakın olduğunu bul
            nearest_side_index = None
            min_distance = float('inf')
            for i, (start_x, start_y) in enumerate(rect_coords):
                end_x, end_y = rect_coords[(i + 1) % 4]
                side_center_x = (start_x + end_x) / 2
                side_center_y = (start_y + end_y) / 2
                distance = ((animal_x - side_center_x) ** 2 + (animal_y - side_center_y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_side_index = i

            # En yakın kenarın ismini al
            nearest_side_name = edge_names[nearest_side_index]
            
            # Hayvanın ekran dışında olduğu ve en yakın kenarı yazdır
            cv2.putText(frame, f"{animal_data['name']} disinda ({nearest_side_name})", (0, y_offset), font, 0.5, text_color, 1, cv2.LINE_AA)
        
        # Yüksekliği artır
        y_offset += 30

    # İşlenen çerçeveyi göster
    cv2.imshow('Video', frame)
    
    # q tuşuna basılınca videoyu kapat
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Açılan pencereleri kapat
cap.release()
cv2.destroyAllWindows()
