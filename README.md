
## Modules

### CameraHandler

This module handles camera operations, including face detection using the Haar Cascade classifier.

- `check.py`: Script to check camera functionality.
- `haarcascade_frontalface_default.xml`: XML file for face detection.
- `oneM2Mget.py`: Script for oneM2M communication.
- `Speak.py`: Script for text-to-speech functionality.
- `update_main1.py`: Main script for updating camera data.

### Display

This module manages the display of data and the graphical user interface.

- `getdata.py`: Script to fetch data for display.
- `serviceRunner.py`: Script to run display services.
- `updated_gui.py`: Main GUI script.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```sh
    cd smartpole
    ```

3. Install the required dependencies for each module:
    ```sh
    pip install -r CameraHandler/requirements.txt
    pip install -r Display/requirement.txt
    ```

## Usage

1. Run the camera handler:
    ```sh
    python CameraHandler/update_main1.py
    ```

2. Run the display module:
    ```sh
    python Display/serviceRunner.py
    ```

## License

This project is licensed under the Intel License Agreement for Open Source Computer Vision Library. See the haarcascade_frontalface_default.xml file for details.