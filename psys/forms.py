from django import forms
from .models import Customer, Employee

from .models import Item

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["item_name", "price", "stock"]

    def clean_price(self):
        v = self.cleaned_data.get("price")
        if v is not None and v < 0:
            raise forms.ValidationError("価格は0以上で入力してください。")
        return v

    def clean_stock(self):
        v = self.cleaned_data.get("stock")
        if v is not None and v < 0:
            raise forms.ValidationError("在庫は0以上で入力してください。")
        return v

class EmployeeForm(forms.ModelForm):
    """登録用（従業員番号も入力）"""
    class Meta:
        model = Employee
        fields = ["employee_no", "employee_name", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_employee_no(self):
        v = (self.cleaned_data.get("employee_no") or "").strip()
        if len(v) != 6:
            raise forms.ValidationError("従業員番号は6文字で入力してください。")
        return v

    def clean_password(self):
        v = (self.cleaned_data.get("password") or "").strip()
        if v and len(v) > 8:
            raise forms.ValidationError("パスワードは8文字以内で入力してください。")
        return v


class EmployeeUpdateForm(forms.ModelForm):
    """編集用（従業員番号は変更させない）"""
    class Meta:
        model = Employee
        fields = ["employee_name", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_password(self):
        v = (self.cleaned_data.get("password") or "").strip()
        if v and len(v) > 8:
            raise forms.ValidationError("パスワードは8文字以内で入力してください。")
        return v


# 🔍 検索フォーム（1つに統合）
class CustomerSearchForm(forms.Form):
    keyword = forms.CharField(label="キーワード", required=False)


# 📝 編集フォーム（Customer）
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "customer_code",
            "customer_name",
            "customer_telno",
            "customer_postalcode",
            "customer_address",
            "discount_rate",
            "is_ok",
        ]
        labels = {
            "customer_code": "得意先コード",
            "customer_name": "得意先名",
            "customer_telno": "電話番号",
            "customer_postalcode": "郵便番号",
            "customer_address": "住所",
            "is_ok": "OK欄",
        }
