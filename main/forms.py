from ajax_select.fields import AutoCompleteSelectField
from django.forms import ModelForm, Form, DateInput, CharField, PasswordInput

from biblioteca_pessoal import settings
from main.models import Usuario, Leitura, Livro


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'skoob_user', 'contato', 'groups', 'is_active',
                  'is_superuser']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UsuarioForm, self).save(commit=False)

        if not user.pk:
            user.set_password(settings.DEFAULT_PASSWORD)  # Set de default password
            user.is_staff = True
        if commit:
            user.save()
        return user


class LeituraForm(ModelForm):
    class Meta:
        model = Leitura
        fields = ['livro', 'usuario', 'data']
        widgets = {
            'data': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LeituraForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['usuario'].queryset = Usuario.objects.filter(id=user.id)
        self.fields['livro'].queryset = Livro.objects.filter(id=self.instance.livro.id)


class MesclarAutoresForm(Form):
    autor_primario = AutoCompleteSelectField('autores', help_text="Selecione o autor que continuará existindo", show_help_text=False)
    autor_secundario = AutoCompleteSelectField('autores', help_text="Selecione o autor que deixará de existir", show_help_text=False)


class MesclarEditorasForm(Form):
    editora_primaria = AutoCompleteSelectField('editoras', help_text="Selecione a editora que continuará existindo", show_help_text=False)
    editora_secundaria = AutoCompleteSelectField('editoras', help_text="Selecione a editora que deixará de existir", show_help_text=False)


class PasswordForm(ModelForm):
    senha = CharField(widget=PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super(PasswordForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
