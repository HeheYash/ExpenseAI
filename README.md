# MultiModel Classification System for Expense Management

A modern web application where users scan receipts and UPI screenshots to automatically extract transaction details via OCR, classify categories using ML, and track expenses with budgets on an animated dashboard with monthly resets and savings tracking.

## 🚀 Features

- **Receipt OCR & Parsing**: Google Vision API with Tesseract fallback for accurate text extraction
- **ML-Powered Classification**: Transformer-based transaction categorization with vendor mapping
- **Real-time Processing**: WebSocket notifications for processing updates
- **Modern Dashboard**: Animated charts with glassmorphism design
- **Budget Tracking**: Monthly budget limits with progress tracking
- **Mobile Responsive**: Optimized for all devices with camera support
- **Privacy-First**: PII detection and data redaction

## 📋 Tech Stack

### Backend
- **FastAPI**: High-performance async API framework
- **PostgreSQL**: Primary database with SQLAlchemy ORM
- **Redis**: Caching and message broker
- **Celery**: Background task processing
- **MinIO**: S3-compatible object storage
- **JWT**: Authentication with refresh tokens

### Frontend
- **React 18**: Modern UI with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Recharts**: Interactive data visualization
- **Zustand**: Lightweight state management

### ML & Processing
- **Google Vision API**: Primary OCR service
- **Tesseract**: Open-source OCR fallback
- **DistilBERT**: Transaction classification
- **OpenCV**: Image preprocessing

## 🛠️ Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Google Vision API key (optional, Tesseract available as fallback)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MultiModel_Classification_System_for_Expense_Management
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start development services**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Initialize database**
   ```bash
   docker-compose -f docker-compose.dev.yml exec backend python -m alembic upgrade head
   docker-compose -f docker-compose.dev.yml exec backend python scripts/seed-data.py
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001
   - Flower (Celery monitoring): http://localhost:5555

### Production Deployment

```bash
docker-compose up -d
```

## 📊 Database Schema

### Core Tables
- **users**: User accounts with authentication
- **categories**: Transaction categories (system + user-defined)
- **transactions**: Expense records with OCR data
- **budgets_history**: Monthly budget tracking
- **vendor_mappings**: Learned vendor→category relationships
- **audit_corrections**: User corrections for active learning

## 🔄 Processing Pipeline

1. **Upload**: User uploads receipt image via frontend
2. **Storage**: File stored in MinIO with transaction record created
3. **OCR**: Image processed with Google Vision → Tesseract fallback
4. **Parsing**: Extract amount, date, vendor using rules + ML
5. **Classification**: Predict category with confidence scoring
6. **Notification**: WebSocket update to frontend
7. **Confirmation**: User confirms/corrects extracted data
8. **Learning**: System learns from corrections for future accuracy

## 🎨 Categories (System Defaults)

| Category | Icon | Color | Description |
|----------|------|-------|-------------|
| Food & Dining | 🍔 | #FF6B6B | Restaurants, cafes, bars |
| Groceries | 🛒 | #4ECDC4 | Supermarkets, food stores |
| Transportation | 🚗 | #45B7D1 | Uber, fuel, public transport |
| Utilities | 💡 | #96CEB4 | Electricity, water, internet |
| Housing | 🏠 | #DDA0DD | Rent, maintenance, supplies |
| Healthcare | 🏥 | #FFB6C1 | Hospitals, pharmacies, insurance |
| Entertainment | 🎬 | #FFD93D | Movies, games, subscriptions |
| Shopping | 🛍️ | #6C5CE7 | Clothing, electronics, books |
| Education | 📚 | #74B9FF | Courses, books, training |
| Other | 📌 | #A8A8A8 | Miscellaneous expenses |

## 🔐 Security Features

- **JWT Authentication**: Short-lived access tokens with refresh mechanism
- **Password Hashing**: bcrypt with cost factor 12
- **Rate Limiting**: Configurable limits per endpoint
- **PII Detection**: Automatic redaction of sensitive information
- **HTTPS Only**: Enforced in production
- **CORS**: Configured for frontend domain
- **Input Validation**: Comprehensive request validation

## 📈 Monitoring & Logging

- **Structured Logging**: JSON format with correlation IDs
- **Health Checks**: All services expose health endpoints
- **Error Tracking**: Sentry integration for error monitoring
- **Metrics**: Prometheus-compatible metrics
- **Performance**: Request timing and database query monitoring

## 🧪 Testing

```bash
# Backend tests
docker-compose -f docker-compose.dev.yml exec backend pytest

# Frontend tests
docker-compose -f docker-compose.dev.yml exec frontend npm test

# E2E tests
npm run test:e2e
```

## 📚 API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/transactions/upload` - Upload receipt for processing
- `GET /api/v1/dashboard/summary` - Dashboard summary data
- `GET /api/v1/categories` - List transaction categories
- `POST /api/v1/budgets/{category_id}` - Set category budget

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Bank account integration
- [ ] Advanced analytics and insights
- [ ] Multi-currency support
- [ ] Team/family expense sharing
- [ ] Receipt template learning
- [ ] Subscription management
