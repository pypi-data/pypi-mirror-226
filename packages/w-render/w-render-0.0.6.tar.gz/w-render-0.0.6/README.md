### Description

Web-render is a method of rendering dynamic web pages using Selenium.

### Commands

To start the rendering service, use the following command:

```shell
render-server "web-render -f selenium --headless --proxy=185.105.91.140:1021" "flask-backend"
```

To run a test, use the following command:

```shell
python -W ignore:ResourceWarning -m unittest web_render/base/test_webrender.py
```