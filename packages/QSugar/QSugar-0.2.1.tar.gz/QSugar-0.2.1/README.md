# QSugar
PyQt/PySide framework, dedicated to more modern Declarative UI design. Based on interface injection, achieve separation of interface and data, as well as hierarchical layout design. It is recommended to use it in conjunction with the QBinder framework.

![GIF 2023-8-21 17-30-35](https://github.com/AtticRat/QSugar/assets/129368033/41d24ae4-b731-45db-95e5-73e26efc90cd)

# Other Language

- en [English](README.md)

- zh_CN [简体中文](README.zh_CN.md)

# Qt Module Enhancements
`QSugar` enhances Qt Module using interface injection without the need for source code changes. 

But you need to enhance it by registering the module or class name, e.g.
```python
from QSugar import register

from PySide2.QtWidgets import QPushButton

register(QPushButton) # This is okay

from PySide2 import QtWidgets

register(QtWidgets) # This is okay,too

```

# Layout and Widget Nesting
Thanks to the magic method, `QSugar` allows developers to easily layout using

In the past, you needed to write like this.
```python
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.button_1 = QPushButton('Button1',self)
        self.button_2 = QPushButton('Button2',self)
        self.layout.addWidget(self.button_1)
        self.layout.addWidget(self.button_2)
```

Using QSugar, you can obtain code with higher readability
```python
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = QHBoxLayout(self)[
            QPushButton('Button1',self),
            QPushButton('Button2',self),
        ]
```

Nesting of controls and layouts also applies
```python
ui = QHBoxLayout(self)[
    QFrame(self)[
        QVBoxLayout(self)[
            QPushButton('Button1')
        ]
    ],
    QLabel(self,'Quick Demo')
]
```

Grid layout is also supported, requiring a two-dimensional list
```python
ui = QGridLayout(self)[
    [QPushButton('Row1 Col1'),QPushButton('Row1 Col2')],
    [QPushButton('Row2 Col1'),QPushButton('Row2 Col2')]
]
```

Combining List Expressions to Quickly Implement Similar Layouts
```python
ui = QGridLayout(self)[
    [[QPushButton(str(i+j*3)) for i in range(1,4)] for j in range(1,4)]
]
```

Vertical and horizontal layouts are nested to achieve flexible layout
```python
ui = QVBoxLayout(self)[
    QHBoxLayout(self)[
        QPushButton('A1'),
        QPushButton('A2'),
        QPushButton('A3'),
    ],

    QPushButton('B1'),

    QHBoxLayout(self)[
        QPushButton('C1'),
        QPushButton('C2')
    ]
]
```

# Property simplification
Enhancement of the `prop` method allows for more effective property configuration of widgets.

## Property `objectName` simplification
By using the `name` parameter of the prop method,

you can dynamically add member properties to the parent window while setting the Object Name to the widget.

Named controls can be dynamically obtained through the `findChild` method,

or can be accessed directly as member objects.

(This is recommended as it will enable automatic completion of the IDE, such as PyCharm)

```python
class MyWidget(QWidget):
    def __init__(self):
        self.ui = QVBoxLayout(self)[
            QPushButton(self).prop(
                name="btn_1"
            )
        ]

        self.findChild(QPushButton,"btn_1").setText('Hello,World') # Okay

        if hasattr(self,'btn_1') and isinstance(self.btn_1,QPushButton):
            self.btn_1.setText('Hello,World') # Okay and Recommended
```

## Setter method simplification

It is unnecessary to call the setter function in a tedious manner.
```python
btn = QPushButton(self)
btn.setObjectName("btn_1")
btn.setText("Something")
btn.setStyleSheet("color:blue")
btn.setFixedHeight(40)
btn.setFixedWidth(200)
```

The `prop` method provides a simplified approach,
which can automatically convert `setXXX` method to `xxx` parameter of `prop` method,
such as `setVisible(False)` and `prop(visible=False)`

The parameter names corresponding to the `Setter` method will also be deleted and modified according to the habits specified in `Html`,
such as `setContentsMargins(5,0,0,0)` and `prop(margin=(5,0,0,0))`, `setMinimumWidth(200)` and `prop(min_width=200)`

The equivalent code content is as follows.

```python
QPushButton(self).prop(
    name="btn_1"
    text="Something",
    style="color:blue",
    height=40,
    width=200
)
```

`
Note: There are some differences between the style and qss parameters. The style setting does not allow the use of selectors and can only take effect on the current control. And the scope of action of qss will be wider.
`

The `prop` method is not the only property setter method, `QSugar` reserves the `set` method for injection.

```python
QPushButton(self)
.set("text","Something")
.setStylesheet("color:blue")
```

# Slot function binding simplification

There is almost no difference between it and property setting,

except for the support of the QML signal form `onXXX`,

such as the `onClick` parameter being equivalent to `clicked`.

```python
QPushButton(self).prop(
    clicked=lambda:print('clicked work')
)

QPushButton(self).prop(
    onClick=lambda:print('onClick work')
)
```

QSugar also retains the `bind` and `unbind` methods for binding slot functions and signals

```python
QPushButton(self).bind("clicked",lambda:print('Clicked'))

QPushButton(self).unbind("clicked")
```

# Custom Simplification

QSugar provides `def_prop` and `map_prop` method in `Prop` class,
which allows developers to customize the parameter implementation of the prop method

## Usage of Method `map_prop`

If you are only simplifying the method name, you can consider using it,e.g.

```python
from QSugar import Prop

Prop.map_prop('vis','setVisible')

register(QPushButton)

QPushButton('Button').prop(vis=False)
```

## Usage of Method `def_prop`

For complex situations, consider using `def_prop` method,e.g.

```python
from QSugar import Prop

def debug_prop_method(widget,value):
    if value:
        print(widget)

Prop.def_prop('debug',debug_prop_method)

register(QWidget)

QWidget().prop(debug=True)
```

You can refer to `example/rect.py` for this simplified process.

# Property injection

The `prop` method allows developers to dynamically inject property through dictionary variables,

to achieve the separation of data and interface layout.

```python
from QSugar import Style

btn = {
    'height': 40,
    'align': 'center',
    'style': Style({
        'padding-right': '20px',
        'padding-left': '20px',
        'padding-top': '8px',
        'padding-bottom': '8px',
        'border-radius': '5px'
    })
}

QPushButton('Button1').prop(btn)
QPushButton('Button2').prop(btn)
```

The usage is somewhat similar to CSS style sheets, but it is more customizable

```python
from QSugar import StyleDict

primary = StyleDict({
    'background-color': '#428BCA',
    'color': 'white'
})

success = StyleDict({
    'background-color': '#5CB85C',
    'color': 'white'
})

info = StyleDict({
    'background-color': '#5BC0DE',
    'color': 'white'
})

warning = StyleDict({
    'background-color': '#F0AD4E',
    'color': 'white'
})

danger = StyleDict({
    'background-color': '#D9534F',
    'color': 'white'
})

QPushButton('Primary').prop(primary)
QPushButton('Success').prop(success)
QPushButton('Info').prop(info)
QPushButton('Warning').prop(warning)
QPushButton('Danger').prop(danger)

```

# Example

The project provides an example of a counter, refer to ` example/counter.py`
