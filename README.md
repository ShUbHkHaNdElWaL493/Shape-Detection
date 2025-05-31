# Shape Detection

**Shape Detection** is a project aimed at identifying and classifying various geometric shapes within images using computer vision techniques and data science practices.

## Features

- Detects common geometric shapes: circles, squares and triangles.
- Utilizes computer vision algorithms for accurate corner detection and Hu moment detection.
- Modular code structure for easy maintenance and scalability.

## Technologies Used

- **C++**
- **CMake**
- **OpenCV**
- **Python**
- **ROS Noetic**

## Getting Started

### Prerequisites

- C++ compiler supporting C++11 or higher
- CMake
- OpenCV library
- Python 3.x
- ROS Noetic
- Dataset Link: https://www.kaggle.com/datasets/smeschke/four-shapes

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShUbHkHaNdElWaL493/Shape-Detection.git
   cd Shape-Detection
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Download and extract the dataset in model and rename the folder as 'dataset':
   ```bash
   cd model
   ls # The dataset folder should be here
   ```

### Usage

1. Train the model using Euclidean Distance Classifier and test it:
   ```bash
   python3 train.py
   python3 test.py
   ```

2. Copy the 'mean.csv' file inside the 'Implementation' folder:
   ```bash
   cp mean.csv ../Implementation/src/image_processor/include
   ```

2. Run the project using the 'launch.sh' bash script:
   ```bash
   cd ../Implementation
   ./launch.sh
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.