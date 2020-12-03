# GitHub Release Monitor

A small python spider project for monitoring publication of  github project release.

It will send an email to specific E-mail addresses if new releases is published.

Just want to learn how to use github actions.

## You need to know before running

You need to read `src/conf/setting.py`.

```python
GITHUB_RELEASES = {
    "hexo-next": "https://github.com/next-theme/hexo-theme-next/releases",
    "Halo": "https://github.com/halo-dev/halo/releases",
}
```

`GITHUB_RELEASES`: The project you want to monitor, please use right url .

In the project structure, `data and log folder` is auto-generated. You can rm these folders after cloning the project.

## Run on local environment
You need to change src/conf/setting.py.
```python
MAIL = {
    "email": None, #sender email  example: 'xxx@qq.com'
    "password": None, # password of stmp  example: 'xxxxxxxxxxxx'
    "receivers": None # receivers example: ['xxx@qq.com', 'xxx@email.com']
}
```
**Note**: Only support QQ Mail for sending now.

## Run on github action
You need to set secrets of actions before using.

| SecretName     | Description        | Exampe                    |
| -------------- | ------------------ | ------------------------- |
| MAIL_USERNAME  | sender             | abc@qq.com                |
| MAIL_PASSWORD  | password of smtp   | xxxxxxxxxxxx              |
| MAIL_RECEIVERS | receivers          | abc@qq.com, abc@gmail.com |
| ACCESS_TOKEN   | access key of repo | It's useless actually     |