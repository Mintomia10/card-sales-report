from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from .models import CardSale


def home(request):

    # =========================
    # ADD NEW RECORD
    # =========================
    if request.method == 'POST':

        operator_name = request.POST.get('operator_name')
        transaction_type = request.POST.get('transaction_type')
        card_quantity = int(request.POST.get('card_quantity'))

        CardSale.objects.create(
            operator_name=operator_name,
            transaction_type=transaction_type,
            card_quantity=card_quantity
        )

        return redirect('home')

    # =========================
    # ALL RECORDS
    # =========================
    records = CardSale.objects.all().order_by('-date', '-time')

    # =========================
    # SEARCH OPERATOR
    # =========================
    search = request.GET.get('search', '').strip()

    if search:
        records = records.filter(
            operator_name__icontains=search
        )

    # =========================
    # MONTH FILTER
    # =========================
    selected_month = request.GET.get('month', '').strip()

    if selected_month:
        try:
            year, month = selected_month.split('-')

            records = records.filter(
                date__year=int(year),
                date__month=int(month)
            )
        except ValueError:
            pass

    # =========================
    # TOTAL CARDS
    # =========================
    total_cards = records.aggregate(
        total=Sum('card_quantity')
    )['total'] or 0

    # =========================
    # TOTAL AMOUNT
    # =========================
    total_amount = records.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # =========================
    # SALE CARDS
    # =========================
    sale_cards = records.filter(
        transaction_type='Sale'
    ).aggregate(
        total=Sum('card_quantity')
    )['total'] or 0

    # =========================
    # REPLACE CARDS
    # =========================
    replace_cards = records.filter(
        transaction_type='Replace'
    ).aggregate(
        total=Sum('card_quantity')
    )['total'] or 0

    # =========================
    # DAMAGE CARDS
    # =========================
    damage_cards = records.filter(
        transaction_type='Damage'
    ).aggregate(
        total=Sum('card_quantity')
    )['total'] or 0

    # =========================
    # OPERATOR REPORT
    # =========================

    operator_names = [
        'MD. Minto Mia',
        'Sompa Rani',
        'Proxy Operator'
    ]

    operators = []

    for name in operator_names:

        operator_records = records.filter(
            operator_name=name
        )

        operator_cards = operator_records.aggregate(
            total=Sum('card_quantity')
        )['total'] or 0

        operator_amount = operator_records.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        operators.append({
            'name': name,
            'cards': operator_cards,
            'amount': operator_amount,
        })

    # =========================
    # CURRENT MONTH
    # =========================

    today = timezone.localdate()

    current_month_records = CardSale.objects.filter(
        date__year=today.year,
        date__month=today.month
    )

    current_month_cards = current_month_records.aggregate(
        total=Sum('card_quantity')
    )['total'] or 0

    current_month_amount = current_month_records.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # =========================
    # SEND DATA TO HTML
    # =========================

    context = {
        'records': records,

        'total_cards': total_cards,
        'total_amount': total_amount,

        'sale_cards': sale_cards,
        'replace_cards': replace_cards,
        'damage_cards': damage_cards,

        'operators': operators,

        'current_month_cards': current_month_cards,
        'current_month_amount': current_month_amount,

        'selected_month': selected_month,
        'search': search,
    }

    return render(request, 'home.html', context)