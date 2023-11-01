from PIL import Image
from model import FruitsClassifier
import torchvision.transforms as transforms
import torch
import os
import glob

script_dir = os.path.dirname(os.path.abspath(__file__))
#upload_dir = os.path.join(script_dir, 'uploads')
upload_dir = '/Users/roudykaram/Desktop/jsmrecipes/uploads'

#print(f"Chemin absolu du répertoire 'uploads' : {upload_dir}")

# Initialisation de la variable image_file
image_file = None

# Recherchez la dernière image dans le répertoire 'uploads'
image_files = glob.glob(os.path.join(upload_dir, '*.jpeg'))
if image_files:
    # Triez les fichiers par date de modification (le plus récent en premier)
    image_files.sort(key=os.path.getmtime, reverse=True)

    # Prenez la première image (la plus récente)
    image_file = image_files[0]


if image_file:
    # Load the image using the constructed path
    image = Image.open(image_file)

    # Transformations pour le prétraitement des images
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Appliquez les transformations à l'image
    input_image = transform(image).unsqueeze(0)  # Vous devez également ajouter une dimension de lot (batch) car le modèle s'attend à un lot.

    # Chargez le modèle pré-entraîné
    # Specify the image file name
    image_fil = 'fruits_classifier.pth'

    # Construct the full path to the image file
    image_pat = os.path.join(script_dir, image_fil)
    model_checkpoint = image_pat #'training/fruits_classifier.pth'
    model = FruitsClassifier(num_classes=3)  # Assurez-vous d'utiliser les mêmes paramètres que lors de l'entraînement
    model.load_state_dict(torch.load(model_checkpoint))
    model.eval()


    # Faites la prédiction
    with torch.no_grad():
        outputs = model(input_image)
        _, predicted = torch.max(outputs, 1)

    # Interprétez les prédictions pour les 3 classes

    if predicted.item() == 0:
            print("L'image représente une pomme.")
    elif predicted.item() == 1:
            print("L'image représente du chocolat.")
    else:
            print("L'image représente une prune.")
else:
    print("Aucune image trouvée dans le répertoire 'uploads'.")