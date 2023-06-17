import cv2, torch, io, pickle, numpy as np
from PIL import Image

(tW, tH) = 111, 161
card = pickle.load(open("datasets/card_img.ob", "rb"))

def classificate_card(image):
    resized = cv2.resize(image, (tW, tH))

    found = [[0, "blank", "blank.jpg"]]
    for tmplt in card:
        name, img, template = tmplt
        result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        found.append([maxVal, name, img])
    
    found = sorted(found, key=lambda l:l[0], reverse=True)
    return found[:10]

def detect_card_filename(file_name = "source.jpg"):
    model = torch.hub.load('yolo/', 'custom', path='yolo/best.pt', source='local', skip_validation=True)
    im = f'images/{file_name}'
    results = model(im, size=640)
    
    img = cv2.imread(im)
    pre_result = results.pandas().xyxy[0].to_dict(orient="records")
    
    result = sorted(pre_result, key=lambda l:l["xmin"])
    
    for index, r in enumerate(result):
        crop_card = img[int(r['ymin']):int(r['ymax']),
                        int(r['xmin']):int(r['xmax'])]
        
        cv2.rectangle(img, (int(r['xmin']), int(r['ymin'])), (int(r['xmax']), int(r['ymax'])), color = (0, 0, 255), thickness=2)
        if r['xmax'] - r['xmin'] < r['ymax'] - r['ymin']:
            cv2.putText(img, str(index + 1), (int(r['xmin']), int(r['ymin']) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)
            result[index]["card"] = [{"name":c[1], "image":c[2]} for c in classificate_card(crop_card)]
        else:
            result[index]["card"] = [{"name": "no card", "image": "blank.jpg"}]
            
    cv2.imwrite(f"./images/{file_name}", img)
    # print(result)
    return result

def detect_card_filebyte(file):
    model = torch.hub.load('yolo/', 'custom', path='yolo/best.pt', source='local', skip_validation=True)
    im = Image.open(io.BytesIO(file)).convert("RGB")
    results = model(im, size=640)
    
    nparr = np.fromstring(file, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    pre_result = results.pandas().xyxy[0].to_dict(orient="records")
    
    result = sorted(pre_result, key=lambda l:l["xmin"])
    
    for index, r in enumerate(result):
        crop_card = img[int(r['ymin']):int(r['ymax']),
                        int(r['xmin']):int(r['xmax'])]
        
        result[index]["card"] = [{"name":c[1], "image":c[2]} for c in classificate_card(crop_card)]
        
    return result