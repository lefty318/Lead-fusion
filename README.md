# OmniLead - AI-Powered Lead Management Platform

OmniLead is a comprehensive AI-powered dashboard that ingests WhatsApp, Instagram, and Facebook messages into a single unified interface for student conversation management, lead scoring, and automated engagement.

## Features

### Core Functionality
- **Multi-source ingestion**: WhatsApp Business API, Meta Graph API for Facebook Messenger & Instagram DMs
- **Unified inbox**: Single view of conversations across all channels with channel badges and timestamps
- **AI assistant**: Real-time auto-responses, intent classification, contact data extraction, lead scoring, and sentiment analysis
- **Human escalation**: Automatic escalation based on AI confidence thresholds or manual "Talk to human" triggers
- **Multi-user collaboration**: Role-based access control (admin, sales, counselor, analyst) with per-user dashboards
- **Real-time notifications**: In-app, email, SMS, and push notifications with configurable rules
- **Analytics & reporting**: Conversion funnel, response latency, lead sources, campaign ROI, agent performance with CSV/XLSX/PDF exports

### Technical Architecture
- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python) with Socket.IO for real-time updates
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: OpenAI GPT models for intent classification, sentiment analysis, and automated responses
- **Real-time**: Socket.IO for live message updates
- **Caching**: Redis for session management and caching
- **File Storage**: S3-compatible object storage for attachments
- **Notifications**: Firebase Cloud Messaging, SendGrid, Twilio
- **Monitoring**: Structured logging with audit trails

## Project Structure

```
omnilead/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── utils/           # Utilities and compliance
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database connection
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── venv/                # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── store/           # Redux store and slices
│   │   ├── services/        # API services
│   │   ├── hooks/           # Custom hooks
│   │   └── App.tsx          # Main application
│   ├── package.json         # Node dependencies
│   └── tailwind.config.js   # Tailwind configuration
└── README.md
```

## Quick Start

### Automated Setup (Recommended)

**Backend:**
```bash
cd backend
python setup.py          # Creates .env and checks setup
pip install -r requirements.txt
# Update DATABASE_URL in .env file
alembic upgrade head
python -m uvicorn app.main:socket_app --reload
```

**Frontend:**
```bash
cd frontend
node setup.js            # Creates .env and checks setup
npm install
npm start
```

For detailed instructions, see **[GETTING_STARTED.md](GETTING_STARTED.md)** or **[QUICK_START.md](QUICK_START.md)**.

## Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Step-by-step getting started guide ⭐
- **[QUICK_START.md](QUICK_START.md)** - Complete setup guide
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Setup verification checklist
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current project status
- **[FINAL_SUMMARY.md](FINAL_SUMMARY.md)** - Complete project overview
- **[backend/README_MIGRATIONS.md](backend/README_MIGRATIONS.md)** - Database migration guide
- **[backend/README_TESTS.md](backend/README_TESTS.md)** - Testing guide

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Key Components

### AI Processing Pipeline
- **Intent Classification**: Categorizes messages as enquiry, complaint, enrollment, technical, etc.
- **Sentiment Analysis**: Determines emotional tone of conversations
- **Lead Scoring**: Calculates lead quality based on intent, keywords, and engagement
- **Automated Responses**: Generates contextual replies for routine queries

### Escalation Logic
- Automatic escalation when AI confidence < 65%
- Keyword-based escalation (refund, legal, complaint, technical, urgent)
- Negative sentiment + repeated messages trigger human intervention

### Compliance & Security
- PII detection and masking
- Data retention policies (2 years for conversations, 3 years for leads)
- Comprehensive audit logging
- GDPR compliance checks

## Development

### Running Tests
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

See **[backend/README_TESTS.md](backend/README_TESTS.md)** for detailed testing information.

### Code Quality
- **Backend**: Type hints, Pydantic validation, comprehensive error handling
- **Frontend**: TypeScript with strict mode, ESLint, comprehensive type definitions
- **Database**: Alembic migrations for schema management
- **Configuration**: Environment-based with validation and security checks

### Recent Improvements
- ✅ Enhanced environment variable configuration with validation
- ✅ Comprehensive error handling for AI services
- ✅ Alembic database migrations setup
- ✅ Complete TypeScript type system
- ✅ Testing infrastructure with pytest
- ✅ Production-ready configuration

See **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** for details.

## Deployment

The application is designed for serverless deployment with:
- AWS Lambda + API Gateway for backend
- S3 + CloudFront for frontend static hosting
- PostgreSQL RDS for database
- Redis ElastiCache for caching
- Firebase/SendGrid/Twilio for notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub or contact the development team.