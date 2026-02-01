from ultralytics import YOLO

model = YOLO("models\\best.pt")

results = model.predict('D:\\Nti_football_analysis\\input_videos\\WhatsApp Video 2025-12-14 at 09.56.24_7c2d2ca1.mp4', save=True)
print(results[0])

print("*")
for box in results[0].boxes:
    print(box)