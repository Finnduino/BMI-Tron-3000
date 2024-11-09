import http.client
import json
import mimetypes
from io import BytesIO
import matplotlib.pyplot as plt



def gatherData():
    # Replace "your_image.jpg" with your actual file path
    file_path = 'data/floorplan-apartment-ground-floor.png'
    boundary = "----011000010111000001101001"

    # Open the file and read the binary data
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Construct payload for multipart form-data
    payload = BytesIO()
    payload.write(f"--{boundary}\r\n".encode())
    payload.write(f'Content-Disposition: form-data; name="image"; filename="{file_path}"\r\n'.encode())
    payload.write(f"Content-Type: {mimetypes.guess_type(file_path)[0]}\r\n\r\n".encode())
    payload.write(file_data)
    payload.write(f"\r\n--{boundary}--\r\n".encode())



    with open('data/keysAndStuff.json') as f:
        data = json.load(f)
        API_KEY = data['rasterscan']

    # Set the headers
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "floor-plan-digitalization.p.rapidapi.com",
        'Content-Type': f"multipart/form-data; boundary={boundary}"
    }

    # Make the HTTPS connection and send the request
    conn = http.client.HTTPSConnection("floor-plan-digitalization.p.rapidapi.com")
    conn.request("POST", "/raster-to-vector-raw", body=payload.getvalue(), headers=headers)

    # Get the response
    res = conn.getresponse()
    data_str = res.read().decode("utf-8")
    data = json.loads(data_str)
    return (data)

# Print the response
#print(data.decode("utf-8"))

data = gatherData()

points = []
maxHeight= 10
for each in data['rooms']:
    print(each)
    for point in each:
        print(point['x'], point['y'])
        points.append((point['x'], point['y'], maxHeight))
        points.append((point['x'], point['y'], 0))

print(points)
vertices=points
wall_pairs = []
for i in range(0, len(vertices), 2):
    wall_pairs.append((vertices[i], vertices[i + 1]))

# Initialize a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot each wall as a line between two points
for start, end in wall_pairs:
    x_values = [start[0], end[0]]
    y_values = [start[1], end[1]]
    z_values = [start[2], end[2]]
    ax.plot(x_values, y_values,z_values, color='black', linewidth=2)



# Set labels
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Plot of Walls")

# Show the plot
plt.show()
