# Valentine Proposal Website

## Deployment on Railway

This is a full-stack application with:
- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI + MongoDB
- **Payment**: Razorpay Integration

## Environment Variables

### Backend Service
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=valentine_db
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
CORS_ORIGINS=*
PORT=8001
```

### Frontend Service
```
REACT_APP_BACKEND_URL=https://your-backend-service.railway.app
REACT_APP_RAZORPAY_KEY_ID=your_razorpay_key_id
```

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8001
```

### Frontend
```bash
cd frontend
yarn install
yarn start
```
