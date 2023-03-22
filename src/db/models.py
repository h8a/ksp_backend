import uuid

import sqlalchemy as sa

from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import select


SAModel = declarative_base()


class Base(object):
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    create_date = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    status = sa.Column(sa.String(2), default='1')

    @classmethod
    async def get(cls, session, **kwargs):
        result = None

        async with session.begin():
            query = select(cls).filter_by(**kwargs)
            result = (await session.execute(query)).scalars()
            result = result.first()

        return result

    async def save(self, session):
        async with session.begin():
            session.add(self)
            await session.flush()
            await session.refresh(self, attribute_names=['id'])
            await session.commit()

        return self

    @classmethod
    async def update(cls, session, id, **kwargs):
        async with session.begin():
            query = (
                sqlalchemy_update(cls).where(cls.id == id)
                           .values(**kwargs)
                           .execution_options(synchronize_session='fetch')
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_list_by(cls, session, **kwargs):
        result = None

        async with session.begin():
            query = select(cls).filter_by(**kwargs).order_by(cls.create_date.desc())
            result = (await session.execute(query)).scalars()
            result = result.all()
            

        return result

    @classmethod
    async def get_list_with_childrens_by(cls, session, **kwargs):
        async with session.begin():
            query = select(cls).filter_by(**kwargs)\
                                .order_by(cls.create_date.desc())\
                                .options(selectinload(cls.employees_beneficiaries))
            result = (await session.execute(query)).scalars()
            result = result.all()
        return result



class EmployeesModel(SAModel, Base):

    __tablename__ = 'employees'
    __mapper_args__ = {"eager_defaults": True}

    hire_date = sa.Column(sa.DateTime(timezone=True), nullable=False)
    job = sa.Column(sa.String(255), nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    salary = sa.Column(sa.Integer, nullable=False)
    employees_beneficiaries = relationship("EmployeesBeneficiariesModel")


    def __init__(self, hire_date, job, name, salary, id=None, status=None):
        self.id = id
        self.status = status
        self.hire_date = hire_date
        self.job = job
        self.name = name
        self.salary = salary

    @property
    def as_dict_with_children(self):
        return {
            'id': str(self.id),
            'status': self.status,
            'hire_date': self.hire_date.strftime('%Y-%M-%d'),
            'job': self.job,
            'name': self.name,
            'salary': self.salary,
            'beneficiaries': [{
                'id': str(beneficiary.id),
                'name': beneficiary.name,
                'birthdate': beneficiary.birthdate.strftime('%Y-%M-%d'),
                'gender': beneficiary.gender,
            } for beneficiary in self.employees_beneficiaries]
        }

    @property
    def as_dict(self):
        return {
            'id': str(self.id),
            'status': self.status,
            'hire_date': self.hire_date.strftime('%Y-%M-%d'),
            'job': self.job,
            'name': self.name,
            'salary': self.salary
        }


class EmployeesBeneficiariesModel(SAModel, Base):

    __tablename__ = 'employees_beneficiaries'

    name = sa.Column(sa.String(255), nullable=False)
    relationship = sa.Column(sa.String(255), nullable=False)
    birthdate = sa.Column(sa.DateTime, nullable=False)
    gender = sa.Column(sa.String(1), nullable=False)
    employee_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("employees.id"))

    def __init__(self, name, relationship, birthdate, gender, employee_id, id=None, status=None) -> None:
        self.id = id
        self.status = status
        self.name = name
        self.relationship = relationship
        self.birthdate = birthdate
        self.gender = gender
        self.employee_id = employee_id

    @property
    def as_dict(self):
        return {
            'id': str(self.id),
            'status': self.status,
            'name': self.name,
            'relationship': self.relationship,
            'birthdate': self.birthdate.strftime('%Y-%M-%d'),
            'gender': self.gender
        }
