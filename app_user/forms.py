from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class QuestionnaireForm(forms.Form):
    QUESTION_CHOICES_1 = [
        ('a', 'A real gambler'),
        ('b', 'Willing to take risks after completing adequate research'),
        ('c', 'Cautious'),
        ('d', 'A real risk avoider')
    ]

    QUESTION_CHOICES_2 = [
        ('a', '$1,000 in cash'),
        ('b', 'A 50% chance at winning $5,000'),
        ('c', 'A 25% chance at winning $10,000'),
        ('d', 'A 5% chance at winning $100,000')
    ]

    QUESTION_CHOICES_3 = [
        ('a', 'Cancel the vacation'),
        ('b', 'Take a much more modest vacation'),
        ('c', 'Go as scheduled, reasoning that you need the time to prepare for a job search'),
        ('d', 'Extend your vacation, because this might be your last chance to go first-class')
    ]

    QUESTION_CHOICES_4 = [
        ('a', 'Deposit it in a bank account, money market account, or insured CD'),
        ('b', 'Invest it in safe high-quality bonds or bond mutual funds'),
        ('c', 'Invest it in stocks or stock mutual funds')
    ]

    QUESTION_CHOICES_5 = [
        ('a', 'Not at all comfortable'),
        ('b', 'Somewhat comfortable'),
        ('c', 'Very comfortable')
    ]

    QUESTION_CHOICES_6 = [
        ('a', 'Loss'),
        ('b', 'Uncertainty'),
        ('c', 'Opportunity'),
        ('d', 'Thrill')
    ]

    QUESTION_CHOICES_7 = [
        ('a', 'Hold the bonds'),
        ('b', 'Sell the bonds, put half the proceeds into money market accounts, and the other half into hard assets'),
        ('c', 'Sell the bonds and put the total proceeds into hard assets'),
        ('d', 'Sell the bonds, put all the money into hard assets, and borrow additional money to buy more')
    ]

    QUESTION_CHOICES_8 = [
        ('a', '$200 gain best case; $0 gain/loss worst case'),
        ('b', '$800 gain best case, $200 loss worst case'),
        ('c', '$2,600 gain best case, $800 loss worst case'),
        ('d', '$4,800 gain best case, $2,400 loss worst case')
    ]

    QUESTION_CHOICES_9 = [
        ('a', 'A sure gain of $500'),
        ('b', 'A 50% chance to gain $1,000 and a 50% chance to gain nothing')
    ]

    QUESTION_CHOICES_10 = [
        ('a', 'A sure loss of $500'),
        ('b', 'A 50% chance to lose $1,000 and a 50% chance to lose nothing')
    ]

    QUESTION_CHOICES_11 = [
        ('a', 'A savings account or money market mutual fund'),
        ('b', 'A mutual fund that owns stocks and bonds'),
        ('c', 'A portfolio of 15 common stocks'),
        ('d', 'Commodities like gold, silver, and oil')
    ]

    QUESTION_CHOICES_12 = [
        ('a', '60% in low-risk investments, 30% in medium-risk investments, 10% in high-risk investments'),
        ('b', '30% in low-risk investments, 40% in medium-risk investments, 30% in high-risk investments'),
        ('c', '10% in low-risk investments, 40% in medium-risk investments, 50% in high-risk investments')
    ]

    QUESTION_CHOICES_13 = [
        ('a', 'Nothing'),
        ('b', 'One month’s salary'),
        ('c', 'Three month’s salary'),
        ('d', 'Six month’s salary')
    ]

    q1 = forms.ChoiceField(choices=QUESTION_CHOICES_1, widget=forms.RadioSelect,
                           label="1. In general, how would your best friend describe you as a risk taker?")
    q2 = forms.ChoiceField(choices=QUESTION_CHOICES_2, widget=forms.RadioSelect,
                           label="2. You are on a TV game show and can choose one of the following; which would you take?")
    q3 = forms.ChoiceField(choices=QUESTION_CHOICES_3, widget=forms.RadioSelect,
                           label="3. You have just finished saving for a 'once-in-a-lifetime' vacation. Three weeks before you plan to leave, you lose your job. You would:")
    q4 = forms.ChoiceField(choices=QUESTION_CHOICES_4, widget=forms.RadioSelect,
                           label="4. If you unexpectedly received $20,000 to invest, what would you do?")
    q5 = forms.ChoiceField(choices=QUESTION_CHOICES_5, widget=forms.RadioSelect,
                           label="5. In terms of experience, how comfortable are you investing in stocks or stock mutual funds?")
    q6 = forms.ChoiceField(choices=QUESTION_CHOICES_6, widget=forms.RadioSelect,
                           label="6. When you think of the word 'risk,' which of the following words comes to mind first?")
    q7 = forms.ChoiceField(choices=QUESTION_CHOICES_7, widget=forms.RadioSelect,
                           label="7. Some experts are predicting prices of assets such as gold, jewels, collectibles, and real estate (hard assets) to increase in value; bond prices may fall, however, experts tend to agree that government bonds are relatively safe. Most of your investment assets are now in high-interest government bonds. What would you do?")
    q8 = forms.ChoiceField(choices=QUESTION_CHOICES_8, widget=forms.RadioSelect,
                           label="8. Given the best and worst case returns of the four investment choices below, which would you prefer?")
    q9 = forms.ChoiceField(choices=QUESTION_CHOICES_9, widget=forms.RadioSelect,
                           label="9. In addition to whatever you own, you have been given $1,000. You are now asked to choose between:")
    q10 = forms.ChoiceField(choices=QUESTION_CHOICES_10, widget=forms.RadioSelect,
                            label="10. In addition to whatever you own, you have been given $2,000. You are now asked to choose between:")
    q11 = forms.ChoiceField(choices=QUESTION_CHOICES_11, widget=forms.RadioSelect,
                            label="11. Suppose a relative left you an inheritance of $100,000, stipulating in the will that you invest ALL the money in ONE of the following choices. Which one would you select?")
    q12 = forms.ChoiceField(choices=QUESTION_CHOICES_12, widget=forms.RadioSelect,
                            label="12. If you had to invest $20,000, which of the following investment choices would you find most appealing?")
    q13 = forms.ChoiceField(choices=QUESTION_CHOICES_13, widget=forms.RadioSelect,
                            label="13. Your trusted friend and neighbor, an experienced geologist, is putting together a group of investors to fund an exploratory gold mining venture. The venture could pay back 50 to 100 times the investment if successful. If the mine is a bust, the entire investment is worthless. Your friend estimates the chance of success is only 20%. If you had the money, how much would you invest?")


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = None
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
