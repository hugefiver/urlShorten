from typing import Any, Union

from django.shortcuts import (render, HttpResponse,
    HttpResponseRedirect, get_object_or_404)
from django.views.decorators.csrf import csrf_exempt

import random
from .utils import *
from .models import LinkURL

# Create your views here.


@csrf_exempt
def get_shorten(request):
    context = {}
    clean_out_time_urls()
    # BASE_HOST = request.scheme + '://' + request.get_host() + '/'
    BASE_HOST = 'https://' + request.get_host() + '/'

    if request.method == 'POST':
        context['status'] = 0
        try:
            # 尝试获取链接
            url: str = request.POST['url']
        except KeyError:
            # 链接不存在 [ERROR 253]
            context = {'status': 253, 'stat_msg': 'Complete keys expect.'}
            return render(request, 'result.html', context)
        else:
            # 获取链接和MD5码
            url = ''.join(url.split())
            ha = get_md5(url)

            # 判断链接合法性
            if not url:
                # 输入为空 [ERROR 252]
                context['status'] = 252
                context['stat_msg'] = '请输入链接。'
            elif not url.startswith(('http://', 'https://', 'ftp://',
                                     'sftp://', 'ed2k://', 'smb://')):
                # 输入非合法链接 [ERROR 251]
                context['status'] = 251
                context['stat_msg'] = '请输入正确的链接。'
            else:
                now = datetime.datetime.now()
                end = now + datetime.timedelta(hours=24)
                # 查看链接是否已在数据库
                try:
                    o = LinkURL.objects.get(url=url)
                    # 获取short_code并更新时间
                    context['status'] = 1
                    context['stat_msg'] = BASE_HOST + o.short_code
                    o.end_time = end
                    o.save()
                except LinkURL.DoesNotExist:
                    # 起始长度
                    n = BASE_CODE_LEN
                    code = ha[:n]
                    while True:
                        try:
                            o = LinkURL.objects.get(short_code=code)
                        except LinkURL.DoesNotExist:
                            o = LinkURL(url=url, short_code=code,
                                        end_time=end)
                            o.save()
                            break
                        else:
                            n += 1
                            if n > 32:
                                code += random.choice(random_seed)
                            else:
                                code = ha[:n]
                    context['status'] = 0
                    context['stat_msg'] = BASE_HOST + code

            return render(request, 'result.html', context)
    else:
        # 非post请求 [ERROR 254]
        context = {
            'status': 254,
            'stat_msg': 'NO GET.'
        }
        return render(request, 'result.html', context)


def service_redirect(request, srt_code):
    # BASE_HOST = request.scheme + '://' + request.get_host() + '/'
    BASE_HOST = 'https://' + request.get_host() + '/'
    try:
        o = LinkURL.objects.get(short_code=srt_code)
        return HttpResponseRedirect(o.url)
    except LinkURL.DoesNotExist:
        return HttpResponse(content=render(request, 'index.html',
                                           context={'from_url': BASE_HOST+srt_code}),
                            status=404)


@csrf_exempt
def index(request):
    return render(request, 'index.html')


def http404(request):
    return render(request, 'index.html')
