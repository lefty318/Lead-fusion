# Setup Checklist

Use this checklist to ensure your OmniLead project is properly configured.

## ✅ Pre-Setup Verification

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ and npm installed
- [ ] PostgreSQL database server running
- [ ] Git repository initialized (optional)

## 🔧 Backend Setup

### Environment Configuration
- [ ] Create `backend/.env` file
- [ ] Set `DATABASE_URL` (PostgreSQL connection string)
- [ ] Generate and set `SECRET_KEY` (use: `python -c 'import secrets; print(secrets.token_urlsafe(32))'`)
- [ ] Set `ENVIRONMENT=development`
- [ ] Set `DEBUG=true` (for development)
- [ ] (Optional) Set `OPENAI_API_KEY` if using AI features
- [ ] (Optional) Configure other service keys (Twilio, SendGrid, AWS, etc.)

### Database Setup
- [ ] PostgreSQL database created: `CREATE DATABASE omnilead;`
- [ ] Database user has proper permissions
- [ ] Run initial migration: `cd backend && alembic upgrade head`
  - Or create migration: `alembic revision --autogenerate -m "Initial migration"`

### Dependencies
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`

### Verification
- [ ] Backend starts without errors: `python -m uvicorn app.main:socket_app --reload`
- [ ] API docs accessible: `http://localhost:8000/docs`
- [ ] Health check works: `http://localhost:8000/health`

## 🎨 Frontend Setup

### Environment Configuration
- [ ] (Optional) Create `frontend/.env` file
- [ ] (Optional) Set `REACT_APP_API_URL` if different from default

### Dependencies
- [ ] Dependencies installed: `cd frontend && npm install`
- [ ] Verify `react-router-dom` is installed

### Verification
- [ ] Frontend starts: `npm start`
- [ ] Application loads at `http://localhost:3000`
- [ ] No console errors

## 🧪 Testing

### Backend Tests
- [ ] Run tests: `cd backend && pytest`
- [ ] All tests pass
- [ ] (Optional) Run with coverage: `pytest --cov=app`

### Frontend Tests
- [ ] Run tests: `cd frontend && npm test`
- [ ] All tests pass

## 🔐 Security Checklist

- [ ] `SECRET_KEY` is set and secure (not default value)
- [ ] `.env` files are in `.gitignore`
- [ ] Database credentials are secure
- [ ] API keys are not committed to version control
- [ ] CORS settings are appropriate for your environment
- [ ] (Production) HTTPS is configured
- [ ] (Production) Debug mode is disabled

## 📊 Database Migrations

- [ ] Initial migration created and reviewed
- [ ] Migration applied: `alembic upgrade head`
- [ ] Database schema matches models
- [ ] Migration files are version controlled

## 🚀 First Run

- [ ] Backend server running
- [ ] Frontend application running
- [ ] Can access login page
- [ ] Can register a new user (or user exists in database)
- [ ] Can login successfully
- [ ] Dashboard loads after login
- [ ] No console errors in browser
- [ ] No errors in backend logs

## 📝 Documentation Review

- [ ] Read `QUICK_START.md`
- [ ] Read `IMPLEMENTATION_SUMMARY.md`
- [ ] Read `backend/README_MIGRATIONS.md`
- [ ] Read `backend/README_TESTS.md`
- [ ] Understand project structure

## 🎯 Production Readiness (When Deploying)

- [ ] `ENVIRONMENT=production` in `.env`
- [ ] Secure `SECRET_KEY` generated
- [ ] `DEBUG=false`
- [ ] Database migrations tested
- [ ] All environment variables set
- [ ] Reverse proxy configured (nginx)
- [ ] HTTPS enabled
- [ ] Monitoring/logging set up
- [ ] Backup strategy in place
- [ ] Security headers configured

## 🐛 Troubleshooting

If something doesn't work:

1. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check `DATABASE_URL` format
   - Ensure database exists
   - Check user permissions

2. **Import Errors**
   - Verify virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check Python path

3. **TypeScript Errors**
   - Run `npm install` in frontend
   - Check `tsconfig.json` settings
   - Verify all types are imported correctly

4. **CORS Issues**
   - Check `allow_origins` in `backend/app/main.py`
   - Verify frontend URL matches

5. **Migration Issues**
   - Review migration files
   - Check database connection
   - Verify models match migration

## 📞 Next Steps

Once everything is checked:

1. Start developing features
2. Add more tests
3. Set up CI/CD (optional)
4. Deploy to staging environment
5. Deploy to production

---

**Note**: Keep this checklist updated as you add new features or configurations!

