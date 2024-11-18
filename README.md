# Project Name

This project is a simple Node.js application to parse user inputs and return a selecion of possible birds. Follow the instructions below to set up your environment and get started.

## Setup

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone <repository-url>
```

### 2. Install Dependencies

After cloning the project, navigate into the project directory:

cd <42Hackathon_RSPB>

Then, install the necessary dependencies by running:

```bash
npm install
```

This will install the required node_modules and all other dependencies listed in the package.json file.

### 3. Create a .env File

The application requires a .env file to configure environment variables.

  Create a file named .env in the root of the project.
  Add the following line to the .env file to define your preferred port:

PORT=3005

You can replace 3005 with any port number you'd like the application to run on. If you don’t specify a port, the application will default to port 3000.

### 4. Running the Application

Once the dependencies are installed and your .env file is set up, you can start the application with the following command:

npm run dev

This will start the server and it will listen on the port specified in your .env file.

### 5. Available Endpoints

The current available endpoint is:

   GET /birds
   
   GET /test

### 6. Troubleshooting

  If you encounter issues with missing dependencies, try running npm install again.
  Make sure your .env file is correctly set up and the PORT variable is defined.
  If you run into port conflicts, change the value of PORT in your .env file to an available port.
