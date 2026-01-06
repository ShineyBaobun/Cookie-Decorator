import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import Mapped

Base = so.declarative_base()

class users(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement = True)
    username: so.Mapped[str] = so.mapped_column(unique=True)
    password: so.Mapped[str] 
    coins: so.Mapped[int]
    chocolatechipsadd: so.Mapped[bool]
    sprinklesadd: so.Mapped[bool]
    oats: so.Mapped[bool]
    raisins: so.Mapped[bool]
    coffee: so.Mapped[bool]
    vanilla: so.Mapped[bool]
    nuts: so.Mapped[bool]
    cocoapowder: so.Mapped[bool]
    icing: so.Mapped[bool]
    sprinklestop: so.Mapped[bool]
    chocolatechiptop: so.Mapped[bool]
    nutella: so.Mapped[bool]
    peanutbutter: so.Mapped[bool]
    candycanes: so.Mapped[bool]
    fruit: so.Mapped[bool]
    marshmallows: so.Mapped[bool]
    hersheykisses: so.Mapped[bool]
    jollyranchers: so.Mapped[bool]
    twizzlers: so.Mapped[bool]
    reesespieces: so.Mapped[bool]
    cottoncandy: so.Mapped[bool]
    popcorn: so.Mapped[bool]