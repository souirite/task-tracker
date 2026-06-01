# Task Tracker v2 - Vue 3 + FastAPI

A modern, elegant task management application with area-based organization built with Vue 3 + Vite frontend and FastAPI + SQLite backend.

## Features

✅ **Area Management**
- Create, read, update, and delete areas
- Organize tasks by areas
- Sidebar navigation with area list

✅ **Task Management**
- Full CRUD operations for tasks
- Task status toggle (open/closed)
- Auto-populate date closed when task is closed
- Priority levels (Critical, High, Medium, Low)

✅ **Filtering & Search**
- Filter by status (all/open/closed)
- Filter by priority
- Search by description
- Real-time filtering

✅ **Statistics Dashboard**
- Total task count
- Open task count
- Closed task count
- Critical task count

✅ **Export**
- Export tasks to CSV format

✅ **Elegant UI**
- Responsive design with Tailwind CSS
- Clean, modern interface
- Smooth animations and transitions

## Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **SQLite** - Lightweight database
- **Pydantic** - Data validation using Python type annotations

## Project Structure

```
task-tracker-vue/
├── backend/
│   ├── __init__.py
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── main.py           # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/   # Vue components
│   │   ├── api.js        # API client
│   │   ├── App.vue       # Main app component
│   │   ├── main.js       # Vue app entry point
│   │   └── style.css     # Tailwind CSS
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── requirements.txt      # Python dependencies
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Create virtual environment**
```bash
cd task-tracker-vue
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run FastAPI server**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## API Endpoints

### Areas
- `GET /api/areas` - Get all areas
- `POST /api/areas` - Create new area
- `GET /api/areas/{id}` - Get specific area with tasks
- `PUT /api/areas/{id}` - Update area
- `DELETE /api/areas/{id}` - Delete area

### Tasks
- `GET /api/tasks?area_id={id}` - Get tasks for an area
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `GET /api/tasks/stats/{area_id}` - Get task statistics

### Health
- `GET /api/health` - Health check endpoint

## Database Schema

### Areas Table
- `id` - Primary key
- `name` - Area name
- `description` - Area description
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Tasks Table
- `id` - Primary key
- `area_id` - Foreign key to areas
- `description` - Task description
- `priority` - Priority level (Critical, High, Medium, Low)
- `status` - Task status (open, closed)
- `date_raised` - Date task was created
- `date_closed` - Date task was closed (nullable)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Usage

1. **Create an Area**
   - Click "+ New Area" button
   - Enter area name and description
   - Click Save

2. **Create a Task**
   - Select an area from the sidebar
   - Click "+ New Task" button
   - Fill in task details (description, priority, date raised)
   - Click Save

3. **Manage Tasks**
   - Click status button to toggle between open/closed
   - Click "Edit" to modify task details
   - Click "Delete" to remove task

4. **Filter Tasks**
   - Use search bar to filter by description
   - Use status dropdown to filter by open/closed
   - Use priority dropdown to filter by priority level

5. **Export Tasks**
   - Click "Export CSV" to download tasks as CSV file

## Development

### Running Tests
```bash
# Backend tests (if added)
pytest

# Frontend tests (if added)
npm run test
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:**
The FastAPI app is production-ready. Deploy using:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## License

MIT License

## Support

For issues or questions, please create an issue in the repository.
