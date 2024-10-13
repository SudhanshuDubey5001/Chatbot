# Chatbot Application Overview

This is a comprehensive chatbot application designed to facilitate seamless interactions between users and the system. The application leverages cutting-edge technologies to provide a robust and efficient solution for managing orders, tracking status, and processing user requests.

## Technologies Used

The application is built using a combination of the following technologies:

### DialogFlow

DialogFlow is a Google-developed platform that enables the creation of conversational interfaces. In this application, DialogFlow is utilized for:

* Chatting with the bot: Users can engage in natural language conversations with the chatbot.
* Processing text: DialogFlow processes user input using training phrases to extract relevant information.
* Sending extracted information: The extracted information is sent to the backend for further processing.

### Python and FastAPI

Python is used as the backend technology, and FastAPI is employed to create webhooks APIs. These APIs process requests received from DialogFlow and send appropriate responses back to the user.

### MySQL

MySQL is the database management system of choice for storing and fetching data related to:

* Order details
* Food item details
* Tracking order information

## Deployment

The application is deployed on two platforms:

### Backend Deployment

The backend is deployed on Vercel (https://vercel.com/), a platform that enables fast and efficient deployment of web applications.

### MySQL DB Deployment

The MySQL database is deployed on Aiven (https://aiven.io/), a cloud-based service that provides managed databases for various technologies, including MySQL.

This deployment strategy ensures high availability, scalability, and reliability of the application, making it suitable for production environments.
