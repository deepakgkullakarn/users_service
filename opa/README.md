# Users Service API (FastAPI + JWT + OPA-style Authorization)

This project is a **FastAPI-based Users API** with:

- JWT authentication
- Role-based authorization (admin/user)
- OPA-style authorization logic (simple)
- In-memory user storage (can be replaced with a database)

**************************************************************

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Authorization & JWT](#authorization--jwt)
- [Notes](#notes)

**************************************************************

## Features

- **User login** with JWT token generation
- **GET /users**: Accessible to all authenticated users
- **POST /users**: Only admin users can create new users
- Simple **OPA-style authorization** logic implemented in Python
- Logs JWT payload for debugging

**************************************************************

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- PyJWT
- Pydantic

**************************************************************

## Installation

1. Clone the repository:
git clone <repo-url>
cd <repo-directory>
