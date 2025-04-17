import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag = "p", value = "this is a test paragraph",props = {
    "href": "https://www.google.com",
    "target": "_blank"}
    )
        self.assertEqual(
            "tag: p value: this is a test paragraph children: None props: href=https://www.google.com target=_blank", repr(node)
        )

    def test_none_props(self):
        node = HTMLNode(tag = "p", value = "this is a test paragraph")
        self.assertEqual(
            "tag: p value: this is a test paragraph children: None props: ", repr(node)
        )

    def test_props_to_html(self):
        node = HTMLNode(tag = "p", value = "this is a test paragraph",props = {
    "href": "https://www.google.com",
    "target": "_blank"}
    )
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node.props_to_html())

    # tests for LeafNode class
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(tag = "a", value = "website",props = {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.to_html(), '<a href=\"https://www.google.com\" target=\"_blank\">website</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # tests for ParentNode class
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode("i", "Italic")
        child3 = LeafNode(None, "Plain text")
        parent = ParentNode("p", [child1, child2, child3])
        self.assertEqual(parent.to_html(), "<p><b>Bold</b><i>Italic</i>Plain text</p>")

    def test_parent_node_with_empty_children_list(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_parent_node_with_props(self):
        child = LeafNode("span", "Child")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(parent.to_html(), '<div class="container" id="main"><span>Child</span></div>')

    def test_nested_parent_nodes_with_props(self):
        grandchild = LeafNode("em", "Emphasized")
        child = ParentNode("span", [grandchild], {"class": "highlight"})
        parent = ParentNode("div", [child], {"id": "outer"})
        self.assertEqual(
            parent.to_html(),
            '<div id="outer"><span class="highlight"><em>Emphasized</em></span></div>'
        )

    def test_complex_nesting(self):
        # Create a complex nested structure
        text1 = LeafNode(None, "Hello, ")
        bold = LeafNode("b", "world")
        text2 = LeafNode(None, "!")
        span = ParentNode("span", [text1, bold, text2])
        
        paragraph = ParentNode("p", [span])
        
        list_item1 = ParentNode("li", [LeafNode(None, "First item")])
        list_item2 = ParentNode("li", [LeafNode(None, "Second item")])
        list_item3 = ParentNode("li", [paragraph])
        
        unordered_list = ParentNode("ul", [list_item1, list_item2, list_item3])
        
        div = ParentNode("div", [
            LeafNode("h1", "My Page Title"),
            unordered_list
        ])
        
        expected = (
            "<div>"
            "<h1>My Page Title</h1>"
            "<ul>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "<li><p><span>Hello, <b>world</b>!</span></p></li>"
            "</ul>"
            "</div>"
        )
        
        self.assertEqual(div.to_html(), expected)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
    
    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
    
    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props.get("href"), "https://example.com")

    def test_image(self):
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Empty string for image value
        self.assertEqual(html_node.props.get("src"), "https://example.com/image.png")
        self.assertEqual(html_node.props.get("alt"), "Alt text for image")
        

if __name__ == "__main__":
    unittest.main()