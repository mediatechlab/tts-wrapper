from tts_wrapper import SSMLNode


def test_simple_tag():
    assert str(SSMLNode("speak")) == "<speak></speak>"


def test_tag_with_attrs():
    assert str(SSMLNode("speak", {"foo": "bar"})) == '<speak foo="bar"></speak>'


def test_tag_with_children():
    assert (
        str(SSMLNode("speak", children=[SSMLNode("a"), SSMLNode("b")]))
        == "<speak><a></a><b></b></speak>"
    )


def test_add_node():
    assert str(SSMLNode("speak").add(SSMLNode("a"))) == "<speak><a></a></speak>"


def test_add_text():
    assert (
        str(SSMLNode("speak").add(SSMLNode("a").add("hello")))
        == "<speak><a>hello</a></speak>"
    )
