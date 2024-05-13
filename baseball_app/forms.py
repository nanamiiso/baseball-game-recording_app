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
    def clean_home_team(self):
        home_team = self.cleaned_data.get('home_team')
        away_team = self.cleaned_data.get('away_team')
        if home_team == away_team:
            raise forms.ValidationError('ホームチームとアウェイチームは同じチームを選択できません。')
        return home_team

    def clean_away_team(self):
        home_team = self.cleaned_data.get('home_team')
        away_team = self.cleaned_data.get('away_team')
        if home_team == away_team:
            raise forms.ValidationError('ホームチームとアウェイチームは同じチームを選択できません。')
        return away_team  
    
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        # start_time が正しい形式であることを確認するカスタムバリデーションロジックをここに追加
        return start_time
    
    

class EventEditForm(forms.ModelForm):
    home_score = forms.IntegerField(label='ホームスコア', min_value=0)
    away_score = forms.IntegerField(label='アウェイスコア', min_value=0)
    comment = forms.CharField(widget=forms.Textarea, required=False, label='コメント')  # コメントも任意

    class Meta:
        model = Event
        fields = ['date', 'home_team', 'away_team', 'stadium', 'start_time', 'home_score', 'away_score', 'comment']
        fields = '__all__'
        # フィールドの入力ウィジェットをカスタマイズする場合は、widgets を使います
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }  
    

class CombinedScoreForm(forms.ModelForm):
    combined_score = forms.CharField(label='スコア', max_length=100)

    class Meta:
        model = Event
        fields = ['combined_score']

    def __init__(self, *args, **kwargs):
        super(CombinedScoreForm, self).__init__(*args, **kwargs)
        if self.instance:
            home_score = self.instance.home_score
            away_score = self.instance.away_score
            combined_score = f"{home_score} - {away_score}"
            self.initial['combined_score'] = combined_score

    def save(self, commit=True):
        home_score, away_score = map(int, self.cleaned_data['combined_score'].split('-'))
        self.instance.home_score = home_score
        self.instance.away_score = away_score
        if commit:
            self.instance.save()
        return self.instance

