<p align="center">
  <img src="https://i.imgur.com/wSihQEu.png" width="250" />
</p>

<h1 align="center">AEM - ACES Event Manager</h1>

<p align="center">
  <strong>Streamline your college's event management with AEM</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#ideas">Ideas</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <em>Special thanks to <a href="https://github.com/TomSchimansky">TomSchimansky</a> for their amazing <a href="https://github.com/TomSchimansky/CustomTkinter">CustomTkinter</a> library!</em>
</p>

## What is AEM?

AEM (ACES Event Manager) is a desktop application designed specifically by & for the <a href="https://cse.dbatu.ac.in/?page_id=2458">Association of Computer Engineering Students (ACES)</a>. Built using the CustomTkinter Python GUI library, AEM makes event management easier and quicker for student organizations.

## Why AEM?

Managing events can be challenging for student organizations. AEM simplifies this process by providing a user-friendly interface and powerful features for both user and admin roles, tailored to ACES' needs. It streamlines event organization, scheduling, and tracking, making it easier for students to create and participate in memorable experiences.

## Features

- 🔐 **Secure Authentication**: Dedicated student registration & login panel
- 📊 **Comprehensive Dashboard**: Tailored experience for different user roles 
- 💾 **MySQL Database**: Secure storage and management of all event-related data
- 🤖 **Quick Message Generation**: Create broadcasting messages based on given event details in a click
- 📱 **Messaging Integration**: WhatsApp and Telegram integration to broadcast notifications of new events
- 📧 **Bulk Email**: Send event-related emails in bulk to all the users
- 📊 **Data Export**: Export event data to CSV and XLSX formats using openpyxl

## Installation


Make sure you have Python 3.x installed on your system before proceeding with the installation.

To set up AEM on your local machine, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ryukaizen/ACES-Event-Manager.git
    cd ACES-Event-Manager
    ```

2. **Set up environment variables**:
    ```sh
    cp .env.example .env
    ```

3. **Edit and fill up all the relevant environment variables inside the .env file**

4. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application:**:
    ```sh
    python3 app.py
    ```

## Ideas
- [ ] Feature to import CSV or XSLX files
- [ ] Reset button in content configuration
- [ ] Ability to merge saved content, generated date, time and venue values


## Contributing

Contributions are always welcomed! PR or open an issue in case you stumble upon any bugs.

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by<a href="https://cse.dbatu.ac.in/?page_id=2458"> ACES</a>
</p>
