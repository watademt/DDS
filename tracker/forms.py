from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        trans_type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        # Валидация: Категория должна относиться к выбранному типу
        if category and trans_type and category.type != trans_type:
            self.add_error('category', f'Категория "{category.name}" не относится к типу "{trans_type.name}".')

        # Валидация: Подкатегория должна относиться к выбранной категории
        if subcategory and category and subcategory.category != category:
            self.add_error('subcategory', f'Подкатегория "{subcategory.name}" не относится к категории "{category.name}".')

        return cleaned_data