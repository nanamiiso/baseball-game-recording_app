from django.shortcuts import render, redirect
from .forms import EventForm
from django.http import JsonResponse
from .models import Event
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from .forms import EventEditForm
from django.contrib.auth.decorators import login_required


def calendar_view(request):
    if request.method == 'POST':
        # POSTされたデータからフォームを作成
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
                'id': event.id,
                'title': f"{event.home_team} vs {event.away_team}",  # イベントのタイトル
                'start': event.date.strftime("%Y-%m-%d") + "T" + event.start_time.strftime("%H:%M:%S"),  # 開始時刻をISO8601形式に
                'url': reverse('event_details', args=[event.id])  # イベントの詳細ページへのURL
            })
        except ObjectDoesNotExist:
            # 関連オブジェクトが存在しない場合は、ログにエラーを記録
            logger.error(f"イベント {event.id} の取得に失敗しました。関連するオブジェクトが存在しません。")
            
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
            form.save()
            # 成功のメッセージを追加
            messages.success(request, 'イベントが更新されました。')
            return redirect('event_details', event_id=event.id)
    else:
        form = EventEditForm(instance=event)

    return render(request, 'calendar/edit_event.html', {'form': form, 'event': event})


def top_page(request):
    return render(request, 'portfolio/top_page.html')
