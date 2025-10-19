from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node, text_to_textnodes

def markdown_to_blocks(markdown):
    final_list = []
    split_text = markdown.split("\n\n")
    for block in split_text:
        stripped_block = block.strip()
        if stripped_block != "":
            final_list.append(stripped_block)
    return final_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    if re.match(r"^#{1,6}$", block.split(" ", 1)[0]):
        return BlockType.HEADING
    block_lines = block.split("\n")
    if block[:2] == "> ":
        for line in block_lines:
            if line[:2] != "> ":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block[:2] == "- ":
        for line in block_lines:
            if line[:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block[:3] == "1. ":
        count = 1
        for line in block_lines:
            if line[:3] != f"{count}. ":
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    htmlnodes = []
    for node in text_to_textnodes(text):
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children_list = []
    for block in markdown_blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.CODE:
            node = TextNode(block[4:-3], TextType.CODE)
            children_list.append(ParentNode("pre", [text_node_to_html_node(node)]))
        elif blocktype == BlockType.PARAGRAPH:
            children_list.append(ParentNode("p", text_to_children(" ".join(block.split()))))
        elif blocktype == BlockType.QUOTE:
            quotelines = block.split("\n")
            for i in range(len(quotelines)):
                quotelines[i] = quotelines[i][2:]
            text = " ".join(quotelines)
            children_list.append(ParentNode("blockquote", text_to_children(text)))
        elif blocktype == BlockType.UNORDERED_LIST:
            list_lines = block.split("\n")
            text = ""
            for line in list_lines:
                text += "<li>" + line[2:] + "</li>"
            children_list.append(ParentNode("ul", text_to_children(text)))
        elif blocktype == BlockType.ORDERED_LIST:
            list_lines = block.split("\n")
            text = ""
            for line in list_lines:
                text += "<li>" + line[3:] + "</li>"
            children_list.append(ParentNode("ol", text_to_children(text)))
        else:
            seperate_heading = block.split(" ", 1)
            heading_number = seperate_heading[0].count("#")
            children_list.append(ParentNode(f"h{heading_number}", text_to_children(seperate_heading[1])))
    return ParentNode("div", children_list)

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block.startswith("# "):
            return block[2:]
    raise Exception("Error: No h1 header found")
