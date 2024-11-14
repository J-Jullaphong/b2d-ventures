from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from ..models import Investor
from ..forms import InvestorProfileForm


class InvestorProfileView(View):
    """View to manage investor profile updates."""
    template_name = 'b2d/investor_profile.html'

    def get(self, request):
        """Handles the GET request to display the investor profile form."""
        try:
            investor = Investor.objects.get(id=request.user.id)
        except Investor.DoesNotExist:
            messages.error(request, "Investor profile not found.")
            return redirect("b2d:home")

        form = InvestorProfileForm(instance=investor)
        context = {
            'form': form,
            'investor': investor,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Handles the POST request to update investor profile information."""
        try:
            investor = Investor.objects.get(id=request.user.id)
        except Investor.DoesNotExist:
            messages.error(request, "Investor profile not found.")
            return redirect("b2d:home")

        form = InvestorProfileForm(request.POST, request.FILES,
                                   instance=investor)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("b2d:investor_profile")

        messages.error(request,
                       "There was an error updating your profile. Please check the form and try again.")
        context = {
            'form': form,
            'investor': investor,
        }
        return render(request, self.template_name, context)

