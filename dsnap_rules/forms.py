from django import forms


class DisasterForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        benefit_begin_date = cleaned_data["benefit_begin_date"]
        benefit_end_date = cleaned_data["benefit_end_date"]
        if benefit_begin_date > benefit_end_date:
            self.add_error("benefit_begin_date", forms.ValidationError(
                    "Benefit begin date cannot be later than Benefit end date"
            ))


class ApplicationPeriodForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        begin_date = cleaned_data["begin_date"]
        end_date = cleaned_data["end_date"]
        if begin_date > end_date:
            self.add_error("begin_date", forms.ValidationError(
                    "Period begin date cannot be later than Period end date"
            ))
