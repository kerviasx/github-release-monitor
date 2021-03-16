'''
    html模板
'''

item = \
"""
    <div class="block">
        <header><a href="{url}">{name}</a><span
                id='label'>{tag}</span><span id="title">{title}</span>
        </header>
        <div class='content'>
            {content}
        </div>
    </div>
"""

HTMLT1 = \
"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email</title>
    <style>
        body {
            margin: 0 auto;
        }

        .block {
            margin: 10px 5px;
        }

        header {
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid transparent;
            border-radius: 4px;
            background-color: #d9edf7;
            text-shadow: 0 1px 0 rgba(255, 255, 255, .2);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, .25), 0 1px 2px rgba(0, 0, 0, .05);
            border-color: #9acfea;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.42857143;
        }

        #label {
            margin-left: 10px;
            display: inline-block;
            min-width: 10px;
            padding: 3px 7px;
            font-size: 12px;
            font-weight: 700;
            line-height: 1;
            color: #fff;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            background-color: #777;
            border-radius: 10px;
        }

        #title {
            float: right;
        }

        .content {
            margin: 0 8px;
            padding: 2px 50px;
            background-color: #eee;
        }

        @media (min-width: 800px) {
            body {
                width: 800px;
            }
        }
    </style>

</head>

<body>
    {}
</body>
</html>
"""
class TEMPLATE(object):
    def __init__(self, data):
        self.data = data
        temp = ""
        for name, li in data.items():
            if li != None:
                temp += item.format(name=name, url=li['url'],title=li['title'],tag=li['tag'],content=li['content'])
            else:
                temp += item.format(name=name, content="获取信息失败")
        self.ret = HTMLT1.format(temp)
        
    def template(self):
        return self.ret
