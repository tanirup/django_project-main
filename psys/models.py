from django.db import models
from django.db.models import Sum, Count

class Item(models.Model):
    item_code = models.CharField(max_length=6, primary_key=True)
    item_name = models.CharField(max_length=32, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "item"

    def __str__(self):
        return f"{self.item_code} {self.item_name}"


class Employee(models.Model):
    employee_no = models.CharField(max_length=6, primary_key=True)
    employee_name = models.CharField(max_length=32, blank=True, null=True)
    password = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "employee"

    def __str__(self):
        return self.employee_name or self.employee_no

class Customer(models.Model):
    customer_code = models.CharField(max_length=10, primary_key=True)  # ★主キーを明示！
    customer_name = models.CharField(max_length=100)
    customer_telno = models.CharField(max_length=20, blank=True)
    customer_postalcode = models.CharField(max_length=10, blank=True)
    customer_address = models.CharField(max_length=200, blank=True)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    delete_flag = models.BooleanField(default=False)

    # 🆕 OK欄を追加！（ここだけ追加すればOK）
    is_ok = models.BooleanField(default=False)
   


    def __str__(self):
        return self.customer_name

    class Meta:
        managed = False  # 既存テーブルをそのまま使う
        db_table = 'customer'  # 使用するMySQLテーブル名
