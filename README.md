# B2D-Ventures

## Description

B2D Ventures is a web-based application designed to connect investors with promising startup companies. B2D Ventures allows investors to browse, evaluate, and invest in startups that match their interests. The platform ensures a secure and compliant investment process.

## Project Documentation

All project documents are in the [Project Wiki](../../wiki/Home).

## Installation Instruction
1. Clone the repository from GitHub.
   ```
   git clone https://github.com/J-Jullaphong/b2d-ventures.git
   ```
2. Change directory to b2d-ventures.
   ```
   cd b2d-ventures
   ```
3. Create a virtual environment.
   ```
   python -m venv venv
   ```
4. Activate the virtual environment.
   - Linux and macOS
   ```
   source venv/bin/activate
   ```
   - Windows
   ```
   .\venv\Scripts\activate
   ```
5. Install Dependencies for required python modules.
   ```
   pip install -r requirements.txt
   ```
6. Create a `.env` file for externalized variables.
   - Linux and macOS
   ```
   cp sample.env .env
   ```
   - Windows
   ```
   copy sample.env .env
   ```
7. Use a text editor to edit the values in `.env` file as needed.

## How to Run
1. Activate virtual environment.
   - Linux and macOS
   ```
   source venv/bin/activate
   ```
   - Windows
   ```
   .\venv\Scripts\activate
   ```
2. Start the server. (If it doesn't work, please use `python3` instead of `python`)
   ```
   python manage.py runserver
   ```
3. To use this application, go to this link in your browser.
   ```
   http://localhost:8000
   ```
4. To close the running server, press `Ctrl+C` in your terminal or command prompt.
5. After finish using the application, deactivate the virtual environment.
   ```
   deactivate
   ```
