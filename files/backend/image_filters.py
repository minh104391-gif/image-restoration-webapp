import cv2
import numpy as np
from scipy import signal
from skimage.restoration import denoise_nl_means, denoise_tv_chambolle

def apply_bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """
    Apply Bilateral Filter for edge-preserving smoothing
    
    Args:
        image: Input image (BGR)
        d: Diameter of pixel neighborhood
        sigma_color: Filter sigma in the color space
        sigma_space: Filter sigma in the coordinate space
    
    Returns:
        Filtered image
    """
    result = cv2.bilateralFilter(image, d, sigma_color, sigma_space)
    return result

def apply_nlm_filter(image, h=10, patch_size=5, patch_distance=7):
    """
    Apply Non-Local Means (NLM) denoising
    
    Args:
        image: Input image (BGR)
        h: Filter strength. Higher h value removes more noise but removes details too
        patch_size: Size of patches (should be odd)
        patch_distance: Maximum distance to search for patches
    
    Returns:
        Filtered image
    """
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Apply NLM
    result_rgb = denoise_nl_means(
        image_rgb,
        h=h,
        fast_mode=True,
        patch_size=patch_size,
        patch_distance=patch_distance,
        channel_axis=2
    )
    
    # Convert back to BGR
    result = cv2.cvtColor((result_rgb * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    return result

def apply_wiener_filter(image, noise_variance=None):
    """
    Apply Wiener Filter in frequency domain
    
    Args:
        image: Input image (BGR)
        noise_variance: Estimated noise variance
    
    Returns:
        Filtered image
    """
    result = image.copy()
    
    for i in range(3):  # Apply to each channel
        # Convert to grayscale channel
        channel = image[:, :, i].astype(np.float64)
        
        # Estimate local mean
        local_mean = cv2.blur(channel, (5, 5))
        
        # Estimate local variance
        local_sq_mean = cv2.blur(channel ** 2, (5, 5))
        local_variance = np.maximum(local_sq_mean - local_mean ** 2, 0)
        
        # Estimate noise variance if not provided
        if noise_variance is None:
            noise_var = np.mean(local_variance) * 0.1
        else:
            noise_var = noise_variance
        
        # Apply Wiener filter
        wiener_result = local_mean + np.maximum(
            local_variance - noise_var, 0
        ) / np.maximum(local_variance, 1e-10) * (channel - local_mean)
        
        result[:, :, i] = np.clip(wiener_result, 0, 255).astype(np.uint8)
    
    return result

def apply_notch_filter(image, center_x=None, center_y=None, radius=10):
    """
    Apply Optimum Notch Filter to remove periodic noise
    
    Args:
        image: Input image (BGR)
        center_x: X coordinate of notch center (frequency domain)
        center_y: Y coordinate of notch center (frequency domain)
        radius: Radius of notch
    
    Returns:
        Filtered image
    """
    result = image.copy()
    
    for i in range(3):  # Apply to each channel
        channel = image[:, :, i].astype(np.float32)
        
        # FFT
        f_transform = np.fft.fft2(channel)
        f_shift = np.fft.fftshift(f_transform)
        
        # Create notch filter mask
        rows, cols = channel.shape
        if center_x is None:
            center_x = rows // 2
        if center_y is None:
            center_y = cols // 2
        
        # Create Gaussian notch filter
        u = np.arange(rows)
        v = np.arange(cols)
        u, v = np.meshgrid(u, v, indexing='ij')
        
        # Distance from center
        d = np.sqrt((u - center_x) ** 2 + (v - center_y) ** 2)
        
        # Notch filter (suppress frequencies near center)
        notch_filter = 1 - np.exp(-(d ** 2) / (2 * radius ** 2))
        
        # Apply filter
        f_filtered = f_shift * notch_filter
        
        # Inverse FFT
        f_ishift = np.fft.ifftshift(f_filtered)
        filtered_channel = np.fft.ifft2(f_ishift)
        filtered_channel = np.abs(filtered_channel)
        
        result[:, :, i] = np.clip(filtered_channel, 0, 255).astype(np.uint8)
    
    return result