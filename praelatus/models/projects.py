from base import Base

# TODO add roles as a through relationship
class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    name = Column(String)
    key = Column(String)
    homepage = Column(String)
    icon_url = Column(String)
    repo = Columng(String)

    lead_id = Column(Integer, ForeignKey('users.id'))
    lead = relationship('User')

    permission_scheme_id = Column(Integer,
                                  ForeignKey('permission_schemes.id'))
    permission_scheme = relationship('PermissionScheme')

    def __repr__(self):
        return "Project(id=%d, key=%s)" % (self.id, self.key)
