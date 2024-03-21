Test_task

This repository showcases a test task demonstrating integration with OpenAI's Assistant API. To optimize the workflow, I've designed the logic across three endpoints:

1. Message Response: Receives a user's message and returns the bot's latest response to that message.
2. Thread Messages Retrieval: Retrieves the complete message thread for a specified thread_id.
3. User Thread IDs Retrieval: Lists all thread IDs associated with a user.

Additionally, I have implemented an Authentication API to enhance security and manage user access effectively.





Entity Relationship Diagram (ERD)
        ![image](https://github.com/Geo-Lih/OpenAi_Assitant_Api_Test_Task/assets/72580162/723ab6f7-89c8-41c7-aea6-98b184bccb74)





Uploading Instructions:

1. Clone the Repository:

        git clone https://github.com/Geo-Lih/OpenAi_Assitant_Api_Test_Task.git


2. Set Up Virtual Environment:

        python3.10 -m venv venv

3. Activate the virtual environment:

        source venv/bin/activate


4. Install Dependencies:

        pip install -r requirements.txt


5. Set Up Environment Variables:

You need to create a `.env` file in the root of the project with the following structure:

        DB_HOST=localhost
        
        DB_PORT=3306
        
        DB_NAME=test_task
        
        DB_USER=your_database_user
        
        DB_PASS=your_database_password

        API_KEY = your_api_key
        
        ASSISTANT_KEY = your_assistant_key

        SECRET_KEY = your_secret_key
        
        ALGORITHM = your_symmetric_keyed_hashing_algorithm


6. Run Alembic Migrations:

First, make sure your database connection details are correctly set in the `.env` file.

        alembic upgrade 18062f7f6d1a

This will apply all pending migrations and update the database schema.


7. Run the FastAPI Application:

        uvicorn main:app --reload
