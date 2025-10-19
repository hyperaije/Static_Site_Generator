import unittest
from blockmarkdown import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node, extract_title

class TestBlock(unittest.TestCase):
    def test_block_code_true(self):
        block = "```This is a code block```"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, blocktype)

    def test_block_code_false(self):
        block = "``This is not a code block``"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_heading_true(self):
        block = "### This is heading text"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, blocktype)

    def test_block_heading_false(self):
        block = "####### This is heading text"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_quote_true(self):
        block = "> This is a quote\n> This is another quote"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, blocktype)

    def test_block_quote_false(self):
        block = "> This is a quote\nThis is not a quote"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_unordered_true(self):
        block = "- This is unordered list text\n- This is a second line"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, blocktype)

    def test_block_unordered_false(self):
        block = "- This is unordered list text\n-This is a second line"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_block_ordered_true(self):
        block = "1. This is an ordered list\n2. This is a second line"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, blocktype)

    def test_block_ordered_false(self):
        block = "1. This is an ordered list\n7. This should be flagged as incorrect"
        blocktype = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, blocktype)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> This is line one
> This is line two
> This is line three
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is line one This is line two This is line three</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is unordered list item 1
- This is unordered list item 2
- This is unordered list item 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is unordered list item 1</li><li>This is unordered list item 2</li><li>This is unordered list item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is unordered list item 1
2. This is unordered list item 2
3. This is unordered list item 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is unordered list item 1</li><li>This is unordered list item 2</li><li>This is unordered list item 3</li></ol></div>",
        )

    def test_heading(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_extract_title(self):
        text = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
    """
        header = extract_title(text)
        self.assertEqual(header, "Heading 1")

if __name__ == "__main__":
    unittest.main()
