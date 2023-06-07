## AI Attendance Monitor

AI Attendance Monitor is a cost-efficient AI-powered attendance monitoring system developed using Python Flask. The project utilizes OpenCV-Python, Geocoder, and Geopy libraries to provide a convenient solution for attendance tracking based on face recognition and location verification.

**Features**
Face recognition: The system uses face recognition algorithms to compare captured faces with the reference photos in the attendanceResources folder. If a match is found, an attendance record is created with a corresponding timestamp.
Geo-tagging: Before running the Flask app, you need to generate a geo tag of your current location using curr_geo_tag_creator.py. This geo tag is used by the app to verify if the user is within the specified vicinity of the tagged location (default: 100 meters).
Cost-efficient: The AI Attendance Monitor eliminates the need for manual attendance tracking and reduces administrative efforts by automating the process using AI technologies.

**Prerequisites**
Python 3.x
OpenCV-Python library
Geocoder library
Geopy library

**Installation**

Clone the repository:

git clone https://github.com/Sour-abh-Raj/AI-Attendance-Monitor.git
cd AI-Attendance-Monitor

Install the required dependencies:

pip install -r requirements.txt

**Usage**

1.Generate a geo tag of your current location by running:

python curr_geo_tag_creator.py

2. Start the Flask app:

python app.py

Access the AI Attendance Monitor web interface by navigating to http://localhost:5000 in your web browser.

**Customization**

1. Changing Vicinity Distance: You can modify the vicinity distance in vicinity_checker.py to adjust the range within which a user's location is considered valid.
2. Updating Reference Photos: To update the reference photos for face recognition, add the corresponding images to the attendanceResources folder.

**License**
This project is licensed under the MIT License.

Feel free to customize the content according to your specific project details and requirements.
