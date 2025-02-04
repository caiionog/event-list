import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def premium_payment(request):
    if request.method == 'POST':
        # Cria um charge no Stripe
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=29000,  # Valor em centavos (R$10.00)
                currency='brl',
                description='Assinatura Premium',
                source=token,
            )
            # Atualiza o usuário para premium
            user = CustomUser.objects.get(id=request.user.id)
            user.is_premium = True
            user.save()
            messages.success(request, 'Pagamento realizado com sucesso! Agora você é um usuário premium.')
            return redirect('feed:index')  # Redireciona para a página inicial ou outra página de sua escolha
        except stripe.error.CardError as e:
            messages.error(request, 'Erro no pagamento: ' + str(e))
            return redirect('premium_payment')
    return render(request, 'services/premium_payment.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })