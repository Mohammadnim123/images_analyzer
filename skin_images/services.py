import torchvision
import torch
import torchvision.transforms as transforms
from PIL import Image


class SkinImagesAnalyzerService:

    classes = ['Bug Bites',
    'Drug Reactions and Allergic Conditions',
    'Hair and Nail Disorders',
    'Infectious Diseases',
    'Inflammatory and Autoimmune Diseases',
    'Neoplastic Diseases (Tumors and Cancers)',
    'Pigmentation and Light Disorders',
    'Systemic and Other Diseases']

    mean = [0.5462, 0.4187, 0.3856]
    std = [0.1858, 0.1591, 0.1534]
    img_dim = (224,224)

    image_transforms = transforms.Compose([
        transforms.Resize(img_dim),    
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x / 255.0)
    ])

    densenet_model = torch.load("skin_images/densenet_201k.pth")

    @classmethod
    def analyze_image(cls, image):
        pil_image = Image.open(image)
        description = cls.classify (cls.densenet_model, cls.image_transforms, pil_image, cls.classes)
        return description

    @classmethod
    def classify (cls,model,image_transforms,pil_image,classes):
        model = model.eval()
        image = image_transforms(pil_image).float()
        image = image.unsqueeze(0)
        output = model(image)
        _, predicted = torch.max(output.data,1)
        return classes[predicted.item()]
