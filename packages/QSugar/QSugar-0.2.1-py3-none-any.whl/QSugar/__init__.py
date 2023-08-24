import uuid
from typing import Iterable

try:
    from Qt.QtCore import Qt, Signal, QObject
    from Qt.QtGui import QPixmap
    from Qt.QtWidgets import QWidget, QLayout, QLabel
except ImportError:
    from qtpy.QtCore import Qt, Signal, QObject
    from qtpy.QtGui import QPixmap
    from qtpy.QtWidgets import QWidget, QLayout, QLabel


class EasyPropInterface:
    """
    QSuagr Property Extension Interface
    which extends `prop` and `__getitem__` method
    """

    PropMethodMap = {
        'qss': 'setStyleSheet',
        'max_width': 'setMaximumWidth',
        'min_width': 'setMinimumWidth',
        'max_height': 'setMaximumHeight',
        'min_height': 'setMinimumHeight',
        'max_size': 'setMaximumSize',
        'min_size': 'setMinimumSize',
        'width': 'setFixedWidth',
        'height': 'setFixedHeight',
        'size': 'setFixedSize',
        'margin': 'setContentsMargins',
    }
    '''
    QSugar property setter method mapping dictionary
    '''

    @staticmethod
    def name_prop_method(obj: QObject, value: str):
        """
        Default `name` property setter method definition
        """
        obj.setObjectName(value)
        if obj.parent():
            setattr(obj.parent(), value, obj)

    @staticmethod
    def style_prop_method(widget: QWidget, value: str):
        """
        Default `style` property setter method definition
        """
        if widget.objectName() == '':
            widget.setObjectName(str(uuid.uuid4()))
        qss = '#' + widget.objectName() + '{' + value + '}'
        widget.setStyleSheet(qss)

    @staticmethod
    def src_prop_method(obj: QObject, value: str):
        """
        Default `src` property setter method definition
        """
        if isinstance(obj, QPixmap):
            obj.load(value)
        elif isinstance(obj, QLabel):
            obj.setPixmap(QPixmap(value))

    PropMethodDefine = {
        'name': name_prop_method,
        'style': style_prop_method,
        'src': src_prop_method
    }
    '''
    QSugar property setter method definition dictionary
    '''

    @staticmethod
    def style_prop_conflict_method(old_value: str, new_value: str):
        """
        Default `style` property conflict method definition
        """
        return old_value + ';\n' + new_value

    @staticmethod
    def qss_prop_conflict_method(old_value: str, new_value: str):
        """
        Default `qss` property conflict method definition
        """
        return old_value + ';\n' + new_value

    PropConflictMethodDefine = {
        'style': style_prop_conflict_method,
        'qss': qss_prop_conflict_method,
    }
    '''
    QSugar property conflict method definition dictionary
    '''

    @classmethod
    def def_prop(cls, name: str, func):
        """
        QSugar custom property setter definition method
        :param name:property name
        :param func:setter method func(obj,value)
        :return:`Prop` Class
        """
        cls.PropMethodDefine[name] = func
        return cls

    @classmethod
    def map_prop(cls, name: str, func_name: str):
        """
        QSugar custom property setter definition method
        :param name:property name
        :param func_name:setter method name
        :return:`Prop` Class
        """
        cls.PropMethodMap[name] = func_name
        return cls

    def prop(self, *prop_objs: Iterable[dict], **kwargs):
        """
        QSugar property setter method
        :param prop_objs: property injection dictionary
        :param kwargs: property key-value
        :return: method caller
        """
        if kwargs is None:
            kwargs = dict()

        for prop_obj in prop_objs:
            conflict_props = prop_obj.keys() & self.PropConflictMethodDefine.keys()
            if conflict_props == 0:
                kwargs.update(prop_obj)
            else:
                for prop in prop_obj:
                    if prop in conflict_props:
                        if prop in kwargs:
                            kwargs[prop] = self.PropConflictMethodDefine[prop](kwargs[prop], prop_obj[prop])
                        else:
                            kwargs[prop] = prop_obj[prop]
                    else:
                        kwargs[prop] = prop_obj[prop]

        for name_, value_ in kwargs.items():
            if name_ in self.PropMethodDefine:
                func = self.PropMethodDefine[name_]
                func(self, value_)
            elif name_ in self.PropMethodMap:
                setter_name = self.PropMethodMap[name_]
                setter = getattr(self, setter_name)
                try:
                    setter(value_)
                except TypeError as e:
                    if isinstance(value_, Iterable):
                        setter(*value_)
                    else:
                        raise e
            else:
                # Signal Property Mapper
                if name_.startswith('on'):
                    name_ = name_.removeprefix('on')
                    name_ += 'ed'
                    name_ = name_.lower()

                if hasattr(self, name_):
                    prop = getattr(self, name_)
                    if isinstance(prop, Signal):
                        prop.connect(value_)

                # Qt Default Property Mapper
                setter_name = 'set' + name_.title()
                if hasattr(self, setter_name):
                    setter = getattr(self, setter_name)
                    try:
                        setter(value_)
                    except TypeError as e:
                        if isinstance(value_, Iterable):
                            setter(*value_)
                        else:
                            raise e
                else:
                    self.setProperty(name_, value_),
        return self

    def __getitem__(self, children):
        """
        QSuagr nesting containers method simplifying `setXXX` and `addXXX`
        :param children:children
        :return:method caller
        """
        if isinstance(children, Iterable):
            for child in children:
                for class_ in type(child).mro():
                    class_name = class_.__name__.removeprefix('Q')
                    add_func_name = 'add' + class_name.title()
                    if hasattr(self, add_func_name):
                        add_func = getattr(self, add_func_name)
                        add_func(child)

                    setter_name = 'set' + class_name.title()
                    if hasattr(self, setter_name):
                        setter = getattr(self, setter_name)
                        setter(child)
        else:
            child = children
            for class_ in type(child).mro():
                class_name = class_.__name__.removeprefix('Q')
                add_func_name = 'add' + class_name.title()
                if hasattr(self, add_func_name):
                    add_func = getattr(self, add_func_name)
                    add_func(child)

                setter_name = 'set' + class_name.title()
                if hasattr(self, setter_name):
                    setter = getattr(self, setter_name)
                    setter(child)
        return self

    def set(self, prop, value):
        """
        QSugar reserved property setter method
        :param prop:property name
        :param value:property value
        :return:method caller
        """
        setter_name = "set" + prop.title()
        setter = getattr(self, setter_name)
        setter(value)
        return self

    def bind(self, signal: str, fn):
        """
        QSugar reserved signal and slots binding method
        :param signal: signal name
        :param fn: slots function
        :return: method caller
        """
        getattr(self, signal).connect(fn)
        return self

    def unbind(self, signal: str):
        """
        QSugar reserved signal and slots unbinding method
        :param signal: signal name
        :return: method caller
        """
        getattr(self, signal).disconnect()
        return self


Prop = EasyPropInterface


class EasyLayoutInterface:
    """
    QSuagr Layout Extension Interface
    which extends `__getitem__` method , `align` nad `stretch` params in `prop`
    """

    AlignFlags = {
        'justify': Qt.AlignJustify,
        'center': Qt.AlignCenter,
        'h_center': Qt.AlignHCenter,
        'v_center': Qt.AlignVCenter,
        'left': Qt.AlignLeft,
        'right': Qt.AlignRight,
        'top': Qt.AlignTop,
        'bottom': Qt.AlignBottom,
    }
    '''
    Alignment property value and Qt alignment flag mapping dictionary
    '''

    def __getitem__(self, *children):
        """
        QSuagr nesting containers method simplifying `addWidget` and `andLayout`
        :param children: children
        :return: method caller
        """
        while isinstance(children, tuple) and len(children) == 1:
            children = children[0]

        if isinstance(children, Iterable):
            for row, row_children in enumerate(children):
                if isinstance(row_children, Iterable):
                    for col, child in enumerate(row_children):

                        if isinstance(child, slice):
                            on_init = child.stop
                            on_del = child.step
                            child = child.start

                            if on_init:
                                on_init(child)
                            if on_del:
                                child.__del__ = on_del

                        if isinstance(child, QWidget):
                            self.addWidget(child, row, col)
                        elif isinstance(child, QLayout):
                            self.addLayout(child, row, col)

                else:
                    child = row_children

                    if isinstance(child, slice):
                        on_init = child.stop
                        on_del = child.step
                        child = child.start

                        if on_init:
                            on_init(child)
                        if on_del:
                            child.__del__ = on_del

                    args = [child]

                    stretch = child.property("stretch")
                    if stretch:
                        args.append(stretch)

                    align = child.property("align")
                    if align:
                        align = self.AlignFlags[align]
                        if not stretch:
                            args.append(1)
                        args.append(align)

                    if isinstance(child, QWidget):
                        self.addWidget(*args)
                    elif isinstance(child, QLayout):
                        self.addLayout(*args)

        else:
            child = children
            args = [child]

            if isinstance(child, slice):
                on_init = child.stop
                on_del = child.step
                child = child.start
                if on_init:
                    on_init(child)
                if on_del:
                    child.__del__ = on_del

                stretch = child.property("stretch")
                if stretch:
                    args.append(stretch)

                align = child.property("align")
                if align:
                    if not stretch:
                        args.append(1)
                    align = self.AlignFlags[align]
                    args.append(align)

            if isinstance(child, QWidget):
                self.addWidget(*args)
            elif isinstance(child, QLayout):
                self.addLayout(*args)

        return self


Layout = EasyLayoutInterface


def register(*qt_class_or_module) -> None:
    """
    Qt module/class QSugar enhanced registration function
    :param qt_class_or_module:Qt class or module
    """
    for each in qt_class_or_module:
        typename = type(each).__name__
        if typename in ('type', 'ObjectType'):
            if issubclass(each, object):
                each.PropMethodMap = EasyPropInterface.PropMethodMap
                each.PropMethodDefine = EasyPropInterface.PropMethodDefine
                each.PropConflictMethodDefine = EasyPropInterface.PropConflictMethodDefine
                each.prop = EasyPropInterface.prop
                each.set = EasyPropInterface.set
            if issubclass(each, QObject):
                each.bind = EasyPropInterface.bind
                each.unbind = EasyPropInterface.unbind
                each.__getitem__ = EasyPropInterface.__getitem__
            if issubclass(each, QLayout):
                each.AlignFlags = EasyLayoutInterface.AlignFlags
                each.__getitem__ = EasyLayoutInterface.__getitem__
        elif typename == 'module':
            for module_obj in dir(each):
                if hasattr(each, module_obj):
                    register(getattr(each, module_obj))


def StyleDict(style: dict):
    """
    convert qss style from dictionary to QSugar property dictionary
    :param style: qss style dictionary
    :return: QSugar property dictionary
    """
    content = ''
    for key, value in style.items():
        content += str(key) + ':' + str(value) + ';'
    return {'style': content}


def Style(style: dict):
    """
    convert qss style from dictionary to string
    :param style: qss style dictionary
    :return: qss style string
    """
    content = ''
    for key, value in style.items():
        content += str(key) + ':' + str(value) + ';'
    return content
