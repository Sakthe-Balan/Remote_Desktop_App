# Screen Sharing using Python

A Python-based screen sharing application that allows users to share their screens across different devices. The application uses OpenCV and MSS libraries to capture and display screenshots.

## Requirements

* Python 3.x
* OpenCV
* MSS

## Installation

1. Clone the repository: `git clone https://github.com/your-username/screen-sharing.git`
2. Install the required packages: `pip install -r requirements.txt`

## Usage

1. Run the server on the device that you want to share the screen from: `python server.py`
2. Run the client on the device that you want to view the shared screen on: `python client.py <server-ip-address>`
3. The shared screen will be displayed on the client device in real-time.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* [OpenCV](https://opencv.org/)
* [MSS](https://github.com/BoboTiG/python-mss)
* [Python Socket Programming Tutorial](https://realpython.com/python-sockets/)

Feel free to contribute to the project or report any issues you encounter.
