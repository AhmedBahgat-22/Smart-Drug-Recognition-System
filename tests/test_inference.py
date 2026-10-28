import unittest
import numpy as np
from PIL import Image
from interface.inference import preprocess_image, decode_prediction

class InferenceTests(unittest.TestCase):
    def test_preprocessing_shape_and_range(self):
        array = preprocess_image(Image.new("RGB", (32, 48), (20, 100, 180)))
        self.assertEqual(array.shape, (1, 224, 224, 3))
        self.assertEqual(array.dtype, np.float32)
        np.testing.assert_allclose(array[0, 0, 0], [20, 100, 180], rtol=0, atol=1)

    def test_rgba_image(self):
        array = preprocess_image(Image.new("RGBA", (20, 20), (12, 30, 50, 255)))
        self.assertEqual(array.shape[-1], 3)

    def test_class_order(self):
        self.assertEqual(decode_prediction(0.9)["label"], "Original")
        self.assertEqual(decode_prediction(0.1)["label"], "Counterfeit")
        self.assertEqual(decode_prediction(0.5)["label"], "Original")

    def test_reject_invalid_score(self):
        for value in (-0.1, 1.1, float('nan')):
            with self.assertRaises(ValueError):
                decode_prediction(value)

if __name__ == "__main__":
    unittest.main()
