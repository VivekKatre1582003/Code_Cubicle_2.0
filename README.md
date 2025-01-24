# IssueConnect

## Problem Statement
**IssueConnect** is a platform designed to bridge the gap between local citizens and authorities, making it easier to report issues that require attention. The platform provides a simple and efficient way to:

1. **Remove hesitation**: The platform removes the burden of long, written reports by allowing users to alert authorities with a single click.
2. **Reduce the communication gap**: It establishes a quicker, more effective way for locals to contact authorities, fostering better communication.
3. **Increase response time**: Authorities receive issues faster and can respond more promptly.

## Features
- **Single-click reporting**: Submit issues with one click, eliminating the need for lengthy forms.
- **Fast issue transmission**: Ensure that issues reach authorities more quickly than traditional methods.
- **Efficient handling**: Issues are tracked, categorized, and managed for a swift resolution.

## Challenges & Solutions

### 1. **File Handling Issues**:
   - **Problem**: We faced errors related to file uploads and renaming.
   - **Solution**: Implemented checks to verify if files exist before renaming and improved error handling for file operations.

### 2. **Database Schema Management**:
   - **Problem**: Struggled with schema migrations and database management.
   - **Solution**: Used SQLAlchemy’s `db.create_all()` for initial schema creation and managed schema changes manually.

### 3. **UI/UX Design Constraints**:
   - **Problem**: Issues with displaying images correctly in the web application.
   - **Solution**: Adjusted CSS and HTML templates to ensure proper image sizing and display according to design specifications.

### 4. **Error Handling**:
   - **Problem**: Struggled with effectively handling various types of errors.
   - **Solution**: Improved error handling mechanisms and implemented user-friendly error messages to enhance troubleshooting and the overall user experience.

## Technologies Used

- **Flask**: A web framework for building the web application.
- **TensorFlow**: Used for AI and ML models.
- **Keras**: A deep learning library for building models.
- **SQLite**: Database for storing application data.
- **HTML/CSS**: For frontend development and styling.
- **Jinja2**: Templating engine used in Flask.
- **Werkzeug**: WSGI utility library for Python used for HTTP utilities.
- **Python 3.12**: The Python programming language used to develop the application.
- **Windows 11**: Development environment.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/issueconnect.git
