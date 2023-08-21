from setuptools import setup, find_packages

setup(
    name='skylark_video_processor',
    version='0.1',
    description='A video processing packageg fop YOLOV8',
    author='Prem Varma',
    author_email='prem.varma@skylarklabs.ai',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'ultralytics',
    ],
)
