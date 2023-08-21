import numpy as np
import torch

from PIL import Image
from diffusers import AutoencoderKL, UNet2DConditionModel
from diffusers.schedulers import KarrasDiffusionSchedulers
from tqdm.auto import tqdm
from transformers import CLIPTextModel, CLIPTokenizer
from typing import Any, List, Optional, Union

from stablefused.diffusion import BaseDiffusion


class TextToVideoDiffusion(BaseDiffusion):
    def __init__(
        self,
        model_id: str = None,
        tokenizer: CLIPTokenizer = None,
        text_encoder: CLIPTextModel = None,
        vae: AutoencoderKL = None,
        unet: UNet2DConditionModel = None,
        scheduler: KarrasDiffusionSchedulers = None,
        torch_dtype: torch.dtype = torch.float32,
        device="cuda",
        *args,
        **kwargs
    ) -> None:
        super().__init__(
            model_id=model_id,
            tokenizer=tokenizer,
            text_encoder=text_encoder,
            vae=vae,
            unet=unet,
            scheduler=scheduler,
            torch_dtype=torch_dtype,
            device=device,
            *args,
            **kwargs
        )

    def embedding_to_latent(
        self,
        embedding: torch.FloatTensor,
        video_height: int,
        video_width: int,
        video_frames: int,
        num_inference_steps: int,
        guidance_scale: float,
        guidance_rescale: float,
        latent: Optional[torch.FloatTensor] = None,
    ) -> Union[torch.FloatTensor, List[torch.FloatTensor]]:
        if latent is None:
            shape = (
                embedding.shape[0] // 2,
                self.unet.config.in_channels,
                video_frames,
                video_height // self.vae_scale_factor,
                video_width // self.vae_scale_factor,
            )
            latent = self.random_tensor(shape)

        self.scheduler.set_timesteps(num_inference_steps)
        timesteps = self.scheduler.timesteps

        latent = latent * self.scheduler.init_noise_sigma

        for i, timestep in tqdm(list(enumerate(timesteps))):
            latent_model_input = torch.cat([latent] * 2)
            latent_model_input = self.scheduler.scale_model_input(
                latent_model_input, timestep
            )

            noise_prediction = self.unet(
                latent_model_input,
                timestep,
                encoder_hidden_states=embedding,
                return_dict=False,
            )[0]

            noise_prediction = self.classifier_free_guidance(
                noise_prediction, guidance_scale, guidance_rescale
            )

            latent = self.scheduler.step(
                noise_prediction, timestep, latent, return_dict=False
            )[0]

        return latent

    def resolve_output(
        self,
        latent: torch.FloatTensor,
        output_type: str,
    ) -> Union[torch.Tensor, np.ndarray, List[Image.Image]]:
        if output_type not in ["latent", "pt", "np", "pil"]:
            raise ValueError(
                "`output_type` must be one of [`latent`, `pt`, `np`, `pil`]"
            )

        if output_type == "latent":
            return latent

        # latent.shape => B, C, F, H, W
        latent = latent.permute(0, 2, 1, 3, 4)
        # latent.shape => B, F, C, H, W
        video = []
        for i in tqdm(range(latent.shape[0])):
            video.append(self.latent_to_image(latent[i : i + 1]))
        video = torch.cat(video, dim=0)
        return video

    @torch.no_grad()
    def __call__(
        self,
        prompt: Union[str, List[str]],
        video_height: int = 512,
        video_width: int = 512,
        video_frames: int = 24,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        guidance_rescale: float = 0.7,
        negative_prompt: Optional[Union[str, List[str]]] = None,
        latent: Optional[torch.FloatTensor] = None,
        output_type: str = "pil",
    ) -> Union[torch.Tensor, np.ndarray, List[Image.Image]]:
        self.validate_input(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image_height=video_height,
            image_width=video_width,
            num_inference_steps=num_inference_steps,
        )
        embedding = self.prompt_to_embedding(
            prompt=prompt,
            negative_prompt=negative_prompt,
        )
        latent = self.embedding_to_latent(
            embedding=embedding,
            video_height=video_height,
            video_width=video_width,
            video_frames=video_frames,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            guidance_rescale=guidance_rescale,
            latent=latent,
        )

        return self.resolve_output(
            latent=latent,
            output_type=output_type,
        )

    generate = __call__
