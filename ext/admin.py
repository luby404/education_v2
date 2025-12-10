import os

from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask_admin.form.upload import ImageUploadField, FileUploadField
from wtforms import PasswordField

from ext.models import (
    db,
    Usuarios,
    Cursos,
    Modulos,
    Aulas,
    Progresso,
    Assinatura,
)


class BaseAdminView(ModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True

    create_modal = True
    edit_modal = True

    form_excluded_columns = ("senha", "is_ative", "criado_em", "atualizado_em")
    

    


class UsuariosAdmin(BaseAdminView):
    column_list = ("id", "nome", "emial", "user_type", "is_ative", "criado_em")
    column_searchable_list = ("nome", "emial")
    column_filters = ("user_type", "is_ative")
    
    form_extra_fields = {
        "senha": PasswordField("Senha (defina somente para alterar)")
    }

    def on_model_change(self, form, model, is_created):
        senha = None
        try:
            senha = form.senha.data
        except Exception:
            senha = None

        if senha:
            model.set_password(senha)


class CursosAdmin(BaseAdminView):
    column_list = ("id", "nome", "price", "desconto", "is_ative", "criado_em")
    column_searchable_list = ("nome",)
    #column_filters = ("is_ative",)
    # `capa` será um upload de imagem salvo em `uploads/cursos/`
    form_extra_fields = {}


class ModulosAdmin(BaseAdminView):
    column_list = ("id", "nome", "curso", "is_ative", "criado_em")
    column_searchable_list = ("nome",)
    #column_filters = ("curso",)


class AulasAdmin(BaseAdminView):
    column_list = ("id", "titulo", "modulo", "is_ative", "criado_em")
    column_searchable_list = ("titulo",)
    #column_filters = ("modulo",)
    # `video` será um upload de ficheiro salvo em `uploads/videos/`
    form_extra_fields = {}
    


class ProgressoAdmin(BaseAdminView):
    column_list = ("id", "aluno", "curso", "aula", "is_ative", "criado_em")
    #column_filters = ("aluno", "curso")
    


class AssinaturaAdmin(BaseAdminView):
    column_list = ("id", "aluno", "curso", "price", "data", "dias", "is_ative")
    #column_filters = ("aluno", "curso")
    


def init_admin(app):
    # Preparar diretórios de upload (projeto root /uploads)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    uploads_root = os.path.join(project_root, "uploads")
    cursos_upload = os.path.join(uploads_root, "cursos")
    videos_upload = os.path.join(uploads_root, "videos")

    os.makedirs(cursos_upload, exist_ok=True)
    os.makedirs(videos_upload, exist_ok=True)

    # Configurar campos de upload para as views
    CursosAdmin.form_extra_fields = {
        "capa": ImageUploadField(
            "Capa",
            base_path=cursos_upload,
            url_relative_path=os.path.join("uploads", "cursos"),
            allowed_extensions=("jpg", "jpeg", "png", "gif"),
        )
    }

    AulasAdmin.form_extra_fields = {
        "video": FileUploadField(
            "Vídeo",
            base_path=videos_upload,
            allowed_extensions=("mp4", "webm", "ogg", "mov", "avi"),
        )
    }

    admin = Admin(app, name="Painel")

    admin.add_view(UsuariosAdmin(Usuarios))
    admin.add_view(CursosAdmin(Cursos))
    admin.add_view(ModulosAdmin(Modulos))
    admin.add_view(AulasAdmin(Aulas))
    admin.add_view(ProgressoAdmin(Progresso))
    admin.add_view(AssinaturaAdmin(Assinatura))

    return admin



