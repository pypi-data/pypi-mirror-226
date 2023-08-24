# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AppointmentType(models.Model):
    _name = "appointment_type"
    _inherit = [
        "appointment_type",
    ]

    task_type_id = fields.Many2one(
        string="Task Type",
        comodel_name="task.type",
    )
    task_stage_id = fields.Many2one(
        string="Task Stage",
        comodel_name="project.task.type",
    )
    host_task_type_id = fields.Many2one(
        string="Task Type Host",
        comodel_name="task.type",
        required=False,
    )
    co_appointee_task_type_id = fields.Many2one(
        string="Task Type Co Appointee",
        comodel_name="task.type",
        required=False,
    )
