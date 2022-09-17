from django import forms




class userLogin(forms.Form):
    username = forms.CharField(max_length=100,required=True,widget= forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':' username','id':'signinSrusername','tabindex':'1','aria-label':'username'}))
    password = forms.CharField(max_length=100,required=True,widget=forms.PasswordInput(attrs={'class':'js-toggle-password form-control form-control-lg','placeholder':'  password','id':'signupSrPassword','placeholder':'3+ characters required','aria-label':'3+ characters required','minlength':'3','data-hs-toggle-password-options':'''{
                           "target": "#changePassTarget",
                           "defaultClass": "bi-eye-slash",
                           "showClass": "bi-eye",
                           "classChangeTarget": "#changePassIcon"
                         }'''}))


    