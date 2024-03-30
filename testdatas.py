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


        # İşlemleri burada gerçekleştir, örneğin veritabanına kaydet
        print("Marker Data:", marker_data)
        print("Rectangle Data:", rectangle_data)

        # Dört koordinatın x ve y değerlerinin ortalamasını alarak orta noktayı bulma
        sum_x = sum(coord[0] for coord in rectangle_data_list)
        sum_y = sum(coord[1] for coord in rectangle_data_list)
        center_x = sum_x / len(rectangle_data_list)
        center_y = sum_y / len(rectangle_data_list)

        print("Orta Nokta Koordinatları:", (center_x, center_y))

        # Marker verilerinin her biri için orta noktaya olan kuş uçuşu mesafesini hesapla
        distances_kus = []
        distances_metre = []
        for marker_coords in marker_data_list:
            distance_kus = hesapla_kus((center_x, center_y), marker_coords)
            distances_kus.append(distance_kus)

            distance_metre = hesapla_metre((center_x, center_y), marker_coords)
            distances_metre.append(distance_metre)
            print(marker_coords ," Kuş Uçuşu Mesafe:", distance_kus, "   ||   metre mesafe : ", distance_metre)  

        data = {
            "center_x": center_x,
            "center_y": center_y,
            "marker_coords": marker_data_list,
            "rectangle_data": rectangle_data_list,
            "distance_metre" : distances_metre,
            "distance_kus" : distances_kus
        }

        json_data = json.dumps(data)
        with open("output.json", "w") as json_file:
            json_file.write(json_data)

        return render_template('sonuc.html', mdList = marker_data_list, distance = distance, rcList = rectangle_data_list, orta_nokta = (center_x, center_y))

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

    print("Orta Nokta Koordinatları:", (center_x, center_y))

    # Marker verilerinin her biri için orta noktaya olan kuş uçuşu mesafesini hesapla
    distances_kus = []
    distances_metre = []
    for marker_coords in marker_data_list:
        distance_kus = hesapla_kus((center_x, center_y), marker_coords)
        distances_kus.append(distance_kus)

        distance_metre = hesapla_metre((center_x, center_y), marker_coords)
        distances_metre.append(distance_metre)
        print(marker_coords ," Kuş Uçuşu Mesafe:", distance_kus, "   ||   metre mesafe : ", distance_metre)  
        print(center_x, " ", center_y)
    
    data = {
            "center_x": center_x,
            "center_y": center_y,
            "marker_coords": marker_data_list,
            "rectangle_data": rectangle_data_list,
            "distance_metre" : distances_metre,
            "distance_kus" : distances_kus
        }
    
    json_data = json.dumps(data)
    with open("output.json", "w") as json_file:
        json_file.write(json_data)
    

    return render_template('sonuc.html', mdList = marker_data_list, distance = distance, rcList = rectangle_data_list, orta_nokta = (center_x, center_y))
        
    
    # İşlemleri yaptıktan sonra bir yanıt gönderin. Örneğin JSON formatında bir yanıt gönderebilirsiniz.
    return jsonify({"message": "Veriler başarıyla alındı!", "data": data})

if __name__ == '__main__':
    app.run(debug=False)


