# Air Imports Chatbot for CargoWise

## Description
This repository contains code for a simple chatbot designed for Air Imports using CargoWise. It serves to answer questions, provide instructions, and offer support specifically tailored to users operating air imports through CargoWise. The chatbot is particularly useful for new users undergoing training on the software.

## Requirements
- Python 3.x
- Git

## Setup
1. Clone the repository to your local machine:
    ```shell
    git clone https://github.com/<username>/air-imports-chatbot.git
    cd air-imports-chatbot
    ```

2. Create a virtual environment (optional but recommended):
    ```shell
    python -m venv chatbot
    ```

3. Activate the virtual environment:
    - On Windows:
        ```shell
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```shell
        source venv/bin/activate
        ```

4. Install dependencies:
    ```shell
    pip install -r requirements.txt
    ```

5. Set up AWS credentials:
    - Ensure you have AWS credentials configured with appropriate permissions.
    - Modify the `AWS_PROFILE` environment variable in `chatbot.py` to match your AWS profile name.

6. Run the application:
    ```shell
    streamlit run chatbot.py
    ```

## Usage
- The chatbot interface will open in your default web browser.
- Input your question related to air imports using CargoWise in the sidebar.
- Click the "Submit" button to get the chatbot's response.
- The chatbot will provide answers, instructions, and support tailored to air imports operations in CargoWise.

## Features
- **Customization**: The chatbot is customized for air imports operations using CargoWise.
- **Question Answering**: Provides answers to queries related to CargoWise functionality and air imports processes.
- **Training Support**: Designed to assist new users undergoing training on CargoWise for air imports.


