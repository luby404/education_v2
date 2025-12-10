# Arquivo de Models
from peewee import (
    CharField,
    IntegerField,
    DateTimeField,
    TextField,
    ForeignKeyField,
    DecimalField,
    BooleanField,
    SqliteDatabase,
    Model
)
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SqliteDatabase("banco.db")


class BaseModel(Model):
    
    is_ative      = BooleanField(default=True)
    criado_em     = DateTimeField(default=datetime.now)
    atualizado_em = DateTimeField(default=datetime.now)

    def save(self, *args, **kayargs):
        self.atualizado_em = datetime.now()
        return super().save(*args, **kayargs)

    class Meta:
        database = db



class Usuarios(BaseModel, UserMixin):
    nome  = CharField()
    emial = CharField(unique=True)
    senha = CharField()

    user_type = CharField(
        choices=[
            ("admin", "admin"),
            ("aluno", "aluno"),
            ("educador", "educador"),
        ],
        default="aluno"
    )

    def check_password(self, senha:str):
        return check_password_hash(self.senha, senha)
    
    def set_password(self, senha):
        self.senha = generate_password_hash(senha)
        return self.senha

    def __str__(self):
        return self.nome


class Cursos(BaseModel):
    nome      = CharField(unique=True)
    capa      = CharField(max_length=300)
    descricao = TextField(verbose_name="Descrição")
    price     = DecimalField(max_digits=16, decimal_places=2, verbose_name="preço")
    desconto  = IntegerField(default=0)

    def __str__(self):
        return self.nome



class Modulos(BaseModel):
    nome  = CharField()
    curso = ForeignKeyField(Cursos, backref="modulos")

    def __str__(self):
        return f"{self.curso} -> {self.nome}"

class Aulas(BaseModel):
    modulo    = ForeignKeyField(Modulos, backref="aulas")
    titulo    = CharField()
    descricao = TextField(null=True)
    video     = CharField()

    def __str__(self):
        return f"{self.modulo.curso} - {self.modulo} - {self.titulo}"


class Progresso(BaseModel):
    aluno = ForeignKeyField(Usuarios, backref="progresso")
    curso = ForeignKeyField(Cursos, backref="progresso")
    aula  = ForeignKeyField(Aulas, backref="progresso")


class Assinatura(BaseModel):
    aluno = ForeignKeyField(Usuarios, backref="assinatura")
    curso = ForeignKeyField(Cursos, backref="assinatura")
    price = DecimalField(max_digits=16, decimal_places=2, verbose_name="preço")

    data  = DateTimeField(default=datetime.now)
    dias  = IntegerField(default=60)

    def __str__(self):
        return self.aluno


def init_db():
    db.connect()
    with db:
        db.create_tables([ Usuarios, Cursos, Modulos, Aulas, Assinatura, Progresso ])
