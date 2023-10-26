from .gaussian_pyramid import filterGaussianPyramids, getGaussianPyramids
from .laplacian_pyramid import filterLaplacianPyramids, getLaplacianPyramids
from .processing import (getGaussianOutputVideo, getLaplacianOutputVideo,
                        loadVideo, saveVideo)


def gaussian_evm(images,
                 fps,
                 kernel,
                 level,
                 alpha,
                 freq_range,
                 attenuation):

    gaussian_pyramids = getGaussianPyramids(
                            images=images,
                            kernel=kernel,
                            level=level
                    )

    print("Gaussian Pyramids Filtering...")
    filtered_pyramids = filterGaussianPyramids(
                            pyramids=gaussian_pyramids,
                            fps=fps,
                            freq_range=freq_range,
                            alpha=alpha,
                            attenuation=attenuation
                        )
    print("Finished!")

    output_video = getGaussianOutputVideo(
                        original_images=images,
                        filtered_images=filtered_pyramids
                )

    return output_video


def laplacian_evm(images,
                  fps,
                  kernel,
                  level,
                  alpha,
                  lambda_cutoff,
                  freq_range,
                  attenuation):

    laplacian_pyramids = getLaplacianPyramids(
                                images=images,
                                kernel=kernel,
                                level=level
                    )

    filtered_pyramids = filterLaplacianPyramids(
                            pyramids=laplacian_pyramids,
                            fps=fps,
                            freq_range=freq_range,
                            alpha=alpha,
                            attenuation=attenuation,
                            lambda_cutoff=lambda_cutoff,
                            level=level
                    )

    output_video = getLaplacianOutputVideo(
                            original_images=images,
                            filtered_images=filtered_pyramids,
                            kernel=kernel
                )

    return output_video
