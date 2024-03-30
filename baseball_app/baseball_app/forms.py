from django import forms
from .models import Event, Team, Stadium


class EventForm(forms.ModelForm):
    home_team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='ホームチーム',
        empty_label=None  # デフォルト選択なし
    )
    away_team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='アウェイチーム',
        empty_label=None
    )
    stadium = forms.ModelChoiceField(
        queryset=Stadium.objects.all(),
        label='球場',
        empty_label=None
    )

    class Meta:
        model = Event
        fields = ['date', 'home_team', 'away_team', 'stadium', 'start_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        # start_time が正しい形式であることを確認するカスタムバリデーションロジックをここに追加
        return start_time

class EventEditForm(forms.ModelForm):
    score = forms.CharField(required=False, label='スコア')  # スコアは任意
    comment = forms.CharField(widget=forms.Textarea, required=False, label='コメント')  # コメントも任意

    class Meta:
        model = Event
        fields = ['date', 'home_team', 'away_team', 'stadium', 'start_time', 'score', 'comment']
        # フィールドの入力ウィジェットをカスタマイズする場合は、widgets を使います
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }  
    
