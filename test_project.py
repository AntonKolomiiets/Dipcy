import numpy as np
import cv2 as cv
from scipy.ndimage import gaussian_filter
import pytest
from project import Edit



######## Image with a linear gradient from black to white across one axis
@pytest.fixture
def sample_image():
    height, width = 100, 100
    image = np.zeros((height, width, 3), dtype=np.float32)
    for i in range(width):
        value = i / (width - 1)  
        image[:, i, :] = value  
    return image

########Brightness##########
@pytest.mark.parametrize("brightness_value", [0.1, 0.5, 1.0])
def test_brightness_parametrized(sample_image, brightness_value):
    
    expected_image = np.clip(sample_image + brightness_value, 0, 1)
    result_image = Edit.brightness(sample_image, brightness_value)
    np.testing.assert_array_almost_equal(result_image, expected_image)

########Log Shadows##########
@pytest.mark.parametrize("value, offset", [
    (0.5, 0.333),  # default offset
    (0.5, 0.5),    
    (0.5, 0.1)     
])
def test_log_shadows(sample_image, value, offset):
    steepness = 10
    sigmoid_function = lambda x: 1 / (1 + np.exp(-x * steepness))
    sigmoid_mask = sigmoid_function((sample_image - offset) * 10)
    shadows_adjustment = (offset - (offset - sample_image) * value)
    expected_image = ((1 - sigmoid_mask) * shadows_adjustment) + (sigmoid_mask * sample_image)
    expected_image = np.clip(expected_image, 0, 1)
    result_image = Edit.log_shadows(sample_image, value, offset)

    np.testing.assert_array_almost_equal(result_image, expected_image)

########Gain##########
@pytest.mark.parametrize("gain_value", [0.5, 1.0, 1.5])
def test_gain(sample_image, gain_value):
    expected_image = sample_image * (1 + gain_value * (1 - sample_image))
    expected_image = np.clip(expected_image, 0, 1)
    result_image = Edit.gain(sample_image, gain_value)
    np.testing.assert_array_almost_equal(result_image, expected_image)

########Saturation##########
@pytest.mark.parametrize("saturation_value", [0.5, 1.0, 1.5])
def test_saturation(sample_image, saturation_value):
    hsv_image = cv.cvtColor(sample_image, cv.COLOR_BGR2HSV).astype(np.float32)
    hsv_image[:, :, 1] *= saturation_value
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 1)
    expected_image = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
    result_image = Edit.saturation(sample_image, saturation_value)
    np.testing.assert_array_almost_equal(result_image, expected_image)

########Offset##########
@pytest.mark.parametrize("blue, green, red", [
    (0.1, 0.1, 0.1), 
    (0.5, -0.5, 0.0),  
    (-0.1, 0.0, 0.1)   
])
def test_offset(sample_image, blue, green, red):
    image_adjusted = sample_image.copy()
    image_adjusted[:, :, 0] += blue
    image_adjusted[:, :, 1] += green
    image_adjusted[:, :, 2] += red
    expected_image = np.clip(image_adjusted, 0, 1)
    result_image = Edit.offset(sample_image, blue, green, red)
    np.testing.assert_array_almost_equal(result_image, expected_image)