#  Copyright 2021 Rikai Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import filecmp
from binascii import b2a_base64
from io import BytesIO

import numpy as np
import pytest
from PIL import Image as PILImage

from rikai.types.vision import Image


def test_show_embedded_png(tmp_path):
    data = np.random.random((100, 100))
    rescaled = (255.0 / data.max() * (data - data.min())).astype(np.uint8)
    im = PILImage.fromarray(rescaled)
    uri = tmp_path / "test.png"
    im.save(uri)
    result = Image(uri)._repr_png_()
    with open(uri, "rb") as fh:
        expected = b2a_base64(fh.read()).decode("ascii")
        assert result == expected

        fh.seek(0)
        embedded_image = Image(fh)
        assert result == embedded_image._repr_png_()


def test_show_embedded_jpeg(tmp_path):
    data = np.random.random((100, 100))
    rescaled = (255.0 / data.max() * (data - data.min())).astype(np.uint8)
    im = PILImage.fromarray(rescaled)
    uri = tmp_path / "test.jpg"
    im.save(uri)
    result = Image(uri)._repr_jpeg_()
    with open(uri, "rb") as fh:
        expected = b2a_base64(fh.read()).decode("ascii")
        assert result == expected

        fh.seek(0)
        embedded_image = Image(fh)
        assert result == embedded_image._repr_jpeg_()


def test_format_kwargs(tmp_path):
    data = np.random.random((100, 100))
    rescaled = (255.0 / data.max() * (data - data.min())).astype(np.uint8)
    result_uri = tmp_path / "result.jpg"
    Image.from_array(rescaled, result_uri, format="jpeg", optimize=True)

    expected_uri = tmp_path / "expected.jpg"
    PILImage.fromarray(rescaled).save(
        expected_uri, format="jpeg", optimize=True
    )

    assert filecmp.cmp(result_uri, expected_uri)

    result_uri = tmp_path / "result.png"
    Image.from_array(rescaled, result_uri, format="png", compress_level=1)

    expected_uri = tmp_path / "expected.png"
    PILImage.fromarray(rescaled).save(
        expected_uri, format="png", compress_level=1
    )
    assert filecmp.cmp(result_uri, expected_uri)


def test_embeded_image_from_bytesio():
    data = np.random.random((100, 100))
    rescaled = (255.0 / data.max() * (data - data.min())).astype(np.uint8)
    im = PILImage.fromarray(rescaled)
    buf = BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    image = Image(buf)
    assert np.array_equal(image.to_numpy(), rescaled)


@pytest.mark.timeout(30)
@pytest.mark.webtest
def test_show_remote_ref():
    from IPython.display import Image as IPyImage

    uri = "https://octodex.github.com/images/original.png"
    img = Image(uri)
    # TODO check the actual content
    assert img._repr_html_() == img.display()._repr_html_()
    assert img.display()._repr_html_() == IPyImage(uri)._repr_html_()
