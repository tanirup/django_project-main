from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.db import connection
from django.contrib.auth.models import User
from .models import Item
from .forms import ItemUpdateForm
from .models import Customer, Employee
from .forms import CustomerForm, EmployeeForm, EmployeeUpdateForm
from datetime import datetime
from django.db import transaction
from django.contrib.auth import authenticate, login, logout

# =============================
# index
# =============================
def index(request):
    return render(request, "psys/index.html")


# =============================
# Auth
# =============================
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("psys:login")
    else:
        form = UserCreationForm()
    return render(request, "psys/signup.html", {"form": form})

# =============================
# Login
# =============================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()  # 従業員ID
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("psys:employee_list")  # ログイン後の遷移先
        else:
            messages.error(request, "従業員ID または パスワードが違います。")

    return render(request, "psys/login.html")

# =============================
# Main Menu
# =============================
@login_required
def MainMenu(request):
    return render(request, "psys/MainMenu.html")


@login_required
def CustomerReportMenu(request):
    return render(request, "psys/CustomerReportMenu.html")


# =============================
# Employee: 一覧
# =============================
@login_required
def employee_list(request):
    employees = Employee.objects.all().order_by("employee_no")
    return render(request, "psys/EmployeeList.html", {"employees": employees})


# =============================
# Employee: 新規登録
# =============================
@login_required
def employee_regist(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()

            username = employee.employee_no
            raw_password = (employee.password or "").strip()

            if not raw_password:
                form.add_error("password", "ログイン用パスワードを入力してください。")
                return render(request, "psys/EmployeeRegist.html", {"form": form})

            # auth_user を作成/更新
            user, _ = User.objects.get_or_create(username=username)
            user.first_name = employee.employee_name or ""
            user.set_password(raw_password)  # ★必ずハッシュ化して保存
            user.is_active = True
            user.save()

            messages.success(request, "従業員を登録しました。ログアウト後、このIDでログインできます。")
            return redirect("psys:employee_list")
    else:
        form = EmployeeForm()

    return render(request, "psys/EmployeeRegist.html", {"form": form})


# =============================
# Employee: 編集
# =============================
@login_required
def employee_update(request, employee_no):
    employee = get_object_or_404(Employee, employee_no=employee_no)

    if request.method == "POST":
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            updated = form.save()

            # Django認証Userも更新（username=従業員番号）
            user, _ = User.objects.get_or_create(username=updated.employee_no)
            user.first_name = updated.employee_name or ""

            raw_password = (updated.password or "").strip()
            if raw_password:
                user.set_password(raw_password)
            user.save()

            messages.success(request, "従業員情報を更新しました。")
            return redirect("psys:employee_list")
    else:
        form = EmployeeUpdateForm(instance=employee)

    return render(request, "psys/EmployeeUpdate.html", {"form": form, "employee": employee})


# =============================
# Employee: 削除
# =============================
@login_required
def employee_delete(request, employee_no):
    if request.method == "POST":
        employee = get_object_or_404(Employee, employee_no=employee_no)

        employee.delete()
        User.objects.filter(username=employee_no).delete()

        messages.success(request, f"従業員 {employee_no} を削除しました。")

    return redirect("psys:employee_list")



# =============================
# Customer: 管理メニュー
# =============================
@login_required
def CustomerManagementMenu(request):
    customers = Customer.objects.filter(delete_flag=False)
    return render(request, "psys/CustomerManagementMenu.html", {"customers": customers})


# =============================
# Customer: 一覧 / 検索
# =============================
@login_required
def customer_list(request):
    customers = Customer.objects.filter(delete_flag=False)
    return render(request, "psys/CustomerList.html", {"customers": customers})


@login_required
def customer_search(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = (
            Customer.objects.filter(delete_flag=False)
            .filter(
                Q(customer_code__icontains=query)
                | Q(customer_name__icontains=query)
                | Q(customer_address__icontains=query)
                | Q(customer_telno__icontains=query)
                | Q(customer_postalcode__icontains=query)
            )
        )

    return render(request, "psys/CustomerSearch.html", {"results": results, "query": query})


# =============================
# Customer: 登録 / 更新
# =============================
@login_required
def customer_regist(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["customer_code"]

            with transaction.atomic():
                # 同じコードの顧客を探す
                existing = Customer.objects.filter(customer_code=code).first()

                if existing:
                    if existing.delete_flag:
                        # 🔁 削除済みなら「復活」させる
                        for field, value in form.cleaned_data.items():
                            setattr(existing, field, value)

                        existing.delete_flag = False
                        existing.is_ok = False  # 必要なら初期化
                        existing.save()
                    else:
                        # ❌ 生きてる顧客がいる = 被り
                        form.add_error(
                            "customer_code",
                            "この顧客IDはすでに使用されています"
                        )
                        return render(
                            request,
                            "psys/CustomerRegist.html",
                            {"form": form},
                        )
                else:
                    # 🆕 完全新規
                    obj = form.save(commit=False)
                    obj.delete_flag = False
                    obj.save()

            return redirect("psys:MainMenu")
    else:
        form = CustomerForm()

    return render(request, "psys/CustomerRegist.html", {"form": form})


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "更新しました。")
            return redirect("psys:customer_list")
    else:
        form = CustomerForm(instance=customer)

    return render(request, "psys/CustomerUpdate.html", {"form": form, "customer": customer})


@login_required
def customer_update_inline(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        customer.customer_name = request.POST.get("customer_name", "")
        customer.customer_telno = request.POST.get("customer_telno", "")
        customer.customer_postalcode = request.POST.get("customer_postalcode", "")
        customer.customer_address = request.POST.get("customer_address", "")
        customer.is_ok = request.POST.get("is_ok") == "on"
        customer.save()
        messages.success(request, "更新しました。")

    return redirect("psys:customer_list")


# =============================
# Customer: 削除（Mysqlから完全削除）
# =============================
@login_required
def customer_delete(request, code):
    customer = get_object_or_404(Customer, customer_code=code)

    if request.method == "POST":
        customer_name = customer.customer_name
        customer.delete()  # ← これが MySQL から完全削除
        messages.success(request, f"{customer_name} を削除しました。")

    return redirect("psys:customer_list")


# =============================
# Customer: 得意先別集計
# =============================
@login_required
def customer_summary(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                o.customer_code,
                COUNT(o.order_no) AS total_count,
                COALESCE(SUM(o.total_price), 0) AS total_amount
            FROM orders o
            GROUP BY o.customer_code
        """)
        rows = cursor.fetchall()

    agg_map = {code: {"total_count": cnt, "total_amount": amt} for code, cnt, amt in rows}

    customers = Customer.objects.filter(delete_flag=False).order_by("customer_code")

    summary_list = []
    for c in customers:
        agg = agg_map.get(c.customer_code, {"total_count": 0, "total_amount": 0})
        summary_list.append({
            "customer_code": c.customer_code,
            "customer_name": c.customer_name,
            "total_count": agg["total_count"],
            "total_amount": agg["total_amount"],
        })

    summary_list.sort(key=lambda x: x["total_amount"], reverse=True)

    return render(request, "psys/customer_summary.html", {"summary_list": summary_list})

# =============================
# Item: 一覧 / 更新
# =============================

@login_required
def item_list(request):
    q = request.GET.get("q", "").strip()
    stock_lt = request.GET.get("stock_lt", "").strip()

    # 期間（任意）
    date_from = request.GET.get("from", "").strip()  # 例: 2016-01-01
    date_to = request.GET.get("to", "").strip()      # 例: 2016-12-31

    items = Item.objects.all().order_by("item_code")

    if q:
        items = items.filter(Q(item_code__icontains=q) | Q(item_name__icontains=q))

    if stock_lt.isdigit():
        items = items.filter(stock__lt=int(stock_lt))

    # ざっくり在庫指標（詰め込み）
    total_items = Item.objects.count()
    low_stock_count = Item.objects.filter(stock__lt=50).count()
    out_of_stock_count = Item.objects.filter(stock=0).count()

    # -----------------------------
    # 売れ筋・売上ランキング（SQL）
    # order_details と item をJOIN
    # 期間指定があれば orders.order_date で絞る
    # -----------------------------
    params = []
    date_where = ""

    def is_valid_date(s: str) -> bool:
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return True
        except Exception:
            return False

    if date_from and is_valid_date(date_from):
        date_where += " AND o.order_date >= %s "
        params.append(date_from)
    if date_to and is_valid_date(date_to):
        date_where += " AND o.order_date <= %s "
        params.append(date_to)

    with connection.cursor() as cursor:
        # 商品別集計（数量・金額）
        cursor.execute(f"""
            SELECT
              d.item_code,
              i.item_name,
              COALESCE(SUM(d.order_num), 0) AS total_qty,
              COALESCE(SUM(d.order_num * d.order_price), 0) AS total_sales
            FROM order_details d
            JOIN item i ON i.item_code = d.item_code
            JOIN orders o ON o.order_no = d.order_no
            WHERE 1=1
            {date_where}
            GROUP BY d.item_code, i.item_name
        """, params)
        rows = cursor.fetchall()

    # rows: [(code, name, qty, sales), ...]
    sales_list = [
        {"item_code": r[0], "item_name": r[1], "total_qty": int(r[2] or 0), "total_sales": int(r[3] or 0)}
        for r in rows
    ]

    # ランキング作成（上位10）
    top_by_qty = sorted(sales_list, key=lambda x: x["total_qty"], reverse=True)[:10]
    top_by_sales = sorted(sales_list, key=lambda x: x["total_sales"], reverse=True)[:10]

    context = {
        "items": items,
        "q": q,
        "stock_lt": stock_lt,
        "date_from": date_from,
        "date_to": date_to,
        "total_items": total_items,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "top_by_qty": top_by_qty,
        "top_by_sales": top_by_sales,
        "sales_list": sales_list,  # 一覧として出したければ使える
    }
    return render(request, "psys/ItemList.html", context)


@login_required
def item_update(request, item_code):
    item = get_object_or_404(Item, pk=item_code)

    if request.method == "POST":
        form = ItemUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "商品情報を更新しました。")
            return redirect("psys:item_list")
    else:
        form = ItemUpdateForm(instance=item)

    return render(request, "psys/ItemUpdate.html", {
        "form": form,
        "item": item,
    })