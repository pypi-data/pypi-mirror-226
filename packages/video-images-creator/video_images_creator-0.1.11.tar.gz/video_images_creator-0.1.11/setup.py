from setuptools import setup

setup(
    name='video_images_creator',
    version='0.1.11',
    description='A example Python package',
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