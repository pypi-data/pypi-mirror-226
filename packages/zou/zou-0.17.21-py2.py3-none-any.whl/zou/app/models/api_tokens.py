from sqlalchemy_utils import (
    UUIDType,
    EmailType,
    LocaleType,
    TimezoneType,
    ChoiceType,
)
from sqlalchemy.dialects.postgresql import JSONB

from pytz import timezone as pytz_timezone
from babel import Locale

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin
from zou.app import config


department_link = db.Table(
    "department_link",
    db.Column(
        "person_id",
        UUIDType(binary=False),
        db.ForeignKey("person.id"),
        primary_key=True,
    ),
    db.Column(
        "department_id",
        UUIDType(binary=False),
        db.ForeignKey("department.id"),
        primary_key=True,
    ),
)


class ApiToken(db.Model, BaseMixin, SerializerMixin):
    """
    Describe a member of the studio (and an API user).
    """

    name = db.Column(db.String(80), nullable=False)
    email = db.Column(EmailType)

    active = db.Column(db.Boolean(), default=True)
    archived = db.Column(db.Boolean(), default=False)
    last_presence = db.Column(db.Date())

    timezone = db.Column(
        TimezoneType(backend="pytz"),
        default=pytz_timezone(config.DEFAULT_TIMEZONE),
    )
    locale = db.Column(LocaleType, default=Locale("en", "US"))
    role = db.Column(db.String(30), default="user")
    has_avatar = db.Column(db.Boolean(), default=False)

    notifications_enabled = db.Column(db.Boolean(), default=False)

    departments = db.relationship(
        "Department", secondary=department_link, lazy="joined"
    )

    def __repr__(self):
        return "<ApiToken %s>" % self.full_name()

    def full_name(self):
        return self.name

    def serialize(self, obj_type="ApiToken", relations=False):
        data = SerializerMixin.serialize(self, "ApiToken", relations=relations)
        data["full_name"] = self.full_name()
        return data

    def serialize_safe(self, relations=False):
        data = SerializerMixin.serialize(self, "ApiToken", relations=relations)
        data["full_name"] = self.full_name()
        data["fido_devices"] = self.fido_devices()
        del data["password"]
        del data["totp_secret"]
        del data["email_otp_secret"]
        del data["otp_recovery_codes"]
        del data["fido_credentials"]
        return data

    def present_minimal(self, relations=False):
        data = SerializerMixin.serialize(self, "Person", relations=relations)
        return {
            "id": data["id"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "full_name": self.full_name(),
            "has_avatar": data["has_avatar"],
            "active": data["active"],
            "departments": data.get("departments", []),
            "role": data["role"],
            "desktop_login": data["desktop_login"],
        }

    def set_departments(self, department_ids):
        from zou.app.models.department import Department

        self.departments = []
        for department_id in department_ids:
            department = Department.get(department_id)
            if department is not None:
                self.departments.append(department)
        self.save()

    @classmethod
    def create_from_import(cls, person):
        del person["type"]
        del person["full_name"]
        is_update = False
        previous_person = cls.get(person["id"])

        if "password" in person and person["password"] is not None:
            person["password"] = person["password"].encode()

        department_ids = None
        if "departments" in person:
            department_ids = person.pop("departments", None)

        if previous_person is None:
            previous_person = cls.create(**person)
        else:
            is_update = True
            previous_person.update(person)

        if department_ids is not None:
            previous_person.set_departments(department_ids)

        return (previous_person, is_update)
