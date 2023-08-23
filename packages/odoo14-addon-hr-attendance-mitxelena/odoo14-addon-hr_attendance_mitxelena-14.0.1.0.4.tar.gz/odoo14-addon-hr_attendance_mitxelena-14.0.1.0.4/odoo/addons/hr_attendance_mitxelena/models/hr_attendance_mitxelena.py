from odoo import api, fields, models, _
from datetime import timedelta
from pytz import timezone
from logging import getLogger
_logger = getLogger(__name__)


class HrAttendanceMitxelena(models.Model):
    _inherit = 'hr.attendance'

    is_holiday = fields.Boolean(compute='_compute_is_holiday', store=True)
    shift_type = fields.Selection([
        ('', _('Unknown')),
        ('morning', _('Morning')),
        ('afternoon', _('Afternoon')),
        ('night', _('Night')),
    ], compute='_compute_shift_type', store=True)

    consecutive_days = fields.Integer(
        compute='_compute_consecutive_days', store=True, default=1)

    @api.depends('check_in')
    def _compute_is_holiday(self):
        holiday_model = self.env['hr.holidays.public']
        for record in self:
            if record.check_in:
                # Check if the check_in date is a public holiday
                record.is_holiday = holiday_model.is_public_holiday(
                    record.check_in.date())
            else:
                # If there is no check_in, we can't compute if it's a holiday
                record.is_holiday = False

    @api.depends('check_out')
    def _compute_shift_type(self):
        # Get user timezone, or use Europe/Madrid as default
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        for record in self:
            if record.check_in and record.check_out:
                # Convert check_in and check_out to local time
                check_in = record.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    shift_type = 'morning'
                elif 13 <= hour < 21:
                    shift_type = 'afternoon'
                else:
                    shift_type = 'night'
                record.shift_type = shift_type

    @api.depends('check_in', 'shift_type', 'worked_hours')
    def _compute_consecutive_days(self):
        for record in self:

            # If there is no check_in, set consecutive days to 0
            # and break the loop
            if not record.check_in:
                record.consecutive_days = 0
                break

            # Get the last 7 days range
            datetime_end = record.check_in
            datetime_start = datetime_end - timedelta(days=6)

            # Only select attendances where worked_hours > 0.5 hours
            # to avoid erroneous short attendances
            attendance_records = self.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', datetime_start),
                ('check_in', '<=', datetime_end),
                ('worked_hours', '>', 0.5)
            ], order='check_in desc')

            # Init inner-loop variables
            previous_record = None
            consecutive_days = 1
            _logger.debug('[%s][%i][Init] Counting consecutive days',
                          record.id, consecutive_days)

            # If there are no attendance records, set consecutive days to 1
            # and break the loop
            if len(attendance_records) == 0:
                record.consecutive_days = 1
                break

            # Iterate over the past attendance records
            for rec in attendance_records:
                _logger.debug(
                    '[%s] Checking past attendance %s', record.id, rec)

                # If there is no previous record, set it to the current one
                # and continue the loop
                if not previous_record:
                    previous_record = rec
                    continue

                check_in_date = rec.check_in.date()
                previous_check_in_date = previous_record.check_in.date()

                # If the previous record it's not within the last day
                # break the loop and stop counting consecutive days
                is_consecutive = (previous_check_in_date -
                                  check_in_date) <= timedelta(days=1)

                if not is_consecutive:
                    _logger.debug(
                            '[%s] Records are not consecutive (%s)',
                            record.id, rec.id)
                    break

                # If the previous record it's on the same day
                # check if the start time of the check in of the previous record
                # is at least 7 hours after the end of the current record
                # and if the worked hours of the last shift of the day
                # are at least 2 hours
                if previous_check_in_date == check_in_date:
                    if rec.worked_hours < 2:
                        _logger.debug(
                            '[%s] Same day, but less than 2 hours worked (%s)',
                            record.id, rec.id)
                        break

                    time_difference = previous_record.check_in - rec.check_out

                    if (time_difference >= timedelta(hours=7)):                        
                        _logger.debug(
                            '[%s] Same day, but more than 7 hours difference',
                            record.id)
                        
                        consecutive_days += 1

                        _logger.debug(
                            '[%s] so, +1 consecutive days: %i',
                            record.id, consecutive_days)
                else:
                    # In any other case, add a consecutive day
                    consecutive_days += 1
                    _logger.debug('[%s] +1 consecutive days: %i',
                                  record.id, consecutive_days)

                # Set the previous record to the current one
                previous_record = rec

            # Set the final consecutive days count to the record
            record.consecutive_days = consecutive_days

            print("[%s][%i][Final] Consecutive days for %s has ended." %
                  (record.id, consecutive_days, record.employee_id.name))

    def recompute_all(self):
        # Get all records  from hr.attendance and iterate over them
        attendance_records = self.env['hr.attendance'].search([])
        _logger.debug('Attendance records: %s', attendance_records)
        for record in attendance_records:
            _logger.debug('Updating is_holiday for %s', record)
            record.is_holiday = record._compute_is_holiday()
            _logger.debug('Is holiday: %s', record.is_holiday)
            record.shift_type = record._compute_shift_type()
            _logger.debug('Shift type: %s', record.shift_type)

    def recompute_shifts(self):
        tz = timezone(self.env.user.tz or 'Europe/Madrid')
        attendance_records = self.env['hr.attendance'].search(
            [["consecutive_days", "=", 0]])
        _logger.debug('Attendance records: %s', attendance_records)
        for record in attendance_records:
            try:
                check_in = record.check_in.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                check_out = record.check_out.replace(
                    tzinfo=timezone('UTC')).astimezone(tz)
                midpoint = check_in + (check_out - check_in) / 2
                hour = midpoint.hour
                if 5 <= hour < 13:
                    shift_type = 'morning'
                elif 13 <= hour < 21:
                    shift_type = 'afternoon'
                else:
                    shift_type = 'night'
                record.shift_type = shift_type
                _logger.debug('Shift type %s for %s', shift_type, record)
                if record.shift_type != shift_type:
                    _logger.error('Shift type is %s for %s',
                                  record.shift_type, record)
                record._compute_consecutive_days()
            except Exception as e:
                _logger.error(
                    'Error computing shift type for %s: %s', record, e)
