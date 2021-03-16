[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/germaniumhq/mopyx)

MoPyX is a MobX/Vue inspired reactive model driven UI library. UI
Toolkit independent.

Reactive UI is a concept of having the UI automatically update as a
reaction to changes being done in the backend model. This happens
without manually registering listeners, and the reactive framework
keeping track of what parts of the model affect what parts of the
application..
反应式UI的概念是后端模型变化的反应让UI自动更新,不需要手动注册监听器，也不需要反应式框架跟踪模型的哪部分会影响应用的哪部分。
Demo
====

[PiSide2 MoPyX
Demo](https://raw.githubusercontent.com/germaniumhq/mopyx-sample/master/demo.gif)

Full demo project source is here:
<https://github.com/germaniumhq/mopyx-sample>.

@model
======

You decorate your model classes with `@model`. All the properties of
that class will be monitored for changes. Whenever one of those
properties will change, the affected renderers (only the renderer
functions that used that property) will be re-invoked on model changes.
你用`@model`来装饰你的模型类。该类的所有属性都将被监控变化。每当其中一个属性发生变化时，受影响的renderers（只有使用该属性的renderer函数）将在模型变化时被重新调用。
    @model
    class FormModel:
        def __init__(self):
            self.first_name = "John"
            self.last_name "Doe"

@render
=======

You decorate your UI rendering functions with `@render`, or invoke them
with `render_call`. MoPyX will map what render method used what
properties in the model. The parameters for the function will be also
recorded and sent to the renderer function.
你可以用`@render`装饰你的UI渲染函数，或者用`render_call`来调用它们。
MoPyX会将模型中的渲染方法映射到哪个属性上。函数的参数也会被记录下来并发送给renderer函数。
    class UiForm:
        def __init__(self):
            # ...
            self.render_things()

        @render
        def render_things(self):
            self.first_name_label.set_text(self.model.first_name)
            self.last_name_label.set_text(self.model.last_name)

Whenever either `first_name` or `last_name` change in our model,
`render_things` will be invoked again.
每当我们的模型中的 "first_name "或 "last_name "发生变化时。
`render_things`将再次被调用。

In order to optimize the number of UI updates, only the relevant
`@render` functions will be called, not always the topmost one.
为了优化UI更新的次数，只会调用相关的`@render`函数，而不一定是最上面的那个。

So you could break down the previous `@render` method into two methods:

所以你可以将之前的`@render`方法分解成两个方法:
    @render
    def render_things(self):
        self.render_first_name()
        self.render_last_name()

    @render
    def render_first_name(self):
        self.first_name_label.set_text(self.model.first_name)

    @render
    def render_last_name(self):
        self.last_name_label.set_text(self.model.last_name)

Now if only the `first_name` changes in the model, the set\_text for the
`last_name` will not be invoked. This happens automatically, and only
the needed renderers will be invoked.
现在，如果模型中只有 "first_name "发生变化，"last_name "的set_text将不会被调用。
这是自动发生的，只有需要的renderers才会被调用。

To type less, `render_call()` will just wrap the given callable into a
`@render`. For example we can rewrite our renderer to be shorter:
为了减少类型，`render_call()`只是将给定的callable包装成`@render`。
例如，我们可以将renderer重写得更短:

    @render
    def render_things(self):
        render_call(lambda: self.first_name_label.set_text(self.model.first_name))
        render_call(lambda: self.last_name_label.set_text(self.model.last_name))

`@render` methods are not allowed to do model changes while running. If
setting an UI value will trigger a model change, read the
`ignore_updates` section.
`@render`方法不允许在运行时进行模型修改。
 如果设置一个UI值会触发模型变化，请阅读`ignore_updates`部分。

@action
=======

If they’re not wrapped in an action, every property is also an action,
so after the property change, a rendering will trigger. To improve
performance you can wrap multiple model updates into a single `@action`.
An action method can call other methods, including other \`@action\`s.
如果它们没有被包裹在一个动作中，那么每个属性也是一个动作，所以在属性改变后，会触发渲染。
为了提高性能，你可以将多个模型更新包装成一个`@action`。

一个action方法可以调用其他方法，包括其他``@action`s。
When when the top most `@action` finishes the rendering will be invoked.
MoPyX will find out what renderers need to be called, and what computed
properties should be updated, in order to get the UI into a consistent
state.
当最上面的`@action`完成时，渲染将被调用。
MoPyX将找出哪些渲染器需要被调用，哪些计算的属性需要更新，以使UI状态一致。

Internally all the properties setters in the `@model` classes are
wrapped in \`@action\`s.
在内部，`@model`类中的所有属性设置器都被包裹在`@action`s中。

    @action  # without this we'd trigger a render after each assignment
    def change_model(self):
        self.first_name = "Jane"
        self.last_name = "Mary"

@computed
=========

You can also create properties on the model using the `@computed`
decorator. This works similarly with a regular python `@property` but it
will be invoked only when one of the other properties it depends on
(including from other MoPyX models) change. Otherwise calling this
property will return the previously computed value.
你也可以使用`@computed`decorator在模型上创建属性。
它的工作原理与常规的 python `@property`类似，但只有当它所依赖的其他属性之一(包括来自其他 MoPyX 模型的)发生变化时才会被调用。
否则调用这个属性将返回之前计算的值。
This is great for difficult to compute properties. Have a list that must
be accessed as sorted, but comes from the data store as unsorted? You
can wrap it in a `@computed` method. Again, note that the `@computed`
method will only be invoked when the used properties by that `@computed`
method will change:
这对于难以计算的属性来说是非常好的。
有一个必须按顺序访问的列表，但从数据存储中得到的却是未排序的？
你可以用`@computed`方法把它包起来。再次注意，只有当`@computed`方法所使用的属性发生变化时，`@computed`方法才会被调用。
    @model
    class RootModel:
        def __init__(self):
            self.backend_data = []

        @action
        def fetch_data(self):
            self.backend_data = fetch_data_from_service()

        @computed
        def first_five_items(self):
            # will only be invoked when self.backend_data changes
            result = list(self.backend_data)

            result.sort()
            result = result[0:5]

            return result

    class UiRenderer:
        # ...
        @render
        def render_items(self):
            # will be invoked only when first_five_items changes
            for item in self.root_model.first_five_items:
                self.render_item(item)

`@computed` properties are not allowed to change the state of the
object.
`@computed`属性不允许改变对象的状态。
List
====

If one of the properties is a list, the list will be replaced with a
special implementation, that will also notify its changes on the top
property.
如果其中一个属性是一个列表，这个列表将被一个特殊的实现所取代，该实现也将在顶层属性上通知其变化。
    @model
    class RootModel:
        def __init__(self):
            self.items = []


    class UiComponent:
        @render
        def update_ui(self):
            for item in self.items:
                self.render_sub_component(item)


    model = RootModel()
    ui = UiComponent(model)


    model.items.append("new item")  # this will trigger the update_ui rerender.

ignore\_updates
===============

If the renderer will call a value that sets something in the UI that
will make the UI trigger an event, that will in turn might land in an
action (model updates are also actions), you can disable the rendering
using the `ignore_updates` attribute. This will suppress *all action
invocations* from that rendering method, including *all model updates*.
如果渲染器将要调用一个值在UI中做一些事情，会使UI触发一个事件，而这个事件又可能落在一个动作中（模型更新也是动作），你可以使用`ignore_updates`属性禁用渲染。
这将禁用该渲染方法的*所有动作调用*，包括*所有模型更新*。

This is great for onchange events for input edits, or tree updates such
as selected nodes that otherwise would enter an infinite recursion.
这对于输入编辑的onchange事件或树的更新(比如选定的节点)是有利的，否则就会进入无限递归。

Debugging
=========

To check what goes on, you can export in your environment:

-   `MOPYX_DEBUG` - this will print the rendering process on the
    console.

-   `MOPYX_THREAD_CHECK` - this will throw an exception if the thread
    for `@render` methods change.


