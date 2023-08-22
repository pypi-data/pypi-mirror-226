# -*- coding: utf-8 -*-
import warnings
from .HTTPClient import HTTPClient


class ImageClient(HTTPClient):
    def __init__(self, headers=None):
        defaultHeaders = {
            "Content-Type": "application/json",
        }
        defaultHeaders.update(headers)
        super().__init__(headers=defaultHeaders)
        self.scheduler_ids = {
            "DDIMScheduler": 1,
            "DDPMScheduler": 2,
            "PNDMScheduler": 3,
            "LMSDiscreteScheduler": 4,
            "EulerDiscreteScheduler": 5,
            "HeunDiscreteScheduler": 6,
            "EulerAncestralDiscreteScheduler": 7,
            "DPMSolverMultistepScheduler": 8,
            "DPMSolverSinglestepScheduler": 9,
            "KDPM2DiscreteScheduler": 10,
            "KDPM2AncestralDiscreteScheduler": 11,
            "DEISMultistepScheduler": 12,
            "UniPCMultistepScheduler": 13,
        }

    def generate(self, prompt="", neg_prompt="", model_id=0, img_width=512, img_height=512, inference_steps=25,
                 guidance_scale=7, seed=-1, num_images=4, scheduler="EulerAncestralDiscreteScheduler"):
        if scheduler not in self.scheduler_ids:
            warnings.warn(f"The scheduler must be one of the follow schedulers {self.scheduler_ids.keys()}", Warning)

        data = {
            "guidance_scale": guidance_scale,
            "img_height": img_height,
            "img_width": img_width,
            "inference_steps": inference_steps,
            "model_id": model_id,
            "neg_prompt": neg_prompt,
            "num_images": num_images,
            "prompt": prompt,
            "scheduler": self.scheduler_ids.get(scheduler, 7),
            "seed": seed
        }

        response = self.post("/api/stableDiffusion", data)
        result = response["data"]
        return result

    def img2img(self, imgurl, strength=0.7, prompt="", neg_prompt="", model_id=0, img_width=512, img_height=512,
                inference_steps=25, guidance_scale=7, seed=-1, num_images=4,
                scheduler="EulerAncestralDiscreteScheduler"):
        if scheduler not in self.scheduler_ids:
            warnings.warn(f"The scheduler must be one of the follow schedulers {self.scheduler_ids.keys()}", Warning)

        data = {
            "oss_url": imgurl,
            "strength": strength,
            "guidance_scale": guidance_scale,
            "img_height": img_height,
            "img_width": img_width,
            "inference_steps": inference_steps,
            "model_id": model_id,
            "neg_prompt": neg_prompt,
            "num_images": num_images,
            "prompt": prompt,
            "scheduler": self.scheduler_ids.get(scheduler, 7),
            "seed": seed
        }

        response = self.post("/api/imgToimg", data)
        result = response["data"]
        return result
