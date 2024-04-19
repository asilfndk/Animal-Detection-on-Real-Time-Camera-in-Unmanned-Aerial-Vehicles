from flask import Flask, render_template, request, jsonify
import math
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Kuş uçuşu mesafe
def hesapla_kus(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

# Metre olarak mesafe
def hesapla_metre(coord1, coord2):
    # Dereceleri radyanlara dönüştür
    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    # İki nokta arasındaki enlem ve boylam farkını hesapla
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Haversine formülünü kullanarak uzaklığı hesapla
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000  # Earth's radius in meters
    distancem = R * c

    return distancem

@app.route('/sonuc', methods=['POST'])
def sonuc():    
    if request.method == 'POST':
        # POST isteği alındığında markerData ve rectangleData'yı al
        marker_data = request.form.get('markerData')
        rectangle_data = request.form.get('rectangleData')

        # İlk elemanı silmek için marker_data'yı listeye dönüştürüp dilimleyin
        marker_data_list = eval(marker_data)
        marker_data_list = marker_data_list[1:]

        rectangle_data_list = eval(rectangle_data)
        rectangle_data_list = rectangle_data_list[1:]

        # Dört koordinatın x ve y değerlerinin ortalamasını alarak orta noktayı bulma
        sum_x = sum(coord[0] for coord in rectangle_data_list)
        sum_y = sum(coord[1] for coord in rectangle_data_list)
        center_x = sum_x / len(rectangle_data_list)
        center_y = sum_y / len(rectangle_data_list)

        # Hayvan koordinatları ve diğer verileri oluştur
        animals_coords = {}
        for i, coords in enumerate(marker_data_list, start=1):
            animal_coords = {
                "x": coords[0],
                "y": coords[1],
                "name": f"Hayvan{i}",
                "temperature": 15 + i * 2,  # Sıcaklık için varsayılan bir değer
                "distance_metre": hesapla_metre((center_x, center_y), coords)
            }
            animals_coords[f"animal_coords_{i}"] = animal_coords

        # Kamera koordinatları
        camera_coords = rectangle_data_list[:4]  # Sadece ilk dört koordinatı al

        # JSON verisini oluştur
        data = {
            "center_x": center_x,
            "center_y": center_y,
            "animal_coords": animals_coords,
            "camera_coords": camera_coords
        }

        # JSON dosyasına yaz
        with open("output.json", "w") as json_file:
            json.dump(data, json_file)

        return render_template('sonuc.html', mdList=marker_data_list, distance=distance, rcList=rectangle_data_list, orta_nokta=(center_x, center_y))

@app.route('/', methods=['GET'])
def index():    
    mdList = []
    global distance 
    distance = 0
    distance_metre = 0
    rcList = []
    orta_nokta = []
    
    if request.method == 'GET':
        # GET istekleri için index.html dosyasını render et    
        return render_template('index.html')
    
@app.route('/gonder', methods=['POST'])
def gonder():
    data = request.get_json()
    # Gelen verileri işleyin.
    marker_data_list = data["mdList1"]    
    rectangle_data_list = data["rectangleCoordinates"]

    # Dört koordinatın x ve y değerlerinin ortalamasını alarak orta noktayı bulma
    sum_x = sum(coord[0] for coord in rectangle_data_list)
    sum_y = sum(coord[1] for coord in rectangle_data_list)
    center_x = sum_x / len(rectangle_data_list)
    center_y = sum_y / len(rectangle_data_list)

    # Hayvan koordinatları ve diğer verileri oluştur
    animals_coords = {}
    for i, coords in enumerate(marker_data_list, start=1):
        animal_coords = {
            "x": coords[0],
            "y": coords[1],
            "name": f"Hayvan{i}",
            "temperature": 15 + i * 2,  # Sıcaklık için varsayılan bir değer
            "distance_metre": hesapla_metre((center_x, center_y), coords)
        }
        animals_coords[f"animal_coords_{i}"] = animal_coords

    # Kamera koordinatları
    camera_coords = rectangle_data_list[:4]  # Sadece ilk dört koordinatı al

    # JSON verisini oluştur
    data = {
        "center_x": center_x,
        "center_y": center_y,
        "animal_coords": animals_coords,
        "camera_coords": camera_coords
    }

    # JSON dosyasına yaz
    with open("output.json", "w") as json_file:
        json.dump(data, json_file)

    # İşlemleri yaptıktan sonra bir yanıt gönderin. Örneğin JSON formatında bir yanıt gönderebilirsiniz.
    return jsonify({"message": "Veriler başarıyla alındı!", "data": data})

if __name__ == '__main__':
    app.run(debug=False)
