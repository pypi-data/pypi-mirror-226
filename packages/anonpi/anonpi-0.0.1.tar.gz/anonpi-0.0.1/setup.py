from setuptools import setup, find_packages




long_description = """
# anonpi: Python Module for Calling Systems

The "anonpi" module is a powerful Python package that provides a convenient interface for interacting with calling systems. It simplifies the development of applications that require functionalities such as machine detection, IVR (Interactive Voice Response), DTMF (Dual-Tone Multi-Frequency) handling, recording, playback, and more.

## Key Features

- **Machine Detection:** Easily detect whether a call is being answered by a human or an automated system, enabling intelligent call handling and routing.

- **IVR Support:** Build interactive voice response systems by creating menus, prompts, and collecting user input through voice or DTMF tones.

- **DTMF Handling:** Efficiently capture and process DTMF tones (telephone keypad input) during calls for user interaction, menu navigation, and decision-making.

- **Call Recording:** Seamlessly record incoming or outgoing calls, enabling compliance with legal requirements, quality monitoring, and archiving for later analysis.

- **Playback Functionality:** Retrieve and play back pre-recorded audio files during calls, enhancing the user experience and providing personalized content.

- **Call Control:** Take control of call initiation, termination, and manipulation, allowing for call transfers, forwarding, muting, and more.

## Usage

The "anonpi" module provides a clean and intuitive API, making it easy to integrate calling functionalities into your Python applications. Here's an example of how you can use the module to perform machine detection during a call:

```python
import anonpi

print("Soon")

```
"""


setup(
    name='anonpi',
    version='0.0.1',
    author='Adistar',
    author_email='adityasamalllll6@gmail.com',
    description='The "anonpi" module is a powerful Python package that provides a convenient interface for interacting with calling systems. It simplifies the development of applications that require functionalities such as machine detection, IVR (Interactive Voice Response), DTMF (Dual-Tone Multi-Frequency) handling, recording, playback, and more',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests','flask','colorama'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT'
)