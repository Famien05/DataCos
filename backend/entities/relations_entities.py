from sqlalchemy import Column, Integer, ForeignKey, Date, String
from database import Base

class User_Groups(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id_group'), nullable=False)
    added_date = Column(Date, nullable=False)

class Add_User_Requests(Base):
    __tablename__ = "add_user_requests"

    id_request = Column(Integer, primary_key=True, index=True)
    uid_admin = Column(String, ForeignKey('admins.uid_admin'), nullable=False)
    uid_user = Column(String, ForeignKey('users.uid_user'), nullable=False)
    tenant_id = Column(Integer, ForeignKey('tenants.id_tenant'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id_group'), nullable=False)
    request_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
