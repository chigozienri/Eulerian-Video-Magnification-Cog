# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

import subprocess
import tempfile

from cog import BasePredictor, Input, Path

from evm import gaussian_evm, gaussian_kernel, laplacian_evm, loadVideo, saveVideo


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        video: Path = Input(description="Input video"),
        level: int = Input(
            description="Number of level of the Gaussian/Laplacian Pyramid", default=4
        ),
        alpha: int = Input(description="Amplification factor", default=100),
        lambda_cutoff: int = Input(
            description="λ cutoff for Laplacian EVM", default=1000
        ),
        low_omega: float = Input(
            description="Minimum allowed frequency", default=0.833
        ),
        high_omega: float = Input(description="Maximum allowed frequency", default=1),
        gaussian_mode: bool = Input(
            description="Gaussian mode if true, or Laplacian mode if false",
            default=True,
        ),
        attenuation: float = Input(
            description="Attenuation factor for I and Q channel post filtering",
            default=1,
        ),
    ) -> Path:
        """Run a single prediction on the model"""

        kwargs = {}
        kwargs["kernel"] = gaussian_kernel
        kwargs["level"] = level
        kwargs["alpha"] = alpha
        kwargs["freq_range"] = [low_omega, high_omega]
        kwargs["attenuation"] = attenuation

        images, fps = loadVideo(video_path=str(video))
        kwargs["images"] = images
        kwargs["fps"] = fps
        if gaussian_mode:
            output_video = gaussian_evm(**kwargs)
        else:
            kwargs["lambda_cutoff"] = lambda_cutoff
            output_video = laplacian_evm(**kwargs)

        saving_path = "output.avi"
        saveVideo(video=output_video, saving_path=str(saving_path), fps=fps)

        # To output `cog.Path` objects the file needs to exist, so create a temporary file first.
        # This file will automatically be deleted by Cog after it has been returned.
        mp4_path = Path(tempfile.mkdtemp()) / "output.mp4"

        # Convert to mp4
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            saving_path,
            "-c:v",
            "libx264",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-strict",
            "-2",
            mp4_path,
        ]

        # Execute the command
        subprocess.call(ffmpeg_command)

        return Path(mp4_path)
