# docker-django-celery-tutorial

 docker-django-celery-tutorial 基本教學  📝

* [Youtube Tutorial Part1 - Docker 安裝 RabbitMQ](https://youtu.be/W4ktp3EjFXY)

* [Youtube Tutorial Part2 - Python 結合 Celery ( 使用 Docker )](https://youtu.be/B8Qq9KxEjZc)

* [Youtube Tutorial Part3 - 實戰 Django + Celery ( 使用 Docker )](https://youtu.be/3dwRrJml2NQ)

之前其實也寫過相關的教學，可參考 [django-celery-tutorial](https://github.com/twtrubiks/django-celery-tutorial#django-celery-tutorial)，

那這邊為什麼還要再寫一篇文章介紹呢:question::question::question:

是因為接觸 docker 後，發現 docker 的好，不懂 docker 是什麼？

請參考 [docker-tutorial](https://github.com/twtrubiks/docker-tutorial):laughing:

所以這篇教大家用 docker 建立 Celery，如果你看過 [這篇](https://github.com/twtrubiks/django-celery-tutorial#broker-tutorial) 的介紹，

你會發現安裝環境很麻煩，尤其是在 Windows 上，更慘的是，

Celery [v4.1.0](https://github.com/celery/celery/releases/tag/v4.1.0) 不支援 Windows:sob:

所以這篇會全部使用 docker 來完成:smirk:

## 前言

這邊一些為什麼 Celery 要用 RabbitMQ 的問題就不再做介紹，詳細介紹

可參考 [django-celery-tutorial](https://github.com/twtrubiks/django-celery-tutorial):blush:

透過這篇文章，你將會學會

* [Docker 安裝 RabbitMQ](https://github.com/twtrubiks/docker-django-celery-tutorial#docker-%E5%AE%89%E8%A3%9D-rabbitmq)
* [Python 結合 Celery ( 使用 Docker )](https://github.com/twtrubiks/docker-django-celery-tutorial#python-%E7%B5%90%E5%90%88-celery)
* [實戰 Django + Celery ( 使用 Docker )](https://github.com/twtrubiks/docker-django-celery-tutorial#%E5%AF%A6%E6%88%B0-django--celery)

## Docker 安裝 RabbitMQ

* [Youtube Tutorial Part1 - Docker 安裝 RabbitMQ](https://youtu.be/W4ktp3EjFXY)

詳細教學可參考 [Docker RabbitMQ](https://hub.docker.com/_/rabbitmq/) ，請直接執行下列的指令，

```cmd
docker run -d --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=celery -e RABBITMQ_DEFAULT_PASS=password123  -e RABBITMQ_DEFAULT_VHOST=my_vhost -p 5672:5672 -p 15672:15672 rabbitmq:3.7.3-management
```

比較特別的是，`RABBITMQ_DEFAULT_VHOST` 這個東西，如果大家有興趣，可以 google **RabbitMQ virtual hosts**

進一步的去了解 :grinning:（ 或是有機會我有研究會再補上來 ），這邊我是安裝 rabbitmq:3.7.3-management 的版本，

所以有網頁可以觀看，可直接瀏覽
[http://localhost:15672/](http://localhost:15672/)

![alt tag](https://i.imgur.com/kunrVdl.png)

輸入你的帳密後，應該可以看到類似的畫面

![alt tag](https://i.imgur.com/C4sTKad.png)

接下來，我將介紹如何將 Celery 結合 Python :satisfied:

## Python 結合 Celery

建議搭配影片看比較好理解 :blush:

* [Youtube Tutorial Part2 - Python 結合 Celery ( 使用 Docker )](https://youtu.be/B8Qq9KxEjZc)

### Celery

Python 結合 Celery，可參考 [celery-demo](https://github.com/twtrubiks/docker-django-celery-tutorial/tree/master/celery-demo)，這邊要注意兩點，

第一，Docker 中的 RABBITMQ 請繼續執行著，不要關掉。

第二，請記得安裝 Celery Library 以及 SQLAlchemy ( 因為 result_backend 默認是用 ORM )。

也可以從 celery-demo/[requirements.txt](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/requirements.txt) 直接一次安裝，直接在 Terminal 執行以下指令

```cmd
pip install -r requirements.txt
```

上面這段指令，我已經包進去 celery-demo/[Dockerfile](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/Dockerfile) 了，

也用 docker 幫大家包成 celery-demo/[docker-compose.yml](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/docker-compose.yml) 了，所以直接執行以下指令即可

```cmd
docker-compose up
```

![alt tag](https://i.imgur.com/SEiVJu0.png)

這樣基本上就啟動成功了:smiley:

以下我將簡單介紹  [celery-demo](https://github.com/twtrubiks/docker-django-celery-tutorial/tree/master/celery-demo)  裡面的檔案，

celery_app/[__init__.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/celery_app/__init__.py)

```python
from celery import Celery

app = Celery('demo', broker='amqp://celery:password123@rabbitmq:5672/my_vhost')
app.config_from_object('celery_app.celery_config')
```

這邊主要是設定你的 broker （ 在這邊我們的 broker 就是 RABBITMQ ），

最後一行只是載入我們定義的 config 檔而已，

接著來看看 config 檔到底設定了什麼:wink:

celery_app/[celery_config.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/celery_app/celery_config.py)

```python
from datetime import timedelta

from celery.schedules import crontab

# Timezone
timezone = 'Asia/Taipei'

# import
imports = (
    'celery_app.tasks',
)

# result
result_backend = 'db+sqlite:///results.sqlite'

# schedules
beat_schedule = {
    'every-2-seconds': {
        'task': 'celery_app.tasks.add',
        'schedule': timedelta(seconds=2),
        'args': (5, 8)
    },
    'specified-time': {
        'task': 'celery_app.tasks.add',
        'schedule': crontab(hour=8, minute=50),
        'args': (50, 50)
    }

}
```

`imports` 的部份就是等等我會介紹的 celery-demo/[tasks.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/celery_app/tasks.py)。

`result_backend` 這部份的設定是可以將 Celery 執行的結果儲存起來。

`beat_schedule` 這部份的設定則是 schedule，schedule 後面我會再進一步介紹。

Celery 可以設定的參數非常多，詳細可參考 [configuration-and-defaults](http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration-and-defaults)。

接著來介紹 celery_app/[tasks.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/celery_app/tasks.py)

```python
import time

from celery_app import app


@app.task
def add(x, y):
    return x + y
```

這邊設定了一個很簡單的 task，那我要怎麼執行 :question::question: 請用你的 Terminal 執行這個 worker （很重要），

```cmd
celery -A celery_app worker -l info
```

上面這段指令，我已經包進去 celery-demo/[docker-compose.yml](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/docker-compose.yml) 的 command 了，

接著就可以在你的 Python Console ( docker 容器中 ) 開始玩  Celery 了 :satisfied:

在  Python Console 中我們輸入以下程式碼

```python
from celery_app.tasks import add
add.delay(2,2).get()
```

![alt tag](https://i.imgur.com/hZFWlUn.png)

執行後你會發現目錄中多出了 celery-demo/[results.sqlite](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/results.sqlite)，這個是我們前面所設定的 `result_backend`，

裡面存放著 Celery 的執行結果，

![alt tag](https://i.imgur.com/cunFhuo.png)

Celery 還有很多指令，像是 Chains , Groups , Chords 之類的，基本上就用我這個範例，

你就可以把其他的指令都玩玩看，可參考 [Canvas: Designing Work-flows](http://docs.celeryproject.org/en/latest/userguide/canvas.html)，

在我的 celery_app/[tasks.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/celery_app/tasks.py) 中，還有一段程式碼

```python
'''
ref. http://docs.celeryq.org/en/latest/userguide/tasks.html#avoid-launching-synchronous-subtasks
'''

def chain_demo(x, y):
    # add_demo ->  mul_demo -> insert_db_demo
    chain(add_demo.s(x, y), mul_demo.s(10), insert_db_demo.s())()


@app.task
def add_demo(x, y):
    time.sleep(3)
    return x + y


@app.task
def mul_demo(x, y):
    time.sleep(3)
    return x * y


@app.task(ignore_result=True)
def insert_db_demo(result):
    print('insert db , result {}'.format(result))

```

一樣記得要先啟動 worker，

```cmd
celery -A celery_app worker -l info
```

上面這段指令，我已經包進去 celery-demo/[docker-compose.yml](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/docker-compose.yml) 的 command 了，

在 Python Console ( docker 容器中 ) 輸入下方程式碼

```python
from celery_app.tasks import chain_demo
chain_demo(1,1)
```

![alt tag](https://i.imgur.com/PbEjh3s.png)

![alt tag](https://i.imgur.com/MvSByNV.png)

建議可以先去觀看一下 Celery 中的  [signatures](http://docs.celeryproject.org/en/latest/userguide/canvas.html#signatures)，不然你可能會看不懂這段 code，

Celery 的官方文件我覺得真的不錯，可以多看 :satisfied:

像這段程式碼，就是使用了 celery 中 chain 的概念，我簡單說明一下，這邊有三個 task ，

當我們執行 `chain_demo(1,1)` 的時候，會先執行 `add_demo` 並且回傳 2 ，接著 2 會被傳入

`mul_demo` ，這時候 x = 2，y = 10，回傳 2*10 = 20 ( 這邊補充一下，`time.sleep(3)` 的用意

是模擬這個 task 需要時間執行 )，最後再將 20 傳入 `insert_db_demo`。

這邊有一個裝飾器 `@app.task(ignore_result=True)` ，目的主要是忽略結果不寫入 [results.sqlite](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/results.sqlite)

，如果你的結果沒有很重要，可以加上這個裝飾器，避免不必要的開銷，可參考官方的說明

 [Ignore results you don't want](http://docs.celeryproject.org/en/latest/userguide/tasks.html#ignore-results-you-don-t-want) 。

還記得我們有一個 schedule 還沒有講嘛:question:

接下來我就來介紹 schedule :smirk:

### Periodic Tasks

建議可以閱讀官方的文件，可參考 [Periodic Tasks](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)。

Celery 的 schedule 真的還不錯，可以很簡單的設定 schedule，不知道大家有沒有聽過  [Linux](https://www.linux.com/) 上的 Cron Job

（不知道快 google 阿～），他其實功能和 Cron Job 差不多，但你不需要懂太多 [Linux](https://www.linux.com/) 上的設定 ( 雖然我認為

[Linux](https://www.linux.com/) 有機會還是要懂一下 )，就可以完成幾乎一樣的功能。

我們接著執行剛剛的範例，這次我們要再多啟動一個 celery beat，他是一個 schedule，請先進入 docker 容器中，

並且執行以下指令啟動 celery beat，

```cmd
celery -A celery_app beat
```

![alt tag](https://i.imgur.com/rqTK3bB.png)

![alt tag](https://i.imgur.com/jtKLNX7.png)

你會發現多了一個 celery-demo/[celerybeat-schedule](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/celerybeat-schedule.db) ，這個檔案是儲存了一些 schedule 的資料，

接著一樣啟動 worker

```cmd
celery -A celery_app worker -l info
```

上面這段指令，我已經包進去 celery-demo/[docker-compose.yml](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/docker-compose.yml) 的 command 了( 這邊只是說明一下 )，

還記得剛剛前面設定的東西嗎 :grinning:

```python
# schedules
beat_schedule = {
    'every-2-seconds': {
        'task': 'celery_app.tasks.add',
        'schedule': timedelta(seconds=2),
        'args': (5, 8)
    },
    'specified-time': {
        'task': 'celery_app.tasks.add',
        'schedule': crontab(hour=8, minute=50),
        'args': (50, 50)
    }

}
```

`every-2-seconds` 這個每兩秒會呼叫 add task ，並且傳入參數 (5,8) 。

`specified-time` 這個為每天的早上 8 點 50 分會去呼叫 add task ，並且傳入參數 (50,80)  ，

![alt tag](https://i.imgur.com/NfcqjPt.png)

這個要注意時區，我們在前面有設定時區為 `timezone = 'Asia/Taipei'`，更多的 schedule

設定方法可參考 [crontab-schedules](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules)。

## 實戰 Django + Celery

建議搭配影片看比較好理解 :blush:

* [Youtube Tutorial Part3 - 實戰 Django + Celery ( 使用 Docker )](https://youtu.be/3dwRrJml2NQ)

在 [這篇](https://github.com/twtrubiks/django-celery-tutorial) 的教學中，我們使用了發送 e-mail 當做例子，但在這邊，我們換個例子，模擬爬蟲（透過 github api 爬 repos），

然後再模擬轉檔，這邊其實就是簡單將他轉成 csv 檔而已，當前端按下開始抓取的時候，我們很快的回傳  task id  給前端

（使用者這時候可以繼續的瀏覽網頁其他的資訊 ），讓爬蟲以及轉檔在背景處理，使用者可以透過 task id 查詢任務是否

完成（或是說任務完成後寄一封信通知使用者也是可以 :relaxed: ）

詳細的 Django + Celery 設定教學，這邊就不再做介紹，可參考之前 [這篇](https://github.com/twtrubiks/django-celery-tutorial)  的教學 ，或是可以直接參考 Celery 的官網教學

 [First steps with Django](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)，我也是參考這篇教學的 :smile:

在開始介紹前，先簡單的介紹一下 github API ，我們要先取得 token，取得 token 的方法也很簡單，

可參考 [Creating a token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/#creating-a-token)，取得 token 後，

先來試試看一下 api，這邊用 [curl](https://curl.haxx.se/)

( 請記得換上你自己的 token )

```cmd
curl -H "Authorization: token 7f304579ba192b9d351aa8468e09dd9dca29ff31" "https://api.github.com/search/repositories?q=twtrubiks"
```

也可以使用 [postman](https://www.getpostman.com/)，請參考下圖

![alt tag](https://i.imgur.com/H4Y1N6Z.png)

確認正常後，我們再進行下一步驟。

終於到了我們實戰的步驟了:satisfied:

我用 docker 幫大家包成 [docker-compose.yml](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/django_crawler_celery/docker-compose.yml) 了，所以直接執行以下指令即可

```cmd
docker-compose up
```

![alt tag](https://i.imgur.com/kjWyLw4.png)

執行範例時，請啟動記得 RabbitMQ 以及執行 worker，也就是執行

```python
celery -A django_crawler_celery worker -l info
```

上面這段指令，我已經包進去 django_crawler_celery/
[docker-compose.yml](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/django_crawler_celery/docker-compose.yml) 的 command 了，

我們來看一下 django_crawler_celery/tutorial/
[tasks.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/django_crawler_celery/tutorial/tasks.py)

```python
def chain_tasks(language):
    # crawler_repos ->  build_report_task
    task_id = uuid()
    chain(crawler_repos.s(language, 1000, 1), build_report_task.subtask(args=(task_id,), task_id=task_id))()
    return task_id


'''
ref. http://docs.celeryq.org/en/latest/userguide/tasks.html#ignore-results-you-don-t-want
'''


@shared_task(ignore_result=True)
def crawler_repos(language, per_page, page):
    payload = {
        'sort': 'stars',
        'order': 'desc',
        'q': 'language:{}'.format(language),
        'per_page': per_page,
        'page': page
    }
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token {}'.format(settings.GITHUB_OAUTH)
    }
    r = requests.get(
        'https://api.github.com/search/repositories',
        params=payload,
        headers=headers)

    # Simulation file conversion
    time.sleep(10)

    items = r.json()['items']
    return items


@shared_task
def build_report_task(results, task_id):
    rows = [
        [repo.get('name'), repo.get('full_name'), repo.get('html_url'), repo.get('description')]
        for repo in results
    ]
    filename = '{}/github-repos-{}.csv'.format(settings.MEDIA_ROOT, task_id)

    # Simulation file conversion
    time.sleep(10)

    return create_csv(filename, rows)

```

這邊我一樣使用前面介紹的 chain 概念來完成，有兩個 tasks ，分別為 `crawler_repos` 以及 `build_report_task`，

`crawler_repos` 主要是透過 github api 抓取指定語言的 repos，這邊是用 stars 多到少進行排序，詳細的 github api

參數可參考 [github serach api](https://developer.github.com/v3/search/#search)，
`build_report_task` 則是將結果輸出為 csv ，這邊一樣再提一下，`time.sleep(10)`

主要是要模擬需要一些時間才執行的完。

### django-celery-results

還記得前面有說到一個儲存 Celery 結果的 db 嗎？ 就是前面提到的 [results.sqlite](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/celery-demo/results.sqlite)，同樣的在 Django 中，我們可以透過

 [django-celery-results](https://pypi.python.org/pypi/django-celery-results/) 並且利用 ORM 的方式來讀取裡面的資料，

 詳細可參考 [Using the Django ORM/Cache as a result backend](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#django-celery-results-using-the-django-orm-cache-as-a-result-backend)，

簡單說明一下流程，首先先安裝 Library，請在命令列執行

```python
pip install django-celery-results
```

加入 django_celery_results 到 django_crawler_celery/[settings.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/django_crawler_celery/django_crawler_celery/settings.py) 中

```python
INSTALLED_APPS = (
    ...,
    'django_celery_results',
)
```

接著  migration  database

```cmd
python manage.py migrate django_celery_results
```

![alt tag](https://i.imgur.com/u9e9Sdn.png)

這時候你會發現，你的 db 中多了 `django_celery_results_taskresult`

![alt tag](https://i.imgur.com/nSqkEDP.png)

最後在設定一下你的 backend

```python
CELERY_RESULT_BACKEND = 'django-db'
```

現在我們就可以透過 ORM 的方式操作裡面的資料了，使用方法很簡單，就 Django ORM，

記得 import `TaskResult`，可參考下方程式碼

```python
from django_celery_results.models import  TaskResult
TaskResult.objects.all()
```

TaskResult 的 model 可參考 [models.py](https://github.com/celery/django-celery-results/blob/master/django_celery_results/models.py)。

以上步驟我只是說明一下，我都幫大家包進去 django_crawler_celery/[docker-compose.yml](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/django_crawler_celery/docker-compose.yml) 的 command 了:blush:

## 執行畫面

這邊簡單 demo 一下 Django + Celery 的成果，

```cmd
docker-compose up
```

直接瀏覽 [http://localhost:8000/](http://localhost:8000/)，

![alt tag](https://i.imgur.com/LyV40it.png)

當按下 start crawler github 按鈕時，Celery 會開始爬蟲+轉檔，我會很快得先回傳一個 task id 給前端，

我們來看一下 django_crawler_celery/tutorial/
[views.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/django_crawler_celery/tutorial/views.py)

```python
@require_http_methods(["POST", ])
@csrf_exempt
def task_use_celery(request):
    if request.method == 'POST':
        task_id = chain_tasks('python')
        return JsonResponse({"data": task_id})
```

當你按下按鈕就是去呼叫 `task_use_celery`，然後會去執行 `chain_tasks` ，裡面就是 Celery 的 tasks，

這邊用了一個裝飾器 `@csrf_exempt`，這個主要是先忽略 CSRF 的問題，如果不知道什麼是 CSRF，

可參考我之前介紹的 [CSRF-tutorial](https://github.com/twtrubiks/CSRF-tutorial)。

當爬蟲以及成功輸出成 csv 檔之後，就可以在 datatable 中查詢到，

datatable 的部份其實就是透過 [django-celery-results](https://pypi.python.org/pypi/django_celery_results) 利用 ORM 的方式將資料撈出來而已，

可參考 django_crawler_celery/tutorial/
[views.py](https://github.com/twtrubiks/docker-django-celery-tutorial/blob/master/django_crawler_celery/tutorial/views.py)

```python
def dashboard(request):
    results = TaskResult.objects.all()
    return render(request,
                  'tutorial/dashboard.html',
                  {'results': results})
```

![alt tag](https://i.imgur.com/CHBUE6Z.png)

Celery 在背景執行 task

![alt tag](https://i.imgur.com/J9di9vD.png)

task 執行完成後，可在 datatable 中看到

![alt tag](https://i.imgur.com/EyjMnEN.png)

## 後記

這次帶大家用 docker 建立 Celery 環境，相信大家一定覺得很方便，也解決了很多

環境上的問題。Celery 使用情境真的蠻多的，大家有興趣的話可以多玩玩看:laughing:

## 執行環境

* Python 3.6.2

## Reference

* [Django](https://www.djangoproject.com/)
* [Celery](http://celery.readthedocs.io/en/latest/index.html)

## License

MIT licens
