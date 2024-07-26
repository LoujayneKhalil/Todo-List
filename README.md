# ToDo List Application

A ToDo List application built with React.js, Redux, FastAPI, and PostgreSQL. This project features task management with drag-and-drop reordering capabilities for admin users and categorized task viewing for regular users.

## Features

- **Admin and User Views**: Separate interfaces for admin and regular users.
- **Drag-and-Drop Reordering**: Admin users can reorder tasks using drag-and-drop functionality.
- **Task Categorization**: Tasks can be categorized for better organization.
- **Persistent Storage**: Tasks are saved in a PostgreSQL database.
- **Authentication & Authorization**: Secure login system with role-based access control.

## Technologies Used

- **Frontend**: React.js, Redux
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL
- **Others**: Docker (optional), SQLAlchemy, Pydantic

## Project Structure

### Backend (FastAPI)

```
/backend
├── app
│   ├── main.py          # Entry point for the FastAPI app
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic models
│   ├── crud.py          # CRUD operations
│   ├── dependencies.py  # Dependency injections
│   ├── routers
│   │   ├── tasks.py     # Task-related endpoints
│   │   ├── categories.py# Category-related endpoints
│   │   ├── auth.py      # Authentication endpoints
│   ├── database.py      # Database connection
│   ├── __init__.py
├── requirements.txt     # Project dependencies
├── alembic              # Database migrations
```

### Frontend (React.js with Redux)

```
/frontend
├── src
│   ├── components
│   │   ├── TaskList.js       # Displays tasks
│   │   ├── TaskItem.js       # Single task details
│   │   ├── AdminView.js      # Admin-specific functionalities
│   │   ├── UserView.js       # User-specific functionalities
│   ├── redux
│   │   ├── store.js          # Redux store
│   │   ├── actions.js        # Redux actions
│   │   ├── reducers.js       # Redux reducers
│   ├── App.js                # Main app component
│   ├── index.js              # Entry point
├── package.json              # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.7+
- Node.js and npm
- PostgreSQL

### Backend Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/todo-list-app.git
   cd todo-list-app/backend
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**:
   Update the database connection string in `app/database.py`.

4. **Run the backend server**:

   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to the frontend directory**:

   ```bash
   cd ../frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Start the development server**:

   ```bash
   npm start
   ```

## Usage

- **Admin View**: Accessible to admin users for managing tasks and reordering them.
- **User View**: Regular users can view tasks as ordered by the admin.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to all contributors and the open-source community.
