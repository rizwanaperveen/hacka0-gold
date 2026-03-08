"""
Invoicing Skill - Atomic invoicing operations

Provides core invoicing functionality:
- Create invoices
- Send invoices
- Track payments
- Generate reports
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from skills.base_skill import BaseSkill


class InvoicingSkill(BaseSkill):
    """
    Atomic skill for invoicing operations.

    This skill provides low-level invoicing functionality
    for business financial operations.
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("invoicing")
        self.config = config or {}
        self.invoices = {}  # In-memory storage (replace with database)

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute an invoicing operation."""
        if action == "create_invoice":
            return await self.create_invoice(**kwargs)
        elif action == "send_invoice":
            return await self.send_invoice(**kwargs)
        elif action == "mark_paid":
            return await self.mark_paid(**kwargs)
        elif action == "get_invoice":
            return await self.get_invoice(**kwargs)
        else:
            return {"status": "error", "error": f"Unknown action: {action}"}

    async def create_invoice(
        self,
        client_name: str,
        client_email: str,
        amount: float,
        description: str,
        due_date: str
    ) -> Dict[str, Any]:
        """Create a new invoice."""
        try:
            invoice_id = f"inv_{datetime.now().timestamp()}"

            invoice = {
                "invoice_id": invoice_id,
                "client_name": client_name,
                "client_email": client_email,
                "amount": amount,
                "description": description,
                "due_date": due_date,
                "created_at": datetime.now().isoformat(),
                "status": "draft"
            }

            self.invoices[invoice_id] = invoice
            self.logger.info(f"Created invoice: {invoice_id}")

            await self._track_execution(True)

            return {
                "status": "success",
                "invoice_id": invoice_id,
                "invoice": invoice
            }

        except Exception as e:
            self.logger.error(f"Failed to create invoice: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def send_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Send an invoice to client."""
        try:
            if invoice_id not in self.invoices:
                return {"status": "error", "error": "Invoice not found"}

            invoice = self.invoices[invoice_id]
            invoice["status"] = "sent"
            invoice["sent_at"] = datetime.now().isoformat()

            self.logger.info(f"Sent invoice: {invoice_id}")
            await self._track_execution(True)

            return {
                "status": "success",
                "invoice_id": invoice_id,
                "sent_to": invoice["client_email"]
            }

        except Exception as e:
            self.logger.error(f"Failed to send invoice: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def mark_paid(self, invoice_id: str) -> Dict[str, Any]:
        """Mark an invoice as paid."""
        try:
            if invoice_id not in self.invoices:
                return {"status": "error", "error": "Invoice not found"}

            invoice = self.invoices[invoice_id]
            invoice["status"] = "paid"
            invoice["paid_at"] = datetime.now().isoformat()

            self.logger.info(f"Marked invoice as paid: {invoice_id}")
            await self._track_execution(True)

            return {
                "status": "success",
                "invoice_id": invoice_id,
                "paid": True
            }

        except Exception as e:
            self.logger.error(f"Failed to mark invoice as paid: {str(e)}")
            await self._track_execution(False)
            return {"status": "error", "error": str(e)}

    async def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get invoice details."""
        try:
            if invoice_id not in self.invoices:
                return {"status": "error", "error": "Invoice not found"}

            return {
                "status": "success",
                "invoice": self.invoices[invoice_id]
            }

        except Exception as e:
            self.logger.error(f"Failed to get invoice: {str(e)}")
            return {"status": "error", "error": str(e)}
