# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class AppointmentSchedule(models.Model):
    _name = "appointment_schedule"
    _inherit = [
        "appointment_schedule",
    ]

    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
    )
    auto_create_task = fields.Boolean(
        string="Auto Create Task",
    )
    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task",
    )
    host_task_id = fields.Many2one(
        comodel_name="project.task",
        string="Task Host",
        required=False,
    )
    co_appointee_task_ids = fields.Many2many(
        comodel_name="project.task",
        string="Co-Appointees Task",
        relation="rel_co_appointees_2_project_task",
        column1="co_appointee_ids",
        column2="task_id",
        required=False,
    )

    def action_create_task(self):
        for record in self.sudo():
            record._create_task()
            record._create_host()
            record._create_co_appointee()

    def action_delete_task(self):
        for record in self.sudo():
            record._delete_task()
            record._delete_host()
            record._delete_co_appointee()

    def _delete_task(self):
        self.ensure_one()
        task = self.task_id

        if not task:
            return True

        self.write({"task_id": False})
        task.unlink()

    # CREATE TASK FOR APPOINTEE
    def _prepare_create_task(self):
        self.ensure_one()
        return {
            "name": self.name,
            "project_id": self.project_id.id,
            "type_id": self.type_id.task_type_id.id,
            "user_id": self.appointee_id.id,
            "timebox_ids": self._get_task_timebox(),
            "stage_id": self.type_id.task_stage_id
            and self.type_id.task_stage_id.id
            or False,
            "work_estimation": self.type_id.task_type_id.work_estimation,
        }

    def _create_task(self):
        self.ensure_one()
        Task = self.env["project.task"]
        if not self.auto_create_task:
            return True

        task = Task.create(self._prepare_create_task())
        self.write({"task_id": task.id})

    # CREATE TASK FOR HOST
    def _prepare_create_host(self):
        self.ensure_one()
        return {
            "name": self.name,
            "project_id": self.project_id.id,
            "type_id": self.type_id.host_task_type_id.id,
            "user_id": self.host_id.id,
            "timebox_ids": self._get_task_timebox(),
            "stage_id": self.type_id.task_stage_id
            and self.type_id.task_stage_id.id
            or False,
            "work_estimation": self.type_id.host_task_type_id.work_estimation,
        }

    def _create_host(self):
        self.ensure_one()
        Task = self.env["project.task"]
        if not self.auto_create_task or not self.host_id:
            return True

        task = Task.create(self._prepare_create_host())
        self.write({"host_task_id": task.id})

    # CREATE TASK FOR CO-APPOINTEES
    def _prepare_create_co_appointee(self, user_id):
        self.ensure_one()
        return {
            "name": self.name,
            "project_id": self.project_id.id,
            "type_id": self.type_id.co_appointee_task_type_id.id,
            "user_id": user_id,
            "timebox_ids": self._get_task_timebox(),
            "stage_id": self.type_id.task_stage_id
            and self.type_id.task_stage_id.id
            or False,
            "work_estimation": self.type_id.co_appointee_task_type_id.work_estimation,
        }

    def _create_co_appointee(self):
        self.ensure_one()
        task_ids = []
        Task = self.env["project.task"]
        if not self.auto_create_task:
            return True

        for co_appointee in self.co_appointee_ids:
            task = Task.create(self._prepare_create_co_appointee(co_appointee.id))
            task_ids.append(task.id)
        self.write({"co_appointee_task_ids": [(6, 0, task_ids)]})

    def _get_task_timebox(self):
        self.ensure_one()
        Timebox = self.env["task.timebox"]
        criteria = [
            ("date_start", "<=", self.date),
            ("date_end", ">=", self.date),
            ("state", "!=", "done"),
        ]
        timeboxes = Timebox.search(criteria)

        if len(timeboxes) == 0:
            error_message = _(
                """
            Context: Create task from appointment schedule
            Database ID: %s
            Problem: No timebox
            Solution: Create timebox
            """
                % (self.id)
            )
            raise ValidationError(error_message)

        return [(6, 0, timeboxes.ids)]

    def _delete_host(self):
        self.ensure_one()
        host_task_id = self.host_task_id

        if not host_task_id:
            return True

        self.write({"host_task_id": False})
        host_task_id.unlink()

    def _delete_co_appointee(self):
        self.ensure_one()
        co_appointee_task_ids = self.co_appointee_task_ids

        if not co_appointee_task_ids:
            return True

        self.write({"co_appointee_task_ids": False})
        co_appointee_task_ids.unlink()
