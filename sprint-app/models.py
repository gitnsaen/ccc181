from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Database models (SQLAlchemy 2.0 style)
class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service", passive_deletes=True)


class Operator(db.Model):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="operator")


class Ticket(db.Model):
    __tablename__ = "tickets"
    __table_args__ = (
        CheckConstraint("sent_via IN ('gmail', 'fb')", name="check_ticket_sent_via"),
        CheckConstraint("pages > 0", name="check_ticket_positive_pages"),
        CheckConstraint("pages_type IN ('all', 'specific')", name="check_ticket_pages_type"),
        CheckConstraint("print_type IN ('bw', 'color')", name="check_ticket_print_type"),
        CheckConstraint("paper_size IN ('letter', 'a4', 'legal')", name="check_ticket_paper_size"),
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'unreadable')",
            name="check_ticket_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    student_id: Mapped[str] = mapped_column(String(20), nullable=False)
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"), nullable=False
    )
    operator_id: Mapped[int | None] = mapped_column(
        ForeignKey("operators.id", ondelete="SET NULL"), nullable=True
    )
    sent_via: Mapped[str] = mapped_column(String(20), nullable=False)
    doc_name: Mapped[str] = mapped_column(Text, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    pages_type: Mapped[str] = mapped_column(String(20), nullable=False)
    pages_range: Mapped[str | None] = mapped_column(String(100), nullable=True)
    print_type: Mapped[str] = mapped_column(String(10), nullable=False)
    paper_size: Mapped[str] = mapped_column(String(20), nullable=False, server_default="letter")
    is_rush: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    served_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    service: Mapped["Service"] = relationship(back_populates="tickets")
    operator: Mapped["Operator | None"] = relationship(back_populates="tickets")
