# 🎉 Face Recognition with Real-Time Detection and Database Integration

## 🚀 Title

**Face Recognition with Real-Time Detection and Database Integration**: A project that uses OpenCV, face recognition, and SQLite to identify faces in real-time and log attendance details in a database.

## 🛠️ Technologies Used

- 🐍 **Python**: The core programming language.
- 👁️ **OpenCV**: For real-time computer vision tasks.
- 👤 **face_recognition**: To recognize and identify faces.
- 🗄️ **SQLite**: For database management.
- 🌐 **Socket Programming**: For network communication between server and client.


## 🌟 Features

- 🎥 **Real-Time Face Detection**: Detects faces from a live video stream.
- 👁️ **Face Recognition**: Matches detected faces with pre-encoded images.
- 💾 **Database Logging**: Logs attendance and other details into an SQLite database.
- 🔔 **Customizable Alerts**: Trigger actions based on specific face recognition events.
- 📨 **HTTP Request Parsing**: Listens and reacts to incoming signals via HTTP requests.

## 🗂️ Project Structure

Here's a brief overview of the main files in this project:

- `images`📁:  Directory for storing known face images
- `main_video.py `📝: Main script that runs the project
- `sqlite.db` 🗃️: SQLite database file

## 📝 How to Use

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/face-recognition-project.git
    cd face-recognition-project

    ```

2. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    # Ensure that you camera or IP camera is connected and accessible.
    ```

3. **Run the script**:
    ```bash
    python main_video.py
    ```
## 🎉 Example Output
When a face is detected and recognized, the following output is logged:
```plaintext
Connected by ('192.168.1.100', 53765)
High signal detected! Running Python script...
John Doe Btech CSE 2022-2026 A20405222069 2024-08-17 14:25:30
```
The recognized face's name, course, batch, enrollment number, and timestamp are stored in the SQLite database.

## 🛠️ Customization
- 👤 **`Adding New Faces`**: To add new faces, simply place the images in the **'images/'** directory and re-run the script.

- 🎥 **`Change Camera Source`**: Modify the video capture URL in **'main.py'** to switch between different camera sources.

- 💽 **`Database Modifications`**: Adjust the SQLite database schema in the **'database.py'** file if needed.


## 🤝 Contributing
Contributions are welcome! Please follow these steps:

1. 🍴 Fork the repository.
2. 🌿 Create a new branch (**'git checkout -b feature/your-feature-name'**).
3. 📝 Commit your changes (**'git commit -m 'Add your feature'**).
4. 🚀 Push to the branch (**'git push origin feature/your-feature-name'**).
5. 🔄 Open a pull request.

Let's work together to make this project even better! 🎉
