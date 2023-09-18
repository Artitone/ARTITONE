import logging
import ssl

import clip
import numpy as np
import torch

ssl._create_default_https_context = ssl._create_unverified_context
logger = logging.getLogger("artitone_CLIP")

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

materials = [
    "wood",
    "plastic",
    "metal",
    "leather",
    "silk",
    "paper",
    "glass",
    "rubber",
    "stone",
    "ceramic",
    "fabric",
    "wool",
    "cotton",
]
materials_text = clip.tokenize(materials).to(device)

texture_dict = {
    "Matte": ["wool", "fabric", "cotton", "leather", "paper"],
    "Rough": ["stone", "metal", "wood"],
    "Satin": ["ceramic", "glass", "plastic", "silk", "rubber"],
}

tags = [
    "modern",
    "scandinavian",
    "minimalist",
    "bohemian",
    "industrial",
    "contemporary",
    "asian",
    "boho chic",
    "coastal",
    "eclectic",
    "french",
    "mediterranean",
    "mid-century",
    "modern farmhouse",
    "moroccan",
    "rustic",
    "scandiboho",
    "shabby chic",
    "traditional",
    "vintage",
]
tags_text = clip.tokenize(tags).to(device)


def clip_predict_label(image):
    img = image.copy()
    im = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        model.encode_image(im)
        model.encode_text(materials_text)
        model.encode_text(tags_text)

        logits_per_image, _ = model(im, materials_text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        max_idx = probs.argmax()
        max_item = materials[max_idx]
        for texture, mat_list in texture_dict.items():
            if max_item in mat_list:
                max_text = texture
                break

        logger.debug(
            f"Label probs: {probs}\n Most likely material: {max_item}\n Most likely texture: {max_text}"
        )

        logits_per_image, _ = model(im, tags_text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        max_idx = np.argpartition(probs[0], -3)[-3:]
        max_tags = []
        for idx in max_idx:
            max_tags.append(tags[idx])

        logger.debug(f"Label probs: {probs}\n Most likely tags: {max_tags}")
        return max_text, max_tags
