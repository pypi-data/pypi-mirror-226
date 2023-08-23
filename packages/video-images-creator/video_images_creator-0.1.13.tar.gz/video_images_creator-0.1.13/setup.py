from setuptools import setup

setup(
    name='video_images_creator',
    version='0.1.13',
    description=(
        "Steps:\n"
        "1. Install the package using pip.\n"
        "2. Copy the following code. You can change image_urls and feature_names as per your preferences.\n"
        "from video_images_creator import video_creator\n"
        "feature_names = ['Splash Screen', 'Search']\n"
        "image_urls = [\n"
        "    'https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/feature_figma/image/485/b478c7bd-84f8-48f2-81c7-3b9a5dbe7960.png',\n"
        "    'https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/feature_figma/image/485/b478c7bd-84f8-48f2-81c7-3b9a5dbe7960.png'\n"
        "]\n"
        "video_creator.build(image_urls, feature_names)\n"
        "3. Run your Python script and see the video inside the 'outputs' folder."
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


