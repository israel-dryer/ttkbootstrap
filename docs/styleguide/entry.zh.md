# 输入框

此小部件具有带各式各样颜色边框的输入框。
边框颜色默认为 __muted__ 并更改为 **primary** 或 _hover_ 上的 [选定颜色](index.md#colors)。
边框厚度将通过 _focus_ 增加。

此小部件还支持 [禁用状态](#disabled-entry)的特殊样式,
[只读状态](#readonly-entry)和[无效状态](#invalid-entry)。

![entry](../assets/widget-styles/entries.gif)

```python
# 默认的输入框(样式)
Entry()

# 红色的输入框(样式)
Entry(bootstyle="danger")
```

## 其他输入框样式

#### 被禁用的输入框

此样式 _不能通过关键字来创建_；它是通过小部件设置进行配置的。

```python
# 创建一个被禁用的输入框
Entry(state="disabled")

# 创建之后再设置输入框为禁用
e = Entry()
e.configure(state="disabled")
```

#### 只读输入框

此样式 _不能通过关键字来创建_；它是通过小部件设置进行配置的。

```python
# 创建一个只读的输入框
Entry(state="readonly")

# 创建之后再设置输入框为只读
e = Entry()
e.configure(state="readonly")
```

#### 验证无效输入

此样式 _不能通过关键字来创建_；你需要在输入框上实施验证。
在**事例**中,你将会找到一个名为[如何验证无效输入并且应用到到输入框](../cookbook/validate-user-input.md)的事例。
