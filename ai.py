import cv2
import torch
import pickle
import cv2

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

def detect_card():
    model = torch.hub.load('yolo', 'custom', path='yolo/best.pt', source='local', skip_validation=True)
    im = 'images/source.jpg'
    results = model(im, size=640)
    
    img = cv2.imread(im)
    pre_result = results.pandas().xyxy[0].to_dict(orient="records")
    
    result = sorted(pre_result, key=lambda l:l["xmin"])
    
    for index, r in enumerate(result):
        crop_card = img[int(r['ymin']):int(r['ymax']),
                        int(r['xmin']):int(r['xmax'])]
        
        result[index]["card"] = [{"name":c[1], "image":c[2]} for c in classificate_card(crop_card)]

    return result