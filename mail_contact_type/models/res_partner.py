# Copyright 2023 Foodles (https://www.foodles.com/)
# @author Pierre Verkest <pierreverkest84@gmail.com>
# @author Matthias Barkat <matthias.barkat@foodles.co>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    mail_contact_type_ids = fields.Many2many(
        "mail.contact.type",
        string="Mail Contact Types",
        help="Used by email template to select contacts by mail contact type",
    )

    def _find_contacts_by_mail_contact_types(self, codes):
        return (
            self.commercial_partner_id.child_ids | self.commercial_partner_id
        ).filtered(
            lambda contact: any(
                contact.mail_contact_type_ids.filtered(
                    lambda contact_type: contact_type.code in codes
                )
            )
        )

    def contact_by_types(self, *codes):
        return ",".join(
            [
                str(contact.id)
                for contact in self._find_contacts_by_mail_contact_types(codes)
            ]
        )
