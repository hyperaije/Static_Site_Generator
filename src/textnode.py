from enum import Enum 
from htmlnode import LeafNode
from extract_markdown import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other_text):
        if self.text == other_text.text and self.text_type == other_text.text_type and self.url == other_text.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Error: Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiter_dict = {"**":TextType.BOLD, "_":TextType.ITALIC, "`":TextType.CODE}
    if delimiter not in delimiter_dict:
        raise Exception("Error: Delimiter not supported, this function only supports **, _, and `")
    else:
        if delimiter_dict[delimiter] != text_type:
            raise Exception("Error: Delimiter and text_type do not match.")

    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            split_node_text = node.text.split(delimiter)
            if len(split_node_text) % 2 == 0:
                raise Exception(f'Error: Invalid Markdown syntax, no closing "{delimiter}" found.')
            for i in range(len(split_node_text)):
                if split_node_text[i] == "":
                    continue
                if i % 2 != 0:
                    split_nodes.append(TextNode(split_node_text[i], text_type))
                else:    
                    split_nodes.append(TextNode(split_node_text[i], TextType.TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if images == []:
                new_nodes.append(node)
                continue
            else:
                split_nodes = [node.text]
                count = 0
                for image in images:
                    split_nodes = split_nodes[-1].split(f"![{image[0]}]({image[1]})", 1)
                    if split_nodes[0] != "":
                        new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    count += 1
                    if count == len(images) and split_nodes[-1] != "":
                        new_nodes.append(TextNode(split_nodes[-1], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if links == []:
                new_nodes.append(node)
                continue
            else:
                split_nodes = [node.text]
                count = 0
                for link in links:
                    split_nodes = split_nodes[-1].split(f"[{link[0]}]({link[1]})", 1)
                    if split_nodes[0] != "":
                        new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    count += 1
                    if count == len(links) and split_nodes[-1] != "":
                        new_nodes.append(TextNode(split_nodes[-1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.TEXT)]
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes
    