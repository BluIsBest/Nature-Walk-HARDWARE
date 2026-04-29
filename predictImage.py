import sys
import json
import torch
from PIL import Image
from torchvision import transforms

MODEL_PATH = "./plant_model.pt"
CLASS_MAP_PATH = "./class_to_idx.json"
SPECIES_JSON_PATH = "./plantnet300K_species_names.json"
IMG_SIZE = 224


IMAGE_PATH = './test1.png'

# load model
model = torch.jit.load(MODEL_PATH, map_location="cpu")
model.eval()

# load mappings
with open(CLASS_MAP_PATH, "r") as f:
    class_to_idx = json.load(f)

idx_to_class = {int(v): k for k, v in class_to_idx.items()}

with open(SPECIES_JSON_PATH, "r") as f:
    species_map = json.load(f)

# image transform
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(IMG_SIZE),
    transforms.ToTensor()
])

# load image
img = Image.open(IMAGE_PATH).convert("RGB")
img = transform(img).unsqueeze(0)

# predict
with torch.no_grad():
    output = model(img)
    pred_idx = output.argmax(dim=1).item()

species_id = idx_to_class[pred_idx]
species_name = species_map[species_id]

print("Species ID:", species_id)
print("Species Name:", species_name)
