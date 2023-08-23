from setuptools import setup

setup(
    name='video_images_creator',
    version='0.1.12',
    description="Steps/n1. Install package using pip/n2. Copy below, you can change image_urls and feature_names as per you like from video_images_creator import video_creator\nfeature_names = ['Splash Screen', 'Search']\nimage_urls = ['https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/feature_figma/image/485/b478c7bd-84f8-48f2-81c7-3b9a5dbe7960.png', 'https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/feature_figma/image/485/b478c7bd-84f8-48f2-81c7-3b9a5dbe7960.png']\nvideo_creator.build(image_urls, feature_names)\n3.Run your python and see video inside outputs folder",
    url='',
    author='Nikhil Sharma',
    author_email='nikhilsharma972@gmail.com',
    license='BSD 2-clause',
    packages=['video_images_creator'],
    package_dir={"": "src"},
    package_data={"video_images_creator": ["*.ttf"]},
    install_requires=['opencv-python', 'numpy', 'pillow'],
    classifiers=[]
)


