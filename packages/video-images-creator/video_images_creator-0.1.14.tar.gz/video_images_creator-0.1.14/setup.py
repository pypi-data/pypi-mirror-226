from setuptools import setup

setup(
    name='video_images_creator',
    version='0.1.14',
    description=(
    "Create videos from images using the 'video_images_creator' package. "
    "Easily generate dynamic videos for your project by following these steps:\n\n"
    "1. Install the package using pip:\n"
    "   $ pip install video_images_creator\n\n"
    "2. Import the 'video_creator' module and customize the images and feature names:\n"
    "   ```python\n"
    "   from video_images_creator import video_creator\n"
    "   feature_names = ['Splash Screen', 'Search']\n"
    "   image_urls = [\n"
    "       'URL_to_image_1',\n"
    "       'URL_to_image_2'\n"
    "   ]\n"
    "   video_creator.build(image_urls, feature_names)\n"
    "   ```\n\n"
    "3. Run your Python script to create the video inside the 'outputs' folder.\n"
),
    url='',
    author='Nikhil Sharma',
    author_email='nikhilsharma972@gmail.com',
    license='BSD 2-clause',
    packages=['video_images_creator'],
    package_dir={"": "src"},
    package_data={"video_images_creator": ["*.ttf"]},
    install_requires=['opencv-python', 'numpy', 'pillow'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)


