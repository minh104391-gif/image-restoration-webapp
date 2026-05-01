import numpy as np
import cv2

def add_gaussian_noise(image, std_dev=0.1):
    """
    Add Gaussian noise to image
    
    Args:
        image: Input image (normalized to [0, 1])
        std_dev: Standard deviation of Gaussian noise
    
    Returns:
        Image with added Gaussian noise
    """
    noise = np.random.normal(0, std_dev, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 1)

def add_salt_pepper_noise(image, probability=0.1):
    """
    Add Salt and Pepper noise to image
    
    Args:
        image: Input image (normalized to [0, 1])
        probability: Probability of noise occurrence
    
    Returns:
        Image with added Salt & Pepper noise
    """
    noisy_image = image.copy()
    num_pixels = image.size
    num_salt = int(num_pixels * probability / 2)
    num_pepper = int(num_pixels * probability / 2)
    
    # Add salt (white noise)
    salt_coords = np.random.choice(num_pixels, num_salt, replace=False)
    noisy_image.flat[salt_coords] = 1
    
    # Add pepper (black noise)
    pepper_coords = np.random.choice(num_pixels, num_pepper, replace=False)
    noisy_image.flat[pepper_coords] = 0
    
    return np.clip(noisy_image, 0, 1)

def add_periodic_noise(image, amplitude=0.1, frequency=0.05):
    """
    Add periodic/sinusoidal noise to image
    
    Args:
        image: Input image (normalized to [0, 1])
        amplitude: Amplitude of periodic noise
        frequency: Frequency of periodic noise
    
    Returns:
        Image with added periodic noise
    """
    rows, cols = image.shape[:2]
    u = np.arange(cols)
    v = np.arange(rows)
    u, v = np.meshgrid(u, v, indexing='ij')
    
    # Generate sinusoidal pattern
    periodic_pattern = amplitude * np.sin(2 * np.pi * frequency * u) * np.sin(2 * np.pi * frequency * v)
    
    # Add to image
    noisy_image = image + periodic_pattern
    return np.clip(noisy_image, 0, 1)

def remove_gaussian_noise(image, method='bilateral', **kwargs):
    """Remove Gaussian noise using specified method"""
    if method == 'bilateral':
        return cv2.bilateralFilter(image, 9, 75, 75)
    elif method == 'gaussian_blur':
        return cv2.GaussianBlur(image, (5, 5), 0)
    else:
        return image

def remove_salt_pepper_noise(image, method='median', **kwargs):
    """Remove Salt & Pepper noise using median filter"""
    if method == 'median':
        return cv2.medianBlur(image, 5)
    elif method == 'morphological':
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    else:
        return image