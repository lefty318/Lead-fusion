from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Dict, Any
import pandas as pd
import io
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Conversation, Message, Lead, AnalyticsEvent, User
from ..services import AuthService

router = APIRouter()
auth_service = AuthService()

@router.get("/dashboard")
async def get_dashboard_data(
    days: int = 30,
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get dashboard analytics data"""
    if not auth_service.check_permissions(current_user, "analyst"):
        raise HTTPException(status_code=403, detail="Not authorized")

    start_date = datetime.utcnow() - timedelta(days=days)

    # Conversation metrics
    total_conversations = db.query(Conversation).filter(
        Conversation.created_at >= start_date
    ).count()

    conversations_by_channel = db.query(
        Conversation.channel,
        func.count(Conversation.id).label('count')
    ).filter(
        Conversation.created_at >= start_date
    ).group_by(Conversation.channel).all()

    conversations_by_status = db.query(
        Conversation.status,
        func.count(Conversation.id).label('count')
    ).filter(
        Conversation.created_at >= start_date
    ).group_by(Conversation.status).all()

    # Lead metrics
    total_leads = db.query(Lead).filter(
        Lead.created_at >= start_date
    ).count()

    leads_by_status = db.query(
        Lead.status,
        func.count(Lead.id).label('count')
    ).filter(
        Lead.created_at >= start_date
    ).group_by(Lead.status).all()

    # Average response time (simplified)
    avg_response_time = db.query(
        func.avg(
            func.extract('epoch', Message.sent_at - Conversation.timestamp)
        )
    ).join(Message, Message.conversation_id == Conversation.id).filter(
        Conversation.created_at >= start_date,
        Message.direction == 'outbound'
    ).scalar()

    # Conversion funnel
    conversion_data = {
        "conversations": total_conversations,
        "leads": total_leads,
        "qualified_leads": db.query(Lead).filter(
            Lead.created_at >= start_date,
            Lead.status == "qualified"
        ).count(),
        "converted": db.query(Lead).filter(
            Lead.created_at >= start_date,
            Lead.status == "converted"
        ).count()
    }

    return {
        "total_conversations": total_conversations,
        "conversations_by_channel": dict(conversations_by_channel),
        "conversations_by_status": dict(conversations_by_status),
        "total_leads": total_leads,
        "leads_by_status": dict(leads_by_status),
        "avg_response_time_hours": avg_response_time / 3600 if avg_response_time else 0,
        "conversion_funnel": conversion_data
    }

@router.get("/export/{format}")
async def export_analytics(
    format: str,
    days: int = 30,
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Export analytics data"""
    if not auth_service.check_permissions(current_user, "analyst"):
        raise HTTPException(status_code=403, detail="Not authorized")

    start_date = datetime.utcnow() - timedelta(days=days)

    # Get conversation data
    conversations = db.query(Conversation).filter(
        Conversation.created_at >= start_date
    ).all()

    # Convert to DataFrame
    data = []
    for conv in conversations:
        data.append({
            "id": conv.id,
            "channel": conv.channel,
            "sender_name": conv.sender_name,
            "lead_score": conv.lead_score,
            "sentiment": conv.sentiment,
            "intent": conv.intent,
            "status": conv.status,
            "created_at": conv.created_at,
            "assigned_to": conv.assigned_to
        })

    df = pd.DataFrame(data)

    if format.lower() == "csv":
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=analytics_{days}days.csv"}
        )

    elif format.lower() == "xlsx":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Conversations', index=False)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=analytics_{days}days.xlsx"}
        )

    elif format.lower() == "pdf":
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        output = io.BytesIO()
        c = canvas.Canvas(output, pagesize=letter)

        # Simple PDF generation
        c.drawString(100, 750, f"OmniLead Analytics Report - Last {days} days")
        c.drawString(100, 720, f"Total Conversations: {len(df)}")

        c.save()
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=analytics_{days}days.pdf"}
        )

    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use csv, xlsx, or pdf")

@router.get("/performance")
async def get_performance_metrics(
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get user performance metrics"""
    if not auth_service.check_permissions(current_user, "analyst"):
        raise HTTPException(status_code=403, detail="Not authorized")

    # Agent performance
    agent_performance = db.query(
        User.full_name,
        func.count(Conversation.id).label('conversations_handled'),
        func.avg(Conversation.lead_score).label('avg_lead_score')
    ).join(Conversation, Conversation.assigned_to == User.id).group_by(User.id, User.full_name).all()

    return {
        "agent_performance": [
            {
                "agent": perf[0],
                "conversations_handled": perf[1],
                "avg_lead_score": float(perf[2]) if perf[2] else 0.0
            } for perf in agent_performance
        ]
    }