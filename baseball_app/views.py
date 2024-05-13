from django.shortcuts import render, redirect
from .forms import EventForm
from django.http import JsonResponse
from .models import Event
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotAllowed,HttpResponseBadRequest
from django.contrib import messages
from .forms import EventEditForm
from django.contrib.auth.decorators import login_required
from .models import Team, Stadium



def calendar_view(request):
    if request.method == 'POST':
        # POSTされたデータからフォームを作成python manage.py runserver
        form = EventForm(request.POST)
        if form.is_valid():
            # フォームのデータが有効であればイベントを保存
            events = form.save(commit=False)

            events.save()
            # イベントの詳細ページにリダイレクト
            return JsonResponse({'status': 'success'})
        else:
            # データにエラーがあれば、エラー情報をレスポンスとして返す
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        # GETリクエストの場合は、空のフォームを作成
        form = EventForm()

    # エラーなしでページをレンダリングする
    return render(request, 'calendar/calendar.html', {'form': form})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  # ログインユーザーをイベントの所有者として設定
            event.save()
            events = Event.objects.filter(user=request.user)
            return redirect('calendar')
    else:
        form = EventForm()  # GETリクエストの場合にフォームを生成
    return render(request, 'calendar/add_event.html', {'form': form})

@login_required
def get_events(request):
    events = Event.objects.filter(user=request.user)
    event_data = []
    for event in events:
        try:
            # イベントオブジェクトから情報を取得し、event_data リストに追加
            event_data.append({
                'id': event.pk,
                'title': f"{event.home_team} vs {event.away_team}",  # イベントのタイトル
                'start': event.date.strftime("%Y-%m-%d") + "T" + event.start_time.strftime("%H:%M:%S"),  # 開始時刻をISO8601形式に
                'url': reverse('event_details', args=[event.pk])  # イベントの詳細ページへのURL
            })
        except ObjectDoesNotExist:
            # 関連オブジェクトが存在しない場合は、ログにエラーを記録
            logger.error(f"イベント {event.pk} の取得に失敗しました。関連するオブジェクトが存在しません。")
            
    # JSONとしてevent_dataをレスポンスに
    return JsonResponse(event_data, safe=False)


def event_details(request, event_id):
    # 指定されたIDを持つイベントを取得
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'calendar/details_event.html', {'event': event})

def delete_event(request, event_id):
    if request.method == 'POST':
        # イベントオブジェクトを取得、存在しない場合は404エラー
        event = get_object_or_404(Event, pk=event_id)
        event.delete()  # イベントを削除
        messages.success(request, 'イベントが削除されました。')  # オプション: ユーザーにメッセージを表示
        return redirect('calendar') # カレンダーのビュー名にリダイレクト
    else:
        # POST以外のメソッドでアクセスされた場合はエラーを返す
        return HttpResponseNotAllowed(['POST'])
    
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            home_score = form.cleaned_data.get('home_score')
            away_score = form.cleaned_data.get('away_score')
            score = f"{home_score} - {away_score}"
            form.save()
            # 成功のメッセージを追加
            messages.success(request, 'イベントが更新されました。')
            return redirect('event_details', event_id=event.pk)

    else:
        form = EventEditForm(instance=event)

    return render(request, 'calendar/edit_event.html', {'form': form, 'event': event})


def top_page(request):
    return render(request, 'portfolio/top_page.html')
 
def search(request):
    if request.method == 'GET':
        # チームと球場のリストを取得
        teams = Team.objects.all()
        stadiums = Stadium.objects.all()
        
        # テンプレートに渡すコンテキストを定義
        context = {
            'teams_list': teams,
            'stadiums_list': stadiums,
        }
        
        # 検索結果をテンプレートに渡して表示
        return render(request, 'calendar/search.html', context)
    else:
        return HttpResponseBadRequest('Unsupported request method')




@login_required
def search_result(request):
    if request.method == 'GET' or request.method == 'POST':
        # ユーザーがログインしているかをチェック
        if request.user.is_authenticated:
            # ユーザーがログインしている場合、そのユーザーが関連するイベントを取得
            events = Event.objects.filter(user=request.user)
        else:
            # ユーザーがログインしていない場合、すべてのイベントを取得
            events = Event.objects.all()
        
        # 検索フォームから送信されたデータを取得
        start_date = request.POST.get('start_date', request.GET.get('start_date'))
        end_date = request.POST.get('end_date', request.GET.get('end_date'))
        home_team_id = request.POST.get('home_team', request.GET.get('home_team'))
        away_team_id = request.POST.get('away_team', request.GET.get('away_team'))
        stadium_id = request.POST.get('stadium', request.GET.get('stadium'))
        
        # 検索条件を使用してイベントをフィルタリング
        if start_date:
            events = events.filter(date__gte=start_date)
        if end_date:
            events = events.filter(date__lte=end_date)
        if home_team_id and home_team_id != 'all':
            events = events.filter(home_team_id=home_team_id)
        if away_team_id and away_team_id != 'all':
            events = events.filter(away_team_id=away_team_id)
        if stadium_id and stadium_id != 'all':
            events = events.filter(stadium_id=stadium_id)
        
        # 検索結果をテンプレートに渡して表示
        return render(request, 'calendar/search_result.html', {'events': events})
    else:
        return HttpResponseBadRequest('Unsupported request method')







@login_required
def show_event(request, event_id):
    # イベントの識別子を使用して、特定のイベントを取得
    event = get_object_or_404(Event, id=event_id)
    
    # 特定のイベントをテンプレートに渡して表示
    return render(request, 'calendar/show_event.html', {'event': event})



def events_details(request, event_id):
    events = Event.objects.get(id=event_id)
    return render(request, 'calendar/details_event.html', {'events': events})