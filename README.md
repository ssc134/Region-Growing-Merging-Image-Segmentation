# Region-Growing-Merging-Image-Segmentation

v2.py:
  Using flood_fill algo, a pixel is merged/filled if it's intensity value is lies near the mean of intensities of all merged pixels.
  An error variable is used. If a pixel intensity lies in te range [mean-error, mean+error], it's included.
