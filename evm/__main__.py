import argparse
import os

from evm import gaussian_evm, gaussian_kernel, laplacian_evm, loadVideo, saveVideo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Eulerian Video Magnification for colors and motions magnification"
    )

    parser.add_argument(
        "--video_path",
        "-v",
        type=str,
        help="Path to the video to be used",
        required=True,
    )

    parser.add_argument(
        "--level",
        "-l",
        type=int,
        help="Number of level of the Gaussian/Laplacian Pyramid",
        required=False,
        default=4,
    )

    parser.add_argument(
        "--alpha",
        "-a",
        type=int,
        help="Amplification factor",
        required=False,
        default=100,
    )

    parser.add_argument(
        "--lambda_cutoff",
        "-lc",
        type=int,
        help="λ cutoff for Laplacian EVM",
        required=False,
        default=1000,
    )

    parser.add_argument(
        "--low_omega",
        "-lo",
        type=float,
        help="Minimum allowed frequency",
        required=False,
        default=0.833,
    )

    parser.add_argument(
        "--high_omega",
        "-ho",
        type=float,
        help="Maximum allowed frequency",
        required=False,
        default=1,
    )

    parser.add_argument(
        "--saving_path",
        "-s",
        type=str,
        help="Saving path of the magnified video",
        required=True,
    )

    parser.add_argument(
        "--mode",
        "-m",
        type=str,
        help="Type of pyramids to use (gaussian or laplacian)",
        choices=["gaussian", "laplacian"],
        required=False,
        default="gaussian",
    )

    parser.add_argument(
        "--attenuation",
        "-at",
        type=float,
        help="Attenuation factor for I and Q channel post filtering",
        required=False,
        default=1,
    )

    args = parser.parse_args()
    kwargs = {}
    kwargs["kernel"] = gaussian_kernel
    kwargs["level"] = args.level
    kwargs["alpha"] = args.alpha
    kwargs["freq_range"] = [args.low_omega, args.high_omega]
    kwargs["attenuation"] = args.attenuation
    mode = args.mode
    video_path = args.video_path

    assert os.path.exists(video_path), f"Video {video_path} not found :("

    images, fps = loadVideo(video_path=video_path)
    kwargs["images"] = images
    kwargs["fps"] = fps

    if mode == "gaussian":
        output_video = gaussian_evm(**kwargs)
    else:
        kwargs["lambda_cutoff"] = args.lambda_cutoff
        output_video = laplacian_evm(**kwargs)

    saveVideo(video=output_video, saving_path=args.saving_path, fps=fps)
