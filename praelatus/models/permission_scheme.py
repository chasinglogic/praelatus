from base import Base

# TODO handle permissions
class PermissionScheme(Base):
    __tablename__ = 'permission_schemes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
