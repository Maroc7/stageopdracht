from website.database import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(500), nullable=False, default=name)

    def is_active(self):
        return True

    @staticmethod
    def create_profile_with_user(name, role):
        profile = Profile(name=name, role=role)
        db.session.add(profile)
        db.session.commit()
        return profile
    
    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True if self.id else False

    def is_anonymous(self):
        return False