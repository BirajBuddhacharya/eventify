# Eventify 🎉

A comprehensive event management and registration platform designed for RoadTract Club branches to organize and manage events seamlessly.

## 📋 Overview

Eventify is a full-stack web application that enables users to discover, register for, and manage events organized by various branches of the RoadTract Club. The platform provides an intuitive interface for both event organizers and attendees, streamlining the entire event management process.

## ✨ Features

- **Event Discovery**: Browse events organized by different RoadTract Club branches
- **User Registration**: Simple and secure user authentication system
- **Event Registration**: Easy registration process for events
- **Payment Integration**: Secure payment processing with Khalti
- **Location Services**: Interactive maps and location-based event discovery
- **Email Notifications**: Automated email confirmations and updates
- **Admin Dashboard**: Comprehensive admin panel for event management
- **Club Management**: Multi-branch support with dedicated club pages
- **Responsive Design**: Mobile-friendly interface built with modern UI components
- **Real-time Updates**: Dynamic event information and registration status

## 🛠 Tech Stack

### Frontend
- **Framework**: Next.js 14+ with TypeScript
- **UI Library**: shadcn/ui components
- **Styling**: Tailwind CSS
- **Maps Integration**: Google Maps API & OpenRouteService
- **Geocoding**: OpenCage Geocoding API
- **State Management**: React Hooks & Context API
- **Authentication**: Firebase Authentication

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Firebase Admin SDK
- **Email Service**: Resend API & Gmail SMTP
- **Payment Gateway**: Khalti API
- **File Storage**: Media handling for event assets
- **API**: RESTful API architecture

## 📁 Project Structure

```
Eventify/
├── frontend/                 # Next.js TypeScript frontend
│   ├── app/                 # App router pages
│   │   ├── (normalUser)/    # User-facing pages
│   │   ├── admin/           # Admin dashboard
│   │   ├── club/            # Club-specific pages
│   │   ├── login/           # Authentication pages
│   │   └── api/             # API routes
│   ├── components/          # Reusable UI components
│   ├── lib/                # Utility libraries
│   ├── hooks/              # Custom React hooks
│   ├── context/            # React context providers
│   └── public/             # Static assets
│
└── backend/                 # Flask Python backend
    ├── api/                # API blueprint modules
    │   ├── controllers/    # Request handlers
    │   ├── routes/         # Route definitions
    │   ├── models/         # Database models
    │   └── utils/          # Helper utilities
    ├── firebase/           # Firebase configuration
    ├── middleware/         # Custom middleware
    ├── media/             # File uploads
    └── migrations/        # Database migrations
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/pnpm
- Python 3.8+
- PostgreSQL database (Supabase account)
- Firebase project setup
- Google Maps API key
- Khalti merchant account (for payments)

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   pnpm install
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Configure your environment variables:
   ```env
   NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
   NODE_ENV=development
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   OPEN_ROUTE_SERVICE_API_KEY=your_openroute_api_key
   OPEN_CAGE_API_KEY=your_opencage_api_key
   ```

5. Run the development server:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

6. Run the development server:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

   The frontend will be available at `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

5. Add Firebase service account key:
   ```bash
   # Place your Firebase service account JSON file as:
   # backend/firebase/serviceKey.json
   ```

5. Run database migrations:
   ```bash
   # Database will be automatically managed by Supabase
   # Ensure your DATABASE_URL is correctly configured
   ```

6. Start the Flask development server:
   ```bash
   python app.py
   # or
   flask run
   ```

   The backend API will be available at `http://localhost:5000`

## 🔧 Configuration

### Firebase Setup

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
2. Enable Authentication with your preferred sign-in methods
3. Download the service account key and save it as `backend/firebase/serviceKey.json`
4. Configure Firebase SDK in both frontend and backend

### Third-party Services Setup

**Google Maps API:**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable Maps JavaScript API and Geocoding API
3. Create an API key and add it to your environment variables

**Khalti Payment Gateway:**
1. Create a merchant account at [Khalti](https://khalti.com)
2. Get your API keys from the merchant dashboard
3. Configure test/live keys based on your environment

**OpenRouteService & OpenCage:**
1. Register at [OpenRouteService](https://openrouteservice.org) for routing services
2. Register at [OpenCage](https://opencagedata.com) for geocoding services
3. Add the API keys to your environment variables

### Environment Variables

**Frontend (.env)**
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
NODE_ENV=development
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
OPEN_ROUTE_SERVICE_API_KEY=your_openroute_service_api_key
OPEN_CAGE_API_KEY=your_opencage_api_key
```

**Backend (.env)**
```env
DATABASE_URL=your_supabase_database_url
FIREBASE_API_KEY=your_firebase_api_key
FLASK_ENV=development
RESEND_API_KEY=your_resend_api_key
MAIL_USERNAME=your_gmail_username
MAIL_PASSWORD=your_gmail_app_password
SUPPORT_EMAIL=your_support_email
KHALTI_API_KEY=your_khalti_api_key
BACKEND_URL=http://localhost:5000
FRONTEND_URL=http://localhost:3000
```

## 📚 API Documentation

The backend provides a RESTful API with the following main endpoints:

- `GET /api/events` - Retrieve all events
- `POST /api/events` - Create new event (Admin only)
- `GET /api/events/:id` - Get specific event details
- `POST /api/register` - Register for an event
- `GET /api/clubs` - List all club branches
- `POST /api/auth` - Authentication endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in this repository
- Contact the development team
- Check the documentation wiki

---

**Note**: This project is actively maintained and continuously improved. Check back regularly for updates and new features!
